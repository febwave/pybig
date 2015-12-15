# -*- coding:utf-8 -*-
import os
import sys
import traceback
import multiprocessing as MP
import mongoAccesslib as MA
import re
import codecs
import pyStoreDefine as bsd



########################################################################
class InfoScanner(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, storeAddress,storePort):
        """Constructor"""
        self.nsContainer = set()
        self.reNamespace = re.compile(r"topic=\\([\S]+)\\[\S]+")
        self.storeAddress = storeAddress
        self.storePort = storePort
        self.ma = MA.MongoAccess()
        self.storeConnected = False
        
    def Close(self):
        if(self.storeConnected):
            self.ma.disconnect()
            
    def ClearCache(self):
        self.doConnect()
        self.ma.deleteDatabase(bsd.StoreDefine.DB_NAME)      
        
        
    
    def doConnect(self):
        if(self.storeConnected == False):
            self.ma.connect(self.storeAddress,self.storePort)
            self.storeConnected = True        
    
    def createNSTable(self,tableName):
        # check local cache
        if(tableName in self.nsContainer):
            return
        self.nsContainer.add(tableName)
        # send to mongodb
        self.doConnect()
            
        objDB= self.ma.queryDatabase(bsd.StoreDefine.DB_NAME,True)                           
        objNSListTable = self.ma.queryCollection(objDB,bsd.StoreDefine.TB_NAME_SPACE_LIST,True)  
        objData = dict()
        objData[bsd.StoreDefine.FD_NS_NAME] = tableName
        self.ma.insert(objNSListTable, objData)       
        
    
    def collectTableName(self,fileName):        
        # get first validate line 
        # get namespace
        # return changed table name    
        objFile = codecs.open(fileName,'r','utf-8')
        while(True):
            dataLine = objFile.readline()
            if(len(dataLine) == 0):
                break
            results = self.reNamespace.findall(dataLine)
            if(len(results) > 0):
                orgNS = results[0]
                newNS = orgNS.replace('\\','_')
                self.createNSTable(newNS)
                break
        objFile.close() 
        
    def execTask(self):
        pass
    
    def dispatchTask(self,targetFolder):
        import pyResolve
        pyResolve.execResolve(targetFolder, self.storeAddress, self.storePort)
    
    def Scan(self,parentFolder):
        for fileitem in os.listdir(parentFolder):              
            targetFO = os.path.join(parentFolder,fileitem)     
            if(os.path.isfile(targetFO) == True):
                continue;                    
            for dataFileitem in os.listdir(targetFO):             
                targetFile = os.path.join(targetFO,dataFileitem)     
                if(os.path.isfile(targetFile) == False):
                    continue;                    
                filebasename , fext = os.path.splitext(targetFile);                
                if(filebasename[0] == "."):
                    continue                            
                self.collectTableName(targetFile)
            # all done in current folder
            self.dispatchTask(targetFO)

