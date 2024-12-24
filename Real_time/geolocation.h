#ifndef GEOLOCATION_H
#define GEOLOCATION_H

#include <ESP8266WiFi.h> // For ESP8266
//#include <WiFi.h> // For ESP32
#include <ESP8266HTTPClient.h> // For ESP8266
//#include <HTTPClient.h> // For ESP32
#include <ArduinoJson.h>

const char* ssid = "your_wifi_ssid";
const char* password = "your_wifi_password";
const char* apiKey = "your_google_geolocation_api_key"; // Obtain from Google Cloud Console

class Geolocation {
  public:
    void begin() {
      Serial.begin(115200);
      WiFi.begin(ssid, password);
  
      while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
      }
      Serial.println("Connected to WiFi");
    }

    bool getCoordinates(float &lat, float &lng) {
      // Scan for nearby WiFi networks
      int numNetworks = WiFi.scanNetworks();
      if (numNetworks == 0) {
        Serial.println("No WiFi networks found.");
        return false;
      }

      // Prepare JSON data for the API request
      StaticJsonDocument<512> doc;
      JsonArray wifiAccessPoints = doc.createNestedArray("wifiAccessPoints");

      for (int i = 0; i < numNetworks; i++) {
        JsonObject wifiObject = wifiAccessPoints.createNestedObject();
        wifiObject["macAddress"] = WiFi.BSSIDstr(i);
        wifiObject["signalStrength"] = WiFi.RSSI(i);
        wifiObject["channel"] = WiFi.channel(i);
      }

      // Convert JSON data to a string
      String jsonString;
      serializeJson(doc, jsonString);

      // Send the HTTP POST request
      HTTPClient http;
      http.begin("https://www.googleapis.com/geolocation/v1/geolocate?key=" + String(apiKey));
      http.addHeader("Content-Type", "application/json");

      int httpResponseCode = http.POST(jsonString);

      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.println("HTTP Response code: " + String(httpResponseCode));
        Serial.println("Location data: " + response);
        
        // Parse the JSON response
        StaticJsonDocument<256> responseDoc;
        DeserializationError error = deserializeJson(responseDoc, response);

        if (!error) {
          lat = responseDoc["location"]["lat"];
          lng = responseDoc["location"]["lng"];
          return true;
        } else {
          Serial.println("Failed to parse JSON response.");
          return false;
        }
      } else {
        Serial.println("Error on sending POST: " + String(httpResponseCode));
        return false;
      }

      http.end();
    }
};

#endif
