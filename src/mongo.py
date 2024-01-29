"""
This module, `mongo.py`, is designed to handle all MongoDB related operations. It includes functions to connect to a MongoDB database, load data into the database, fetch data from the database, and close the database connection.

The module uses PyMongo, a Python driver for MongoDB, to interact with the database. The database connection parameters such as the MongoDB URI, database name, and collection name are imported from a separate configuration module, `mongo_config.py`.

Functions:
    - `connectToMongo(uri, database_name, collection_name)`: Establishes a connection to the MongoDB database and returns the client, database, and collection.
    - `load(collection, data)`: Inserts the provided data into the specified collection in the database.
    - `fetch(collection, n_records)`: Fetches the most recent n_records from the specified collection in the database.
    - `mongoClose(client)`: Closes the connection to the MongoDB database.
"""
# Imports
import pymongo
from mongo_config import mongo_creds

# Get mondgoDB credentials from config module...Replace with your own database/atlas credentials
mongo_uri = mongo_creds["mongo_uri"]
database_name = mongo_creds["database_name"]
collection_name = mongo_creds["collection_name"]

# Connection method
def connectToMongo(uri=mongo_uri, database_name=database_name, collection_name=collection_name):
    '''
    Connect to DB and return the client, database and collection
    '''
    mongoClient = pymongo.MongoClient(uri)
    database = mongoClient[database_name]
    collection = database[collection_name]
    return mongoClient, database, collection

# Load data in DB
def load(collection, data):
    '''
    Load incoming data in DB and return response message
    '''
    collection.insert_one(data)
    

# Fetch recent data
def fetch(collection, n_records=1):
    '''
    Return the most recent n_records, for visualisation purposes.
    '''
    cursor = collection.find().sort([("_id", pymongo.DESCENDING)]).limit(n_records)
    records = list(cursor)
    return records

# Close the client connection
def mongoClose(client):
    client.close()