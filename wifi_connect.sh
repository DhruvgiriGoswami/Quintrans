#!/bin/bash

# Define your network names and credentials
OFFICE_SSID="AIC Pinnacle"
OFFICE_PSK="AIC-Pinnacle@123"
HOTSPOT_SSID="DhruvH"
HOTSPOT_PSK="vawj2165"

# Function to connect to Wi-Fi
connect_wifi() {
  local ssid=$1
  local psk=$2

  echo "Connecting to $ssid..."
  sudo wpa_cli -i wlan0 remove_network 0
  sudo wpa_cli -i wlan0 add_network
  sudo wpa_cli -i wlan0 set_network 0 ssid "\"$ssid\""
  sudo wpa_cli -i wlan0 set_network 0 psk "\"$psk\""
  sudo wpa_cli -i wlan0 select_network 0
  sudo wpa_cli -i wlan0 enable_network 0
}

# Try to connect to the office Wi-Fi
connect_wifi "$OFFICE_SSID" "$OFFICE_PSK"

# Wait for 10 seconds to check if connected
sleep 10

# Check the connection status
if sudo wpa_cli -i wlan0 status | grep -q "wpa_state=COMPLETED"; then
  echo "Connected to $OFFICE_SSID."
else
  echo "Failed to connect to $OFFICE_SSID. Reverting to hotspot..."

  # Connect to the hotspot
  connect_wifi "$HOTSPOT_SSID" "$HOTSPOT_PSK"
fi

# Optional: Print the current IP address
echo "Current IP Address:"
hostname -I
