/*
esp.ino

This program connects to a WiFi network, reads temperature and humidity data from a DHT sensor,
encodes the data into JSON format, and sends it to a Flask web application using HTTP POST requests.

*/
#include <ESP8266WiFi.h>       // For connecting to WiFi
#include <ESP8266HTTPClient.h> // For HTTP Client and communication
#include <DHT.h>               // Sensor Library for DHT11 temperature and humidity.
#include <ArduinoJson.h>       // JSON library (v 6.18.0) Future versions might break this...
#include "config.h"            // Local library to get SSID, PASSWORD, HOST variables for network

#define BAUD_RATE 115200 // Define baud rate for serial communication
#define DHTPIN D3        // Define the pin where the DHT sensor is connected
#define DHTTYPE DHT11    // Define the type of DHT sensor, in this case it is DHT11

// Replace with your network credentials
const char *ssid = SSID;
const char *password = PASSWORD;
const char *host = HOST; // Replace with your Flask app's IP or domain; 127... is the dev server default

const int serverPort = 5000;          // Port of Flask app
const String endpoint = "/send-data"; // End point for sending data

WiFiClient client; // Client object for HTTP communication

DHT dht(DHTPIN, DHTTYPE); // Create DHT sensor object

const int DELAY_MS = 100; // Set delay between messages (ms)

const int JSON_SIZE_BYTES = 1024; // Define byte size for JSON message

// Setup()
void setup()
{
    Serial.begin(BAUD_RATE);
    delay(10);

    WiFi.begin(ssid, password); // Connect to WiFi
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("WiFi connected");

    dht.begin(); // Start DHT sensor
}

// Loop()
void loop()
{
    send_JSON(get_data_JSON()); // Send sensor data in JSON format
    delay(DELAY_MS);
}

// Function to obtain sensor values and return the json document
DynamicJsonDocument get_data_JSON()
{
    float temperature = dht.readTemperature();    // Get temperature value
    float humidity = dht.readHumidity();          // Get humidity value
    DynamicJsonDocument jsonDoc(JSON_SIZE_BYTES); // Define jsonDoc

    jsonDoc["temperature"] = temperature; // Add temperature and humidity to the JSON document
    jsonDoc["humidity"] = humidity;

    return jsonDoc;
}

// Send JSON data to Flask app
void send_JSON(DynamicJsonDocument jsonData)
{
    String jsonString;
    serializeJson(jsonData, jsonString); // Serialize the JSON document to a string

    HTTPClient http;
    String url = "http://" + String(host) + ":" + String(serverPort) + endpoint;

    http.begin(client, url);                            // Send HTTP POST request
    http.addHeader("Content-Type", "application/json"); // Define content-type of message

    int httpResponseCode = http.POST(jsonString);
    String payload = http.getString();

    String message = "Sent:" + jsonString + " to -> " + url + " | Payload is: " + payload + " | HTTP Code: " + String(httpResponseCode);
    Serial.println(message); // Log message about HTTP request

    http.end(); // Free resources
}