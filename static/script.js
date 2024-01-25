document.addEventListener("DOMContentLoaded", function () {
    // Function to update sensor data
    function updateSensorData() {
        fetch('/get-data')  // Sensor data endpoint
            .then(response => response.json())
            .then(data => {
                // Update the content of the sensorData div
                document.getElementById('temperature_reading').innerText = `${data.temperature}°C`;
                document.getElementById('humidity_reading').innerText = `${data.humidity}%`;
            })
            .catch(error => {
                console.error('Error fetching sensor data:', error);
            });
    }

    // Call updateSensorData initially
    updateSensorData();

    // Update displayed sensor data every 1 seconds (adjust the interval as needed)
    setInterval(updateSensorData, 1000);
});
