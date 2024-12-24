#include <dht11.h>
#include <SoftwareSerial.h>
#include "geolocation.h"
#include <MySQL_Connection.h>
#include <MySQL_Cursor.h>
#include <ESP8266WiFi.h> // Include WiFi library

#define dht_apin 5 // Digital Pin sensor is connected to
dht11 dhtObject;

String apiKey = "90JHFYDCI4U12LZ8";  // Modify the API_KEY with Things_view write API_KEY
SoftwareSerial ser(2, 3); // TX, RX

Geolocation geo;

// Database connection details
char server[] = "HOST_ADDRES or RDS_ENDPOINT";  // Your AWS RDS endpoint
char user[] = "your_db_username";      // MySQL user login username
char password[] = "your_db_password";  // MySQL user login password
char database[] = "weather_data";      // Database name

WiFiClient client; // Create a WiFi client for connection
MySQL_Connection conn((Client *)&client);
MySQL_Cursor* cursor;

void setup() {
    Serial.begin(115200);
    ser.begin(115200);
    ser.println("AT+RST");

    geo.begin(); // Start WiFi connection for geolocation

    // Resolve the AWS RDS domain name to an IP address
    // if (WiFi.hostByName(server, server_addr)) {
    //     Serial.print("Resolved IP address: ");
    //     Serial.println(server_addr);
    // } else {
    //     Serial.println("Failed to resolve server address.");
    //     return;
    // }

    // Connect to the MySQL database
    if (conn.connect(server_addr, 3306, user, password)) {
        Serial.println("Connected to database.");
        cursor = new MySQL_Cursor(&conn);
    } else {
        Serial.println("Connection to database failed.");
    }
}

void loop() {
    dhtObject.read(dht_apin);

    float temperature = dhtObject.temperature;
    float humidity = dhtObject.humidity;
    float lat, lng;
    String device_id = "Device_001"; // Replace with actual device ID

    Serial.print("Temperature (C) = ");
    Serial.println(temperature);

    Serial.print("Humidity (%) = ");
    Serial.println(humidity);

    if (geo.getCoordinates(lat, lng)) {
        Serial.print("Latitude: ");
        Serial.println(lat);
        Serial.print("Longitude: ");
        Serial.println(lng);
    } else {
        Serial.println("Failed to get coordinates.");
        return;
    }

    // Insert data into the SQL database
    char query[256];
    sprintf(query, "INSERT INTO realtime_data (device_id, temperature, humidity, latitude, longitude) VALUES ('%s', '%f', '%f', '%f', '%f')", 
            device_id.c_str(), temperature, humidity, lat, lng);
    
    cursor->execute(query);

    char tempBuf[16];
    char humBuf[16];

    dtostrf(temperature, 4, 1, tempBuf); // Convert temperature to string
    dtostrf(humidity, 4, 1, humBuf);     // Convert humidity to string

    String cmd = "AT+CIPSTART=\"TCP\",\"184.106.153.149\",80";
    ser.println(cmd);
    if (ser.find("Error")) {
        Serial.println("AT+CIPSTART error");
        return;
    }

    // Prepare the GET request with temperature, humidity, latitude, and longitude data
    String getStr = "GET /update?api_key=" + apiKey + "&field1=" + String(tempBuf) + "&field2=" + String(humBuf) + "&field3=" + String(lat) + "&field4=" + String(lng) + "\r\n\r\n";
    cmd = "AT+CIPSEND=";
    cmd += String(getStr.length());
    ser.println(cmd);

    if (ser.find(">")) {
        ser.print(getStr);
    } else {
        ser.println("AT+CIPCLOSE");
        Serial.println("AT+CIPCLOSE");
    }

    delay(2000); // Wait for 2 seconds before taking the next reading
}
