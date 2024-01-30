document.addEventListener("DOMContentLoaded", function () {
    
    async function fetchData() {
        const response = await fetch('cache.json');
        const data = await response.json();
        return data;
    }

    // Function to update the temperature chart
    function updateTemperatureChart(temperatureData) {

        // Get the existing Chart instance if it exists
        const existingTempChart = Chart.getChart('temperatureChart');

        // If an existing Chart instance is found, destroy it
        if (existingTempChart) {
            existingTempChart.destroy();
        }
            // Set canvas dimensions
        const canvas = document.getElementById('temperatureChart');
        canvas.width = 650; // Set your desired width
        canvas.height = 250; // Set your desired height
        const temperatureChart = new Chart(document.getElementById('temperatureChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: temperatureData.map((_, index) => index), // Use the index as x-axis labels
                datasets: [{
                    label: 'Temperature',
                    data: temperatureData.map(record => record.temperature),
                    borderColor: 'rgb(255, 99, 132)',
                    pointRadius: 0,
                    borderWidth: 4,
                    fill: false
                }]
            },
            options: {
                responsive: false,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom'
                    }
                }
            }
        });

    }

    // Function to update the humidity chart
    function updateHumidityChart(humidityData) {
        // Get the existing Chart instance if it exists
        const existingHumidChart = Chart.getChart('humidityChart');

        // If an existing Chart instance is found, destroy it
        if (existingHumidChart) {
            existingHumidChart.destroy();
        }
        const canvas = document.getElementById('humidityChart');
        canvas.width = 650; // Set your desired width
        canvas.height = 250; // Set your desired height
        const humidityChart = new Chart(document.getElementById('humidityChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: humidityData.map((_, index) => index), // Use the index as x-axis labels
                datasets: [{
                    label: 'Humidity',
                    data: humidityData.map(record => record.humidity),
                    borderColor: 'rgb(75, 192, 192)',
                    borderWidth: 4,
                    pointRadius: 0,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom'
                    }
                }
            }
        });

    }

    // Function to periodically update charts
    async function updateCharts() {
        const jsonData = await fetchData();

        // Assuming jsonData is an array of records with temperature and humidity fields
        const temperatureData = jsonData.map(record => ({ temperature: record.temperature }));
        const humidityData = jsonData.map(record => ({ humidity: record.humidity }));

        // Update charts
        updateTemperatureChart(temperatureData);
        updateHumidityChart(humidityData);

        // Schedule the next update after a certain interval (e.g., 5 seconds)
        setTimeout(updateCharts, 5000);
    }

    // Function to update sensor data
    function updateSensorData() {
        fetch('/get-data')  // Sensor data endpoint
            .then(response => response.json())
            .then(data => {
                // Update the content of the sensorData div
                document.getElementById('temperature_reading').innerText = `${data.temperature} °C`;
                document.getElementById('humidity_reading').innerText = `${data.humidity} %`;
            })
            .catch(error => {
                console.error('Error fetching sensor data:', error);
            });
    }

    // Call updateSensorData initially
    updateSensorData();
    updateCharts();

    // Update displayed sensor data every 1 seconds (adjust the interval as needed)
    setInterval(updateSensorData, 1000);
});

