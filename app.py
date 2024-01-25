"""
Flask Application

This Flask application provides endpoints to interact with IoT sensor data. It includes routes to render the
index page with current sensor data, retrieve data for script.js, and receive data from a NodeMCU device. 
It also calls the mongodb services to fetch/load sensor data.

Endpoints:
    - `/`: Renders the index page with current sensor data.
    - `/get-data`: Endpoint to retrieve data for script.js.
    - `/send-data`: Endpoint to receive data from NodeMCU.

Functions:
    - `index()`: Renders the index page with current sensor data.
    - `get_data()`: Endpoint to retrieve data for script.js.
    - `receive_data()`: Endpoint to receive data from NodeMCU.
    - `update_sensor_data()`: Asynchronously updates sensor data.

Dependencies:
    - Flask: Web framework for creating the web application.
    - asyncio: Asynchronous programming library for handling asynchronous tasks.
    - mongo: Local module, handles mongodb operations.
"""

# Imports
from flask import Flask, render_template, request
from asyncio import run, sleep
from mongo import connectToMongo, load, mongoClose
from atexit import register
    
sensor_data=""
global data
data = {'temperature': 0, 'humidity': 0}

app = Flask(__name__)

client, database, collection = connectToMongo()

# Close connection to MongoDB when Flask app is terminated
register(mongoClose, client)

# Render index.html
@app.route('/')
def index():
    return render_template('index.html', sensor_data=sensor_data)

# Get data for script.js 
@app.route('/get-data', methods=['GET'])
def get_data():
    
    return data

# Get data from NodeMCU
@app.route('/send-data', methods=['POST'])
def receive_data():
    global sensor_data
    data = request.get_json()
    run(update_sensor_data())
    return data

# Run async task to get updated sensor values
async def update_sensor_data():
    await sleep(1)  # Simulating some asynchronous task
    load(collection, data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Expose this app to local network.
