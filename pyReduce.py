# -*- coding:utf-8 -*-
import os
import sys
import pyStoreDefine as bsd
import mongoAccesslib as MA
import pymongo


def execReduce(storeAddress,storePort,dbuser, dbpassword, database,host, port,tps,tpn):
    print('excute %s %s' %(tps, tpn) )
    inst = Reduce(storeAddress, storePort, dbuser, dbpassword, database, host, port)
    result = inst.Calc(tps, tpn)
    inst.Close()    
    # report taskmanager 
    return (tps, tpn ,result)

########################################################################
class Reduce(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self,storeAddress,storePort,dbuser, dbpassword, database,host, port):
        """Constructor"""
        self.storeAddress = storeAddress
        self.storePort = storePort            
        self.dbUser = dbuser
        self.dbpassword = dbpassword
        self.database = database
        self.host = host
        self.port = port      
        self.cnx = None
        self.cursor = None        
        self.ma = MA.MongoAccess()
        self.storeConnected = False           
        self.batchCount = 100
        
    def Close(self):
        if(self.storeConnected):
            self.ma.disconnect()
        if(self.cnx is not None):
            self.cursor.close()
            self.cnx.close()
            
    
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
            
    def Calc(self,tps,tpn):
        self.doConnect()
        
        # for batch query
        skipItem = 0
        
        # for calc 
        exDate = None
        openPrice = None
        closePrice = None
        lotSize = 0
        highPrice = 0
        lowPrice = 0       
        secExTotal = 0       
        
        dailyID = 0
        
        objDB = self.ma.queryDatabase(bsd.StoreDefine.DB_NAME, False)
        if(objDB is None):
            return 1
        storeDetailTable = self.ma.queryCollection(objDB, tps, False)
        if(storeDetailTable is None):
            return 2
        
        queryParams = dict()       
        queryParams[bsd.StoreDefine.FD_NS_F_TOPIC] = tpn        
        filterParams = dict()        
        filterParams['_id']= 0    
        
        sortParams = list()
        sortParams.append((bsd.StoreDefine.FD_NS_F_SEQ,pymongo.ASCENDING))        

        self.createDBInstance()
        
        while(True):
            # get detail with batch
            results =self.ma.queryDocuments(storeDetailTable, queryParams,filterParams,sortParams,  self.batchCount,skipItem)            
            gotRowCount = results.count(with_limit_and_skip=True)
          
            if(gotRowCount ==0):
                break                        
            
            calcResult = list()
            skipItem +=gotRowCount
            for objRow in results:
                # calc                                
                secTime = objRow[bsd.StoreDefine.FD_NS_F_TIME]
                secSeq =  objRow[bsd.StoreDefine.FD_NS_F_SEQ]
                secCode = objRow['P1']
                secName = objRow['P2'].replace("\'","\'\'")
                secNS = objRow[bsd.StoreDefine.FD_NS_F_NS]
                secTime = objRow[bsd.StoreDefine.FD_NS_F_TIME]
                secPrice = float(objRow['P6'])
                secLotSize = float(objRow['P15'])
                
                if(exDate is None):
                    exDate = secTime
                
                if(openPrice is None):
                    openPrice = secPrice
                    lowPrice = openPrice
                    highPrice = lowPrice
                  
                if(secPrice > highPrice):
                    highPrice = secPrice
                    
                if(secPrice < lowPrice):
                    lowPrice = secPrice
                
                closePrice = secPrice                
                
                secExTotal += secLotSize
                
                calcResult.append((secSeq,secTime,secPrice,secLotSize))            
            
            
            # insert or update secDaily
            if(dailyID == 0):
                query = ("insert into secDaily (secCode,secName,ns,dayNum,secTime,openPrice,closePrice,highPrice,lowPrice,changeTotal,exQty) "
                         "values( \'%s\',\'%s\',\'%s\',%d,\'%s\',%f,%f,%f,%f,%d,%d);" % (secCode,secName,secNS,0,exDate,openPrice,closePrice,highPrice,lowPrice, skipItem, secExTotal))
                self.cursor.execute(query)             
                dailyID = self.cursor.lastrowid            
            else:
                query = ('update  secDaily '
                         ' set closePrice = %f'
                         ',highPrice = %f'
                         ',lowPrice = %f'
                         ',changeTotal = %d'
                         ',exQty = %d'
                         ' where tID = %d;' %(closePrice,highPrice,lowPrice,  skipItem, secExTotal,dailyID))          
                self.cursor.execute(query)                   
        
            # batch insert secDetail 
            for (secSeq,secTime,secPrice,secLotSize) in calcResult:
                query = ("insert into secDetail (secDailyID,seq,detailTime,price,qty)"
                         "values( %d,%d,\'%s\',%f,%f);" % (dailyID,secSeq,secTime,secPrice,secLotSize))
                self.cursor.execute(query)
            self.cnx.commit()  
        return 0
            
            
            