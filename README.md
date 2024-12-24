# Real-Time-Weather-Forecasting-and-Trend-Analysis-System

# Global Weather Forecasting System and Climate Analysis Platform

## Overview

This project is a **Global Weather Forecasting System and Climate Analysis Platform** designed to collect, process, and analyze weather data in real time. It integrates sensor data with geolocation information and uploads the data to an AWS RDS database and ThingSpeak for further processing and visualization. This platform is part of a larger system aimed at forecasting weather patterns and analyzing climate trends.

## Features

<ul>
  <li><strong>Real-Time Data Collection:</strong> Collects temperature, humidity, and geolocation data from sensors.</li>
  <li><strong>Database Integration:</strong> Stores collected data into an AWS RDS MySQL database for persistent storage and future analysis.</li>
  <li><strong>ThingSpeak Integration:</strong> Uploads real-time weather data to ThingSpeak for visualization and monitoring.</li>
  <li><strong>Geolocation Services:</strong> Utilizes Google Geolocation API to obtain accurate coordinates based on nearby Wi-Fi access points.</li>
  <li><strong>Modular Design:</strong> Easily extendable and adaptable to different hardware setups and data processing needs.</li>
</ul>

## Hardware Requirements

<ul>
  <li>ESP8266 or ESP32 Microcontroller</li>
  <li>DHT11 Temperature and Humidity Sensor</li>
  <li>Wi-Fi Access</li>
  <li>AWS RDS Instance (MySQL Database)</li>
  <li>Google Cloud Account for Geolocation API</li>
  <li>ThingSpeak Account</li>
</ul>

## Software Requirements

<ul>
  <li>Arduino IDE</li>
  <li>MySQL Connector for Arduino</li>
  <li>ArduinoJson Library</li>
  <li>ESP8266WiFi Library (or WiFi Library for ESP32)</li>
  <li>ESP8266HTTPClient Library (or HTTPClient Library for ESP32)</li>
</ul>

## Setup Instructions

<ol>
  </li>
  <li><strong>Configure the Project:</strong>
    <ul>
      <li>Open the project in Arduino IDE.</li>
      <li>Replace the placeholders in the code with your actual credentials:
        <ul>
          <li>Wi-Fi SSID and Password</li>
          <li>Google Geolocation API Key</li>
          <li>AWS RDS MySQL database endpoint, username, and password</li>
          <li>ThingSpeak API Key</li>
        </ul>
      </li>
    </ul>
  </li>
  <li><strong>Upload the Code:</strong>
    <ul>
      <li>Connect your ESP8266/ESP32 microcontroller to your computer.</li>
      <li>Select the correct board and port in Arduino IDE.</li>
      <li>Upload the code to the microcontroller.</li>
    </ul>
  </li>
  <li><strong>Run the System:</strong>
    <ul>
      <li>Once the code is uploaded, the system will start collecting data from the DHT11 sensor.</li>
      <li>The geolocation data will be fetched using the Google Geolocation API.</li>
      <li>The collected data will be uploaded to the AWS RDS database and ThingSpeak for storage and visualization.</li>
    </ul>
  </li>
</ol>

## Code Structure

<ul>
  <li><strong>geolocation.h:</strong> Handles the Wi-Fi connection and geolocation data fetching using Google Geolocation API.</li>
  <li><strong>main.ino:</strong> The main file that integrates all components, collects sensor data, and manages data uploads to the database and ThingSpeak.</li>
  <li><strong>config.h:</strong> Contains configuration parameters like API keys, database credentials, etc. (Optional, depending on your setup).</li>
</ul>

## AWS RDS Database Schema

<ul>
  <li><strong>Table:</strong> <code>weather</code>
    <ul>
      <li><code>device_id:</code> VARCHAR, ID of the device collecting data</li>
      <li><code>temperature:</code> FLOAT, temperature reading</li>
      <li><code>humidity:</code> FLOAT, humidity reading</li>
      <li><code>latitude:</code> FLOAT, latitude of the data point</li>
      <li><code>longitude:</code> FLOAT, longitude of the data point</li>
      <li><code>timestamp:</code> TIMESTAMP, the time the data was recorded</li>
    </ul>
  </li>
</ul>

## Future Enhancements

<ul>
  <li>Integration of additional sensors (e.g., wind speed, pressure).</li>
  <li>Implementation of predictive analytics and weather forecasting models.</li>
  <li>Development of a web-based dashboard for real-time monitoring and data visualization.</li>
  <li>Expansion of the system to support multiple devices and locations.</li>
</ul>

<!--
## Contributing

Contributions are welcome! Please fork this repository and submit a pull request to contribute to the project.

## License

This project is licensed under the In License - see the <a href="LICENSE">LICENSE</a> file for details.
-->
