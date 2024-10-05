#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

#define LED_PIN 2  // Use GPIO 2 for the onboard LED (D4 on NodeMCU)

const char* ssid = "Virus";  // Your network SSID
const char* password = "7021318754"; // Your network password

ESP8266WebServer server(80);  // Create a web server on port 80

void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);  // Set the LED pin as an output
    digitalWrite(LED_PIN, LOW); // Ensure the LED is off at startup

    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println(" connected!");
    Serial.println(WiFi.localIP());  // Print the local IP address

    // Define the HTTP GET route for toggling the LED
    server.on("/toggle", HTTP_GET, []() {
        if (server.arg("state") == "on") {
            digitalWrite(LED_PIN, LOW);  // Turn the LED on
            server.send(200, "text/plain", "LED is ON");
        } else {
            digitalWrite(LED_PIN, HIGH);   // Turn the LED off
            server.send(200, "text/plain", "LED is OFF");
        }
    });

    server.begin();  // Start the server
}

void loop() {
    server.handleClient();  // Handle incoming client requests
}
