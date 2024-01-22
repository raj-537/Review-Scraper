from re import DEBUG
import pymongo
import pandas as pd
import  json

from pymongo import database
from pymongo import collection

class MongoDBManagement:

    def __init__(self, username, password):
        """
        This function require URL for the database
        """
        try:
            self.username = username
            self.password = password
           # self.url = 'mongodb+srv://{username}:{password}@cluster0.9qmvl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'.format(username=self.username, password=self.password)
            self.url = 'mongodb+srv://{username}:{password}@cluster0.h8xwrdy.mongodb.net/?retryWrites=true&w=majority'.format(username=self.username, password=self.password)

        except Exception as e:
            raise Exception(f'(__init__): Something went wrong on initiasation of process'+ str(e))
    

    def getMongoDBClientObject(self):

        """
        This function creates the client object for connection with monogDb database
        """

        try:

            client = pymongo.MongoClient(self.url)
            return client
        except Exception as e:
            raise Exception('(getMongoDBClientObject): Something went wrong'+str(e))

    
    def closeMongoDBconnection(self, mongoClient):

        """
        This function closees the connection of client with database
        provided with mongoClient
        """

        try:
            mongoClient.close()
        except Exception as e:
            raise Exception(f'Something went wrong in closing the Client database connection'+str(e))
    

    def isDatabasePresent(self, db_name):
        """
        This function checks if database is pressent or not.
        :param-> db_name
        """

        try:
            mongoClient = self.getMongoDBClientObject()

            if db_name in mongoClient.list_database_names():
                mongoClient.close()
                return True
            else:
                mongoClient.close()
                return False
        except Exception as e:
            raise Exception('(isDatabasePresent): Failed on checking the data is pressent or not'+str(e))
        
    
    def createDatabase(self, db_name):

        """
        This function creates database.
        :param db_name
        :return
        """

        try:
            database_check_status = self.isDatabasePresent(db_name)

            if not database_check_status:
                mongoClient = self.getMongoDBClientObject()
                database = mongoClient[db_name]
                # mongoClient.close()
                return database,mongoClient
            else:
                mongoClient = self.getMongoDBClientObject()
                database = mongoClient[db_name]
                #mongoClient.close()
                return database,mongoClient
        except Exception as e:
            raise Exception('(createDatabse): Failed on create DATABASE '+str(e))

    
    def dropDatabase(self, db_name):

        """
        This function deletes the database from MongoDb
        :param db_name
        :return
        """

        try:
            mongoClient = self.getMongoDBClientObject()
            if db_name in mongoClient.list_database_names():
                mongoClient.drop_database(db_name)
                mongoClient.close()
                return True
        except Exception as e:
            raise Exception('(dropDatabase): Failed to drop the database dbname'+str(e))

    
    def getDatabase(self, db_name):
        """
        This function returns database or create if not present in list
        :param db_name
        :return
        """

        try:
            mongoClient = self.getMongoDBClientObject()
            #mongoClient.close()
            return mongoClient[db_name],mongoClient
        except Exception as e:
            raise Exception('(getDatabase): Failed to get the database lsit'+str(e))

        

    def getCollection(self, db_name, collection_name):
        """
        This function returns collection in database
        :param collectionName
        :param db_name
        :return
        """

        try:
            
            database, mongoClient = self.getDatabase(db_name)
            return database[collection_name], mongoClient
            
        except Exception as e:
            raise Exception('(getCollection): Failed to get the collection from the database'+str(e))
            
        

    def  isCollectionPresent(self, db_name, collectionName):
        """
        This checks if the collection is present or not present
        :param db_name
        :param collectionName
        :return
        """

        try:
            #database_status = self.isDatabasePresent(db_name)
            # if database_status:
            #     database, mongoClient = self.getDatabase(db_name=db_name)
            #     mongoClient.close()
            #     if collectionName in database.list_collection_names():
            #         return True
            #     else:
            #         return False   
            # else:
            #     return False
            database, mongoClient = self.getDatabase(db_name=db_name)
            
            if collectionName in database.list_collection_names():
                mongoClient.close()
                return True
            else:
                mongoClient.close()
                return False
            
        
        except Exception as e:
            raise Exception('(isCollectionPresent): Failed to get the collection from the database'+str(e))

    

    def createCollectionOrGet(self, db_name, collection_name):
        """
        This function creates the collection in the given database
        :param db_name
        :param collection_name
        :return
        """

        try:
            #collection_status, mongoClient = self.isCollectionPresent(db_name,collection_name)

            # if not collection_status:
            #     database, mongoClient = self.getDatabase(db_name=db_name)
            #     collection = database[collection_name]
            #     return collection, mongoClient
            # else:
            #     return self.getCollection(db_name,collection_name)

            database, mongoClient = self.getDatabase(db_name=db_name)
            collection = database[collection_name]
            return collection, mongoClient
            
        except Exception as e:
            raise Exception(f'(createCollection): Failed to create collection {collection_name}'+str(e))
        
    
    def dropCollection(self, db_name, collection_name):
        """
        This function drops the collection
        :param db_name
        :param collection_name
        :return
        """

        try:
            collection_check_status = self.isCollectionPresent(db_name,collection_name)

            if collection_check_status:
                collection, mongoClient = self.getCollection(db_name=db_name, collection_name=collection_name)
                collection.drop()
                mongoClient.close()
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f'(dropCollection): Failed to drop the collection {collection_name}\n'+str(e))
        
    
    def insertRecord(self, db_name, collection_name, record):
        """
        This function inserts a record to the collection
        :param db_name
        :param collection_name
        :param record
        :return    
        """

        try:
            
            collection, mongoClient  = self.createCollectionOrGet(db_name,collection_name)
            collection.insert_one(record)
            mongoClient.close()
            
            return f'row inserted'
        except Exception as e:
            raise Exception('(insertRecord): Someting went wrong while inserting the record\n'+str(e))

    
    def insertRecords(self, db_name, collection_name, records):
        """
        This function inserts a record to the collection
        :param db_name
        :param collection_name
        :param record
        :return    
        """

        try:
            
            collection,mongoClient  = self.createCollectionOrGet(db_name,collection_name)
            collection.insert_many(records)
            mongoClient.close()
            
            return 'rows inserted'
        except Exception as e:
            raise Exception('(insertRecords): Someting went wrong while inserting the record\n'+str(e))
    

    def findFirstRecord(self, db_name, collection_name, query=None):
        """
        This function returns the first found record
        :param db_name
        :param collection_name
        :param query
        :return
        """

        try:
            if self.isCollectionPresent(db_name=db_name, collectionName=collection_name):
                collection, mongoClient = self.getCollection(db_name=db_name,collection_name=collection_name)

                firstRecord = collection.find_one(query)
                
                mongoClient.close()
                
                return firstRecord
            

        except Exception as e:
            raise Exception('(findFirstRecord): Failed to find the first record.\n'+str(e))

    def findQueryOrAllRecords(self, db_name, collection_name,query=None):
        """
        This function returns the first found record
        :param db_name
        :param collection_name
        :param query
        :return
        """
        try:
            #if self.isCollectionPresent(db_name,collection_name):
            collection, mongoClient = self.getCollection(db_name,collection_name)
            if query is not None:  
                findAllRecords = collection.find(query, {'_id':0})
            else:
                findAllRecords = collection.find({}, {'_id':0})
                
            return findAllRecords, mongoClient
        except Exception as e:
            raise  Exception('(findQueryOrAllRecords): Failed to retrieve the record for the given query\n'+str(e))
    

    def updateOneRecord(self, db_name, collection_name,new_record):

        """
        This function updates the first found record
        :param db_name
        :param collection_name
        :param query
        :return
        """

        try:

            if self.isCollectionPresent(db_name, collection_name):
                collection, mongoClient = self.getCollection(db_name, collection_name)
                previous_record = self.findQueryOrAllRecords(db_name,collection_name,query={})
                updated_record = collection.update_one(previous_record, new_record)
                mongoClient.close()
                return updated_record
        
        except Exception as e:
            raise Exception('(updateOneReocrd): Failed to update the first record\n'+str(e))
        
    
    def updateMultipleRecords(self, db_name, collection_name,query):
        """
        This function updates all the found record
        :param db_name
        :param collection_name
        :param query
        :return
        """

        try:
            
            if self.isCollectionPresent(db_name,collection_name):
                collection,mongoClient = self.getCollection(db_name,collection_name)
                previous_records = self.findQueryOrAllRecords(db_name, collection_name)
                new_records = query
                new = collection.update_many(previous_records, new_records)
                mongoClient.close()
                return new
            
        except Exception as e:
            raise Exception(f'(updateMultipleRecords): Failed to update the multiple records\n'+str(e))
        
    

    def deleteRecord(self, db_name, collection_name, query):
        """
        This function delete the first found record
        :param db_name
        :param collection_name
        :param query
        :return
        """

        try:

            if self.isCollectionPresent(db_name,collection_name):
                collection, mongoClient = self.getCollection(db_name,collection_name)
                collection.delete_one(query)
                mongoClient.close()
                return '1 record deleted'
        except Exception as e:
            raise Exception(f'(deleteRecord): Failed to delete the query record\n'+str(e))
        
    
    def deleteRecords(self, db_name,collection_name, query):

        """
        This function deletes all the found record
        :param db_name
        :param collection_name
        :param query
        :return
        """
        
        try:

            if self.isCollectionPresent(db_name,collection_name):
                collection, mongoClient = self.getCollection(db_name,collection_name)
                collection.delete_many(query)
                mongoClient.close()
                return 'Multiple record deleted'
        except Exception as e:
            raise Exception(f'(deleteRecord): Failed to delete the query records\n'+str(e))
        
    
    def getDataFrameOfCollection(self, db_name, collection_name):
        
        """
        This function return all the record in the database in the pandas.DataFrame object
        :param db_name
        :param collection_name
        :return
        """
        try:
            
            if self.isCollectionPresent(db_name,collection_name):
                allrecords = self.findQueryOrAllRecords(db_name,collection_name)
                dataframe = pd.DataFrame(allrecords)
                return dataframe
        
        except Exception as e:
            raise Exception(f'(getDataFrameOfCollection): Failed to convert records to the query records to Dataframe'+str(e))

    
    def saveDataFrameIntoCollection(self, db_name, collection_name, dataframe):
        """
        This function saves all the record in the dataframe in 
        the pandas.DataFrame object to MongoDb collection
        :param db_name
        :param collection_name
        :return
        """

        try:

            dataframe_dict = json.loads(dataframe.to_json())
            if self.isCollectionPresent(db_name, collection_name):

                self.insertRecords(db_name, collection_name, dataframe_dict)
                return 'Inserted into DataBase'
            else:
                self.createDatabase(db_name)
                self.createCollectionOrGet(db_name,collection_name)
                self.insertRecords(db_name, collection_name,dataframe_dict)
                return 'Inserted'
        
        except Exception as e:
            raise Exception(f'(saveDataFrameIntoCollection): Failed to save dataframe to database\n'+str(e))

    

    def getResultToDisplyOnBrowser(self, db_name, collection_name):

        """
        This function returns the final result to display on browser.
        """

        try:
            response = self.findQueryOrAllRecords(db_name, collection_name)
            result = [i for i in response]
            return result
        except Exception as e:
            raise Exception(f"(getResultToDisplayOnBrowser) - Something went wrong on getting result from database.\n" + str(e))


