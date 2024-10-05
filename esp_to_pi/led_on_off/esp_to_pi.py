import requests

# Replace with the actual IP address of your ESP8266
ESP8266_IP = "192.168.29.165"

def toggle_led(state):
    try:
        response = requests.get(f"http://{ESP8266_IP}/toggle?state={state}")
        if response.status_code == 200:
            print(response.text)  # Print the response from ESP8266
        else:
            print("Failed to toggle LED. Status code:", response.status_code)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    while True:
        command = input("Enter 'on' to turn on the LED or 'off' to turn it off (or 'exit' to quit): ").strip().lower()
        if command in ["on", "off"]:
            toggle_led(command)
        elif command == "exit":
            break
        else:
            print("Invalid command. Please enter 'on', 'off', or 'exit'.")
