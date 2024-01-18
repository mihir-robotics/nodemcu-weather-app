# Imports
from flask import Flask, render_template, request
import asyncio
import mongo # Local

app = Flask(__name__)

sensor_data=""

# Render index.html
@app.route('/')
def index():
    return render_template('index.html', sensor_data=sensor_data)

# Get data for script.js 
@app.route('/get-data', methods=['GET'])
def get_data():
    global data
    return data

# Get data from NodeMCU
@app.route('/send-data', methods=['POST'])
def receive_data():
    global sensor_data
    global data
    data = request.get_json()
    temperature =  data.get('temperature')
    humidity = data.get('humidity')
    
    sensor_data = "Temperature: " + str(temperature) + " | Humidity: " + str(humidity) 
    asyncio.run(update_sensor_data())  # Run the asynchronous update
    return data

# Run async task to get updated sensor values
async def update_sensor_data():
    await asyncio.sleep(1)  # Simulating some asynchronous task
    print(f"Updated sensor data: {sensor_data}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Expose this app
