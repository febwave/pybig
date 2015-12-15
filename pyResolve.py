# -*- coding:utf-8 -*-
import os
import sys
import re
import codecs
import pyStoreDefine as bsd
import mongoAccesslib as MA


def execResolve(dataFolder,storeAddress,storePort):
    inst = InfoResolve(dataFolder, storeAddress, storePort)
    inst.Resolve()
    inst.Close()

########################################################################
class InfoResolve(object):
    """mutiple process"""

    #----------------------------------------------------------------------
    def __init__(self,dataFolder,storeAddress,storePort):
        """Constructor"""
        self.dataFolder = dataFolder
        self.reTopic = re.compile(r"(\d\d\d\d-\d\d-\d\d\s\d\d:\d\d:\d\d)\s(?:Request|Update)\ssn=0\stopic=\\([\S]+)\\([\S]+)\sfields=(.+)")
        self.reFields = re.compile(r"<F>([^<]+)<D>([^<]*)")        
        self.storeAddress = storeAddress
        self.storePort = storePort
        self.ma = MA.MongoAccess()
        self.storeConnected = False        
        self.objTopicTable = None
    
    def Close(self):
        if(self.storeConnected):
            self.ma.disconnect()        
    
    def doConnect(self):
        if(self.storeConnected == False):
            self.ma.connect(self.storeAddress,self.storePort)
            self.storeConnected = True            
    
    def Resolve(self):
        topicOrgList = list()
        topicList = list()
        topicFilter = dict()
        
        for dataFileitem in os.listdir(self.dataFolder):             
            targetFile = os.path.join(self.dataFolder,dataFileitem)     
            if(os.path.isfile(targetFile) == False):
                continue;                    
            filebasename , fext = os.path.splitext(targetFile);                
            if(filebasename[0] == "."):
                continue                      
            (tableName,topicSet) = self.resolveFile(targetFile)
            topicOrgList.append((tableName,topicSet))
        # filter duplicated items
        for (tableName,topicSet) in topicOrgList:
            if(tableName in  topicFilter):
                currentSet = topicFilter[tableName]
                newSet = currentSet | topicSet
                topicFilter[tableName] =  newSet
            else:
                topicFilter[tableName] = topicSet
                
        for (tableName, topicSet) in topicFilter.items():
            topicList.append((tableName, topicSet))
            
        
        self.updateTopicIndexer(topicList)
        
    def updateTopicIndexer(self,topicList):
        objDB= self.ma.queryDatabase(bsd.StoreDefine.DB_NAME,True)            
        for (tableName,topicSet) in topicList:
            if(self.objTopicTable is None):
                self.objTopicTable = self.ma.queryCollection(objDB,bsd.StoreDefine.TB_TOPIC_LIST,True)   
                self.ma.enableIndex(bsd.StoreDefine.DB_NAME,bsd.StoreDefine.TB_TOPIC_LIST,'_id')
            for itemTopic in topicSet:
                args = dict()
                args[bsd.StoreDefine.FD_TP_NAME] = itemTopic
                args[bsd.StoreDefine.FD_TP_NS] = tableName
                args[bsd.StoreDefine.FD_TP_STATUS] = 0
                self.ma.insert(self.objTopicTable, args)        
                
    
    def resolveFile(self,dataFile):
        recBaseIndexer = 1
        tableName = None
        objNSTable = None
        topicSet = set()
        objFile = codecs.open(dataFile,'r','utf-8')
        self.doConnect()        
        print('scan %s' % dataFile)
        objDB= self.ma.queryDatabase(bsd.StoreDefine.DB_NAME,True)                           
        while(True):
            dataLine = objFile.readline()             
            if(len(dataLine) == 0):
                break
            orgResults = self.reTopic.findall(dataLine)
            if(len(orgResults) < 1):
                continue;        
            orgResult = orgResults[0]
            itemTime = orgResult[0]
            
            itemNS = orgResult[1]
            if(tableName is None):
                tableName = itemNS.replace('\\','_')
                objNSTable = self.ma.queryCollection(objDB,tableName,True)                  
                self.ma.enableIndex(bsd.StoreDefine.DB_NAME,tableName,bsd.StoreDefine.FD_NS_F_TOPIC)
                
            itemTopic = orgResult[2]
            itemOrgFields = orgResult[3]
            
            fds = self.reFields.findall(itemOrgFields)
            
            args = dict()
            args[bsd.StoreDefine.FD_NS_F_TIME] = itemTime
            args[bsd.StoreDefine.FD_NS_F_NS] = itemNS.replace('\\','-')
            args[bsd.StoreDefine.FD_NS_F_TOPIC] = itemTopic            
            args[bsd.StoreDefine.FD_NS_F_SEQ]   = recBaseIndexer
            recBaseIndexer +=1 
            
            for (fdID, fdValue) in fds:
                args[fdID] = fdValue.strip()
            
            self.ma.insert(objNSTable, args)                
                        
            topicSet.add(itemTopic)
            
            
            
        objFile.close()
        
        return (tableName,topicSet)