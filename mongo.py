# deal with all operations w.r.t MongoDB
import pymongo
import mongo_config

# Replace the following with your MongoDB connection details
mongo_uri = mongo_config["mongo_uri"]
database_name = mongo_config["database_name"]
collection_name = mongo_config["collection_name"]

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)

# Access the database
database = client[database_name]
collection = database[collection_name]

# Insert sample data
sample_data = {"temperature": 29, "humidity": 56}
insert_result = collection.insert_one(sample_data)
print(f"Inserted document with _id: {insert_result.inserted_id}")

# Print the list of collections in the database
collections = database.list_collection_names()
print(f"Collections in {database_name}: {collections}")

# Close the connection
client.close()
