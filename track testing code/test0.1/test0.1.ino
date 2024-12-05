const int relay1 = 7;
const int relay2 = 4;
const int relay3 = 8;

bool relay1On = false;
bool relay2On = false;
bool relay3On = false;
unsigned long relay3OnTime = 0;

void setup() {
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);
  
  digitalWrite(relay1, LOW);
  digitalWrite(relay2, LOW);
  digitalWrite(relay3, LOW);
  
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    
    if (command == '1') {  // Forward command
      digitalWrite(relay1, HIGH);  // Turn on relay1
      digitalWrite(relay2, HIGH);  // Turn on relay2 (motor direction forward)
      digitalWrite(relay3, HIGH);  // Turn on relay3 if needed
    }
    else if (command == '2') {  // Reverse command
      digitalWrite(relay1, LOW);  // Turn off relay1
      digitalWrite(relay2, LOW);  // Turn off relay2 (reverse motor direction)
      digitalWrite(relay3, HIGH);  // Turn on relay3 if needed for reverse
    }
    else if (command == '0') {  // Stop command
      digitalWrite(relay1, LOW);  // Turn off relay1
      digitalWrite(relay2, LOW);  // Turn off relay2 (stop motor)
      digitalWrite(relay3, LOW);  // Turn off relay3 (stop if running)
    }
  }
}
