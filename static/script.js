document.addEventListener("DOMContentLoaded", function () {
    // Function to update sensor data
    function updateSensorData() {
        fetch('/get-data')  // Assuming this is the endpoint to get the latest sensor data
            .then(response => response.json())
            .then(data => {
                // Update the content of the sensorData div
                //document.getElementById('sensorData').innerText = `Temperature: ${data.temperature} | Humidity: ${data.humidity}`;
                document.getElementById('temperature_reading').innerText = `${data.temperature}°C`;
                document.getElementById('humidity_reading').innerText = `${data.humidity}%`;
                updateThermometer(data.temperature);
            })
            .catch(error => {
                console.error('Error fetching sensor data:', error);
            });
    }
     // Function to update the thermometer height
     function updateThermometer(temperature) {
        const thermometer = document.getElementById('thermometer');
        const redPart = document.getElementById('redPart');

        // Adjust the height of the red part based on the temperature
        const redPartHeight = (temperature / 100) * 150; // Adjust this based on your temperature range
        redPart.style.height = `${redPartHeight}px`;
    }

    // Call updateSensorData initially
    updateSensorData();

    // Update sensor data every 5 seconds (adjust the interval as needed)
    setInterval(updateSensorData, 1000);
});
