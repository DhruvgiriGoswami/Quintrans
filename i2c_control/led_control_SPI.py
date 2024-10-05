import spidev
import time

# Set up SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0
spi.max_speed_hz = 50000  # Set clock speed (adjust as needed)

# Function to send a command over SPI
def send_command(command):
    spi.xfer([ord(command)])  # Send the command as a byte over SPI

# Main loop to control LEDs via SPI
try:
    while True:
        command = input("Enter 1 to turn on LED 1, 2 for LED 2, 3 for LED 3: ")
        if command in ['1', '2', '3']:
            send_command(command)
        else:
            print("Invalid input. Please enter 1, 2, or 3.")
except KeyboardInterrupt:
    pass

spi.close()  # Close SPI connection when done
