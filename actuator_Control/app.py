import socket
import subprocess
from flask import Flask, jsonify, render_template, Response, request
import signal
import os

app = Flask(__name__)

# Function to get the local IP address of the machine
def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

# Function to ping an IP
def ping_ip(ip):
    try:
        # Windows-compatible ping command
        result = subprocess.run(["ping", "-n", "1", "-w", "100", ip],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:  # Ping successful
            # Use arp to get the MAC address
            arp_result = subprocess.run(["arp", "-a", ip],
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = arp_result.stdout

            # Parse the output to find the MAC address
            for line in output.splitlines():
                if ip in line:
                    parts = line.split()
                    if len(parts) >= 2:  # Ensure the line has enough segments
                        mac_address = parts[1]  # MAC address is typically the second column
                        return ip, mac_address
            return ip, None  # No MAC address found in ARP table
    except Exception as e:
        print(f"Error pinging {ip}: {e}")
    return None, None

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/check', methods=['GET'])
def check_actuators():
    def generate():
        local_ip = get_local_ip()
        subnet = ".".join(local_ip.split('.')[:3])  # Extract the subnet (e.g., 192.168.0)
        total_ips = 254  # Total IPs to scan
        scanned_ips = 0  # Count of scanned IPs

        print(f"Scanning subnet: {subnet}.0/24")

        for i in range(1, 255):
            ip = f"{subnet}.{i}"
            ip, mac_address = ping_ip(ip)  # Synchronously ping each IP
            scanned_ips += 1
            if ip:
                if mac_address:
                    yield f"data: Found {ip} (MAC: {mac_address})\n\n"
                else:
                    yield f"data: Found {ip}\n\n"

            # Calculate progress percentage and send it to the client
            progress = (scanned_ips / total_ips) * 100
            yield f"data: Progress {int(progress)}%\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/control/<ip>', methods=['POST'])
def control_actuator(ip):
    action = request.json.get("action", "default")  # Example: "start" or "stop"
    return jsonify({"status": f"Sent '{action}' command to actuator at {ip}"})


# Function to handle server shutdown gracefully
def handle_shutdown_signal(signal, frame):
    print("Shutting down Flask server gracefully...")
    os._exit(0)  # Exit cleanly

# Register signal for graceful shutdown
signal.signal(signal.SIGINT, handle_shutdown_signal)
signal.signal(signal.SIGTERM, handle_shutdown_signal)

if __name__ == '__main__':
    try:
        app.run(debug=True, threaded=False)  # Set threaded to False, no threading used
    except KeyboardInterrupt:
        print("Shutting down server...")
