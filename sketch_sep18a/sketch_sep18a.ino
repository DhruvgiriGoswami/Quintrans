#include <Wire.h>

const int ledPin = 9; // Pin where the LED is connected

void setup() {
  Wire.begin(8); // Set the I2C address of the Arduino (8)
  Wire.onReceive(receiveEvent); // Register the receive event
  pinMode(ledPin, OUTPUT); // Set LED pin as output
}

void loop() {
  // Main loop does nothing, waiting for I2C commands
}

void receiveEvent(int howMany) {
  while (Wire.available()) {
    char c = Wire.read(); // Read the incoming byte
    if (c == '1') {
      digitalWrite(ledPin, HIGH); // Turn LED ON
    } else if (c == '0') {
      digitalWrite(ledPin, LOW); // Turn LED OFF
    }
  }
}
