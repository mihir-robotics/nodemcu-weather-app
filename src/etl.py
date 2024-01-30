'''
Take input from app.py, validate data and stage it in cache.json. Routinely load into the mongoDB collection.
'''
import json
import os
from mongo import connectToMongo, load, mongoClose

client, database, collection = connectToMongo()

def loadToMongo(sensorDataList:list)-> None:
    '''
    load list of data in MongoDB
    '''
    for record in sensorDataList:
        load(collection, record)


def validateSensorData(sensorData:dict)-> bool:
    '''
    Check if recieved sensor data is valid
    '''
    flag = all(value != 0 and value is not None for value in sensorData.values())
    return flag


def writeToCache(sensorData:dict, limit=100)-> None:
    '''
    Write data to JSON file, if full load onto Mongo
    '''
    # Check if file exists and read it
    if os.path.exists('.\\cache.json'):
        with open('cache.json', 'r') as json_file:
            data = json.load(json_file)
    else:
        data = []

    # Append new sensor data if less than 100 records
    if len(data) < limit:
        data.append(sensorData)

        # Write data back to JSON file
        with open('cache.json', 'w') as json_file:
            json.dump(data, json_file)
    
    else:
        loadToMongo(data)
        # Clear the JSON file
        with open('cache.json', 'w') as json_file:
            json.dump([], json_file)

def fetchLatest(data:dict)->dict:
    '''
    fetch the most recent record from the json cache
    '''
    # Check if file exists and read it
    if os.path.exists('cache.json'):
        with open('cache.json', 'r') as json_file:
            data = json.load(json_file)
    
    return data[-1] if data else {}