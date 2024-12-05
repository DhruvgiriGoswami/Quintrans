#include <SPI.h>
#include <EthernetESP32.h> // Use EthernetESP32

// MAC address settings
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
EthernetServer server(80);

// Pin assignments for L298 driver and actuator
const int dirPin1 = 2;  // Direction pin 1
const int dirPin2 = 15; // Direction pin 2
const int pwmPin = 22;  // PWM pin
const int feedbackPin = 4; // Feedback pin (analog input)

int desiredPosition = 0;  // Desired actuator position in mm
const int maxPosition = 30;  // Maximum position of the actuator in mm
int feedbackValue = 0;
float speedValue = 6.5;  // Default speed in mm/s
const float maxSpeed = 6.5;  // Maximum speed in mm/s

void setup() {
  // Initialize Ethernet module on pin 5
  Ethernet.init(5); 
  Ethernet.begin(mac); // DHCP will assign the IP
  server.begin();
  Serial.begin(115200);

  // Set actuator control pins as output
  pinMode(dirPin1, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  pinMode(pwmPin, OUTPUT);
  pinMode(feedbackPin, INPUT);

  // Wait for Ethernet connection
  while (Ethernet.localIP() == INADDR_NONE) {
    delay(1000);
    Serial.println("Waiting for DHCP...");
  }

  Serial.print("Server is at ");
  Serial.println(Ethernet.localIP());
}

void loop() {
  EthernetClient client = server.available();
  if (client) {
    Serial.println("New client connected");
    String request = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        request += c;  // Accumulate the request string
        Serial.write(c);

        // Check if the request is fully received (end of HTTP request)
        if (c == '\n') {
          // Parse slider value for actuator position (in mm)
          if (request.indexOf("GET /SET_POS?value=") != -1) {
            int posStart = request.indexOf("value=") + 6;
            int posEnd = request.indexOf(' ', posStart);
            desiredPosition = request.substring(posStart, posEnd).toInt();
            Serial.print("Desired Position: ");
            Serial.print(desiredPosition);
            Serial.println(" mm");
          }

          // Parse slider value for speed (in mm/s)
          if (request.indexOf("GET /SET_SPEED?value=") != -1) {
            int speedStart = request.indexOf("value=") + 6;
            int speedEnd = request.indexOf(' ', speedStart);
            speedValue = request.substring(speedStart, speedEnd).toFloat();
            Serial.print("Speed Value: ");
            Serial.print(speedValue);
            Serial.println(" mm/s");
          }

          // Send response to the client
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println("Connection: close");
          client.println();
          client.println("<!DOCTYPE HTML>");
          client.println("<html>");
          client.println("<head><style>");
          client.println("body { font-family: Arial; text-align: center; background-color: #f0f0f0; }");
          client.println(".slider { width: 300px; }");
          client.println("</style></head>");
          client.println("<body>");
          client.println("<h1>ESP32 Linear Actuator Control</h1>");
          client.println("<label for='posSlider'>Set Actuator Position (0 to 30 mm):</label><br>");
          client.println("<input type='range' min='0' max='30' value='15' class='slider' id='posSlider' oninput='updateSlider(this.value)'><br><br>");
          client.println("<p>Position: <span id='sliderValue'>15</span> mm</p>");

          // Slider for speed control (now in mm/s)
          client.println("<label for='speedSlider'>Set Actuator Speed (0 to 6.5 mm/s):</label><br>");
          client.println("<input type='range' min='0' max='6.5' step='0.1' value='6.5' class='slider' id='speedSlider' oninput='updateSpeed(this.value)'><br><br>");
          client.println("<p>Speed: <span id='speedValue'>6.5</span> mm/s</p>");

          client.println("<script>");
          client.println("function updateSlider(val) {");
          client.println("  document.getElementById('sliderValue').innerHTML = val;");
          client.println("  var xhr = new XMLHttpRequest();");
          client.println("  xhr.open('GET', '/SET_POS?value=' + val, true);");
          client.println("  xhr.send();");
          client.println("}");

          // JavaScript for speed slider
          client.println("function updateSpeed(val) {");
          client.println("  document.getElementById('speedValue').innerHTML = val;");
          client.println("  var xhr = new XMLHttpRequest();");
          client.println("  xhr.open('GET', '/SET_SPEED?value=' + val, true);");
          client.println("  xhr.send();");
          client.println("}");
          client.println("</script>");
          client.println("</body>");
          client.println("</html>");

          break; // Break out of the while loop once the request is processed
        }
      }
    }
    delay(1);
    client.stop();
    Serial.println("Client disconnected");
  }

  // Control the actuator based on feedback and desired position
  controlActuator(desiredPosition);
}

// Function to control the actuator based on feedback and desired position
void controlActuator(int desiredPos) {
  // Read the feedback value from the actuator
  feedbackValue = analogRead(feedbackPin);
  int currentPosition = map(feedbackValue, 3970, 70, 0, maxPosition);  // Convert feedback to position in mm

  Serial.print("Current Position: ");
  Serial.print(currentPosition);
  Serial.println(" mm");can I 

  // Map speed value (0 - 6.5 mm/s) to PWM (0 - 255)
  int pwmValue = map(speedValue * 10, 0, maxSpeed * 10, 0, 255);  // Multiply speed by 10 to avoid floating-point issues

  if (currentPosition < desiredPos) {
    // Move actuator forward
    digitalWrite(dirPin1, HIGH);
    digitalWrite(dirPin2, LOW);
    analogWrite(pwmPin, pwmValue);  // Adjust speed based on mapped PWM value
  } else if (currentPosition > desiredPos) {
    // Move actuator backward
    digitalWrite(dirPin1, LOW);
    digitalWrite(dirPin2, HIGH);
    analogWrite(pwmPin, pwmValue);  // Adjust speed based on mapped PWM value
  } else {
    // Stop the actuator when the position is reached
    analogWrite(pwmPin, 0);  // Stop actuator
    Serial.print(feedbackValue);
    Serial.println("Desired position reached.");
  }
}
