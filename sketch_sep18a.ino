// Define sensor pins
const int sensor1 = A0;
const int sensor2 = A1;
const int sensor3 = A2;

// Define relay pins
const int relay1 = 7;
const int relay2 = 4;
const int relay3 = 8;

bool relay1On = false;
bool relay2On = false;
bool relay3On = false;
unsigned long relay3OnTime = 0;

void setup() {
  // Set relay pins as outputs
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);

  // Initialize relays to HIGH (not triggered)
  digitalWrite(relay1, HIGH);
  digitalWrite(relay2, HIGH);
  digitalWrite(relay3, HIGH);
}

void loop() {
  // Read sensor values
  float sensorValue1 = analogRead(sensor1) * (5.0 / 1023.0);
  float sensorValue2 = analogRead(sensor2) * (5.0 / 1023.0);
  float sensorValue3 = analogRead(sensor3) * (5.0 / 1023.0);

  // Check if Sensor 1 is detected
  if (sensorValue1 >= 4.0) {
    if (!relay1On) {
      digitalWrite(relay1, LOW);  // Turn ON Relay 1
      relay1On = true;
    }
  } else if (relay1On) {
    // Sensor 1 not detected
    // Relay 1 stays ON until Sensor 2 is detected
  }

  // Check if Sensor 2 is detected
  if (sensorValue2 >= 4.0) {
    if (relay1On) {
      digitalWrite(relay1, HIGH); // Turn OFF Relay 1
      relay1On = false;
    }
    if (!relay2On) {
      digitalWrite(relay2, LOW);  // Turn ON Relay 2
      relay2On = true;
    }
  } else if (relay2On) {
    // Sensor 2 not detected
    // Relay 2 stays ON until Sensor 3 is detected
  }

  // Check if Sensor 3 is detected
  if (sensorValue3 >= 4.0) {
    if (!relay3On) {
      digitalWrite(relay2, HIGH); // Turn OFF Relay 2
      relay2On = false;
      digitalWrite(relay3, LOW);  // Turn ON Relay 3
      relay3On = true;
      relay3OnTime = millis();    // Record the time when Relay 3 was turned ON
    }
  }

  // Turn OFF Relay 3 after 1 second
  if (relay3On && (millis() - relay3OnTime >= 1000)) {
    digitalWrite(relay3, HIGH); // Turn OFF Relay 3
    relay3On = false;
  }

  delay(100); // Small delay to avoid rapid switching
}
