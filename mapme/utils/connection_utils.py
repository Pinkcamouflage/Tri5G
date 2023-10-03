import psycopg2
import pymongo
from pymongo import MongoClient
import sqlite3
import pdb

class DatabaseUtils:
    
    @staticmethod
    def establishDatabaseConnection(connection_params):
        try:
            database_type = connection_params['database_type']
            hostname = connection_params['hostname']
            port = connection_params['port']
            database_name = connection_params['database_name']
            username = connection_params['username']
            password = connection_params['password']

            if database_type == 'postgres':
                conn = psycopg2.connect(
                    database=database_name,
                    user=username,
                    password=password,
                    host=hostname,
                    port=port
                )
                return conn
            elif database_type == 'mongodb':
                client = MongoClient(
                    host=hostname,
                    port=int(port),
                    username=username,
                    password=password,
                    authSource=database_name
                )
                return client
            elif database_type == 'sqlite':
                conn = sqlite3.connect(database_name)
                return conn
            else:
                raise ValueError("Unsupported database type")
        except Exception as e:
            raise e

    """
    The following function established a Mongo Client. It then collects the Database Names within the Client,
    as well as the Collections Listed within the given Database.
    """
    @staticmethod
    def databaseInfo(connection_params):
        try:
            mongodb_uri = DatabaseUtils.createMongoUri(connection_params)
            client = MongoClient(mongodb_uri)
            databases = client.list_database_names()
            collection_names = databases.list_collection_names()
            
            collection_keys = {}  # To store collection keys (field names)
            
            for collection_name in collection_names:
                collection = databases.get_collection(collection_name)
                first_document = collection.find_one()
                if first_document:
                    keys = first_document.keys()
                    collection_keys[collection_name] = list(keys)
            
            client.close()
            
            return {'collection_names': collection_names, 'collection_keys': collection_keys}
        except Exception as e:
            raise e
        
    @staticmethod
    def collectionInfo(connection_params,database_name):
        try:
            mongodb_uri = DatabaseUtils.createMongoUri(connection_params)
            client = MongoClient(mongodb_uri)
            database = client[database_name]
            collections = database.list_collection_names()
            collections_info = {}
            for collection in collections:
                curr_collection = database[collection]
                for document in curr_collection.find():
                    keys = document.keys()
                    collections_info[collection] = list(keys)
            
            client.close()
            return collections_info
        except Exception as e:
            raise e

    """
    Different connection types, still to be done, cant be bothered with this ._. Hint--> a bunch of switch cases to find the fitting string syntax
    """
    @staticmethod
    def createMongoUri(connection_params):
        try:
            database_type = connection_params['database_type']
            hostname = connection_params['hostname']
            port = connection_params['port']
            database_name = connection_params['database_name']
            username = connection_params['username']
            password = connection_params['password']
            if database_type == 'mongodb':
                uri = f"mongodb://{hostname}:{port}/{database_name}"
                #uri = f"mongodb://localhost:27017/telekom"
                return uri
            else:
                raise ValueError("Unsupported database type")
        except Exception as e:
            raise e
        
    @staticmethod
    def establish_user_db_connection(request):
        try:
            # Establish a database connection
            connection_params = request.session.get('db_connection_params')
            db_connection = DatabaseUtils.establish_database_connection(connection_params)
            return db_connection
        except Exception as e:
            raise e
        
    @staticmethod
    def close_db_connection(db_connection):
        try:
            # Close the database connection
            db_connection.close()
        except Exception as e:
            raise e
        
    @staticmethod
    def collectionData(collection_name, connection_params):
        try:
            # Establish a MongoDB connection
            mongodb_uri = DatabaseUtils.createMongoUri(connection_params)
            client = MongoClient(mongodb_uri)
            database = client[connection_params['database_name']]
            collection = database[collection_name]
            collection_documents = list(collection.find())
            client.close()
            return collection_documents
        except Exception as e:
            raise e
        

class KPIUtils:
    print()


