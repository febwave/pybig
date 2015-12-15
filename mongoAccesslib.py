# -*- coding: UTF-8 -*-

import os
import io
import codecs
import string
import shutil
import datetime

import pymongo


class MongoAccess(object): 
    """"""

    def __init__(self):
        self.mongoClient = None

    def connect(self,address,port):
        self.mongoClient = pymongo.MongoClient(address,port)

    def auth(self,dbName,account,password):
        pass

    def disconnect(self):
        self.mongoClient.close()

    def queryDatabase(self,dbName,isCreated):
        if(isCreated == False):
            if(dbName not in self.mongoClient.database_names()):
                return None                
        return self.mongoClient[dbName]

    def deleteDatabase(self,dbName):
        self.mongoClient.drop_database(dbName)


    def queryCollection(self,objDB, tableName,isCreated):
        if(isCreated == False):
            if(tableName not in objDB.collection_names(False)):
                return None
        return objDB[tableName]

    def enableIndex(self,dbName, tableName,colName):	
        objDB =  self.queryDatabase(dbName,True)
        objTable =  self.queryCollection(objDB,tableName,True)
        objTable.create_index(  colName )


    def insert(self,objTable,objData):
        rec_id =objTable.insert(objData)
        return rec_id

    def delete(self,objTable,objData):
        objTable.remove(objData)

    def queryDocuments(self,objTable,selectSQL,filter = None, sortText = None, batchCount =0,skipItem=0):
        if(sortText is None):
            if(batchCount > 0 and skipItem !=0):
                return objTable.find(selectSQL,filter).limit(batchCount).skip(skipItem)
            elif(batchCount > 0):
                return objTable.find(selectSQL,filter).limit(batchCount)
            else:
                return objTable.find(selectSQL,filter)
        else:
            if(batchCount > 0 and skipItem !=0):
                return objTable.find(selectSQL,filter).sort(sortText).limit(batchCount).skip(skipItem)
            elif(batchCount > 0):
                return objTable.find(selectSQL,filter).sort(sortText).limit(batchCount)
            else:
                return objTable.find(selectSQL,filter).sort(sortText)
            
    def getCount(self,objTable,objData):
        return objTable.find(objData).count()
        
    def updateBySave(self,objTable,changedDocument):        
        return objTable.save(changedDocument)
        
    def update(self,objTable,filter,changedData, multiFlag=True,upsertFlag=False):
        objTable.update(filter,changedData,upsert=upsertFlag,multi=multiFlag)
            
    def getError(self,objDB):
        return objDB.getLastErrorObj()



