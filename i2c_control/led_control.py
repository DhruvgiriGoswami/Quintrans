import smbus

# Set up I2C bus and Arduino address
bus = smbus.SMBus(1)  # Use I2C bus 1
arduino_address = 0x08  # Arduino I2C address (8)

# Function to send a command to Arduino
def send_command(command):
    bus.write_byte(arduino_address, ord(command))

# Main loop to get user input and control LEDs
try:
    while True:
        command = input("Enter 1 to turn on LED 1, 2 for LED 2, 3 for LED 3: ")
        if command in ['1', '2', '3']:
            send_command(command)
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

except KeyboardInterrupt:
    pass
