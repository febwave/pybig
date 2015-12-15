# -*- coding:utf-8 -*-
import os
import sys
import re
import signal
import pyStoreDefine as bsd
import mongoAccesslib as MA
import multiprocessing 
import threading
import pyReduce
import time

def sigHandler(signum, frame):
    global bExit
    bExit = 0
    print("receive a signal %d, is_exit = %d"%(signum, bExit))
    _thread.interrupt_main()
    


########################################################################
class TaskManager(object):
    """"""

    bExit = False
    #----------------------------------------------------------------------
    def __init__(self,storeAddress,storePort,dbuser, dbpassword, database,host, port):
        """Constructor"""
        self.exitFlag = False
        self.queryInterval = 1
        self.storeAddress = storeAddress
        self.storePort = storePort
        self.dbUser = dbuser
        self.dbpassword = dbpassword
        self.database = database
        self.host = host
        self.port = port              
        self.failedLst = dict()
        self.topicValidateLst = dict()
        
        self.storeTpTable = None
        self.cocurrence = 4
        
        self.ppool = multiprocessing.Pool(self.cocurrence )
        self.resolvedStateLst = dict()
        
        self.ma = MA.MongoAccess()
        self.storeConnected = False              
     
        signal.signal(signal.SIGINT, sigHandler)
        signal.signal(signal.SIGTERM, sigHandler)          
        
    def Close(self):
        self.ppool.close()
        self.ppool.join()
        if(self.storeConnected):
            self.ma.disconnect()        
            
    def createDBInstance(self):
        try:
            import mysql.connector
            self.cnx = mysql.connector.connect(user = self.dbUser, password = self.dbpassword, database=self.database,host=self.host, port=self.port)
            self.cursor = self.cnx.cursor()
        except Exception as exc:     
            raise exc
        
    def doConnect(self):
        if(self.storeConnected == False):
            self.ma.connect(self.storeAddress,self.storePort)
            self.storeConnected = True     
            
    @staticmethod    
    def queryTopicIndexerProc(clsObj):
        if(clsObj.exitFlag):
            return        
        
        clsObj.queryTopicIndexer() 
        clsObj.activeQuery()

    
    def updatePendingState(self,tps, tpn ,result,recID):
        print('callback %s %s' %(tps, tpn) )
        if(result != 0):
            if( recID not in self.failedLst):
                self.failedLst[recID] = (tps,tpn)
        else:
            queryParams = dict()                    
            queryParams['_id'] =  recID
                            
            valueParams  =dict()
            valueBuffer = dict()
            valueBuffer[bsd.StoreDefine.FD_TP_STATUS] = 1
            valueParams['$set'] = valueBuffer
            self.ma.update(self.storeTpTable,queryParams,valueParams)          
    
    def queryTopicIndexer(self):
        self.doConnect()
        if(self.storeTpTable is None):
            objDB = self.ma.queryDatabase(bsd.StoreDefine.DB_NAME, False)
            if(objDB is None):
                return False
            self.storeTpTable = self.ma.queryCollection(objDB, bsd.StoreDefine.TB_TOPIC_LIST, False)
            if(self.storeTpTable is None):
                return False
            
        queryParams = dict()       
        queryParams[bsd.StoreDefine.FD_TP_STATUS] = 0           
        
        filterParams = dict()        
        filterParams['_id']= 1
        filterParams[bsd.StoreDefine.FD_TP_NS]= 1
        filterParams[bsd.StoreDefine.FD_TP_NAME]= 1       
        
              
        
        deletedLst = list()
        
        for (recID,resolvedState) in self.resolvedStateLst.items():
            if(resolvedState.ready()):
                (tps, tpn ,result) = resolvedState.get()
                self.updatePendingState(tps, tpn, result,recID)
                deletedLst.append(recID)
                
        for recID in deletedLst:
            self.resolvedStateLst.pop(recID)
            
        
        
        batchQueryCount = self.cocurrence - len(self.resolvedStateLst)  
        if(batchQueryCount ==0):
            return False
        
        results =self.ma.queryDocuments(self.storeTpTable, queryParams,filterParams,batchCount= batchQueryCount )
        for objRow in results:
            tps = objRow[bsd.StoreDefine.FD_TP_NS]
            tpn = objRow[bsd.StoreDefine.FD_TP_NAME]
            recID = objRow['_id']

            if(recID in self.resolvedStateLst):
                continue

            if(recID in self.topicValidateLst):
                print('duplicated %s %s' %(recID, self.topicValidateLst[recID]) )
                continue            
            
            print('dispatch %s %s' %(tps, tpn) )                  
           
            self.resolvedStateLst[recID] =self.ppool.apply_async(func=pyReduce.execReduce, args=(self.storeAddress, self.storePort, self.dbUser, self.dbpassword, 
                                                                                                       self.database, self.host, self.port, tps, tpn,) ) 
              
            self.topicValidateLst[recID] = tpn
        return True 
   
        
    def activeQuery(self):
        threading.Timer(self.queryInterval, TaskManager.queryTopicIndexerProc,(self,)).start()
    
    def DoLoop(self):
        global bExit 
        bExit = 1 
        self.activeQuery()
        while(bExit == 1):        
            try:
                time.sleep(1)
            except:
                pass
        self.exitFlag = True
        print("exit now")
        
            
        
        
if __name__ == '__main__':
    storeAddress = '192.168.237.144'
    storePort =27017
    dbuser ='root'
    dbpassword='bnm123'
    database ='mystore'
    host='192.168.237.144'
    port  = 3306

    print("press ctrl c  to exit\n")       
    
    tm = TaskManager(storeAddress, storePort, dbuser, dbpassword, database,  host, port)    
    tm.DoLoop()
    tm.Close()
    
