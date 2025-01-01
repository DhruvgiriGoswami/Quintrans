import socket
import subprocess
from flask import Flask, jsonify, render_template, Response, request
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to get the local IP address of the machine
def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    logger.info(f"Local IP address: {local_ip}")
    return local_ip

# Function to ping an IP and retrieve its MAC address
def ping_ip(ip):
    try:
        # Windows-compatible ping command
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "100", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode == 0:  # Ping successful
            # Use arp to get the MAC address
            arp_result = subprocess.run(
                ["arp", "-a", ip],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            output = arp_result.stdout
            for line in output.splitlines():
                if ip in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        mac_address = parts[1]  # Typically the second column
                        return ip, mac_address
            return ip, None
    except Exception as e:
        logger.error(f"Error pinging {ip}: {e}")
    return None, None

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/check', methods=['GET'])
def check_actuators():
    def generate():
        local_ip = get_local_ip()
        subnet = ".".join(local_ip.split('.')[:3])  # Extract the subnet (e.g., 192.168.0)
        logger.info(f"Scanning subnet: {subnet}.0/24")
        total_ips = 254
        scanned_ips = 0

        # Scan each IP address in the subnet without threading
        for i in range(1, 255):
            ip = f"{subnet}.{i}"
            ip, mac_address = ping_ip(ip)
            if ip:
                scanned_ips += 1
                logger.info(f"Pinged IP {ip}")
                if mac_address:
                    yield f"data: Found {ip} (MAC: {mac_address})\n\n"
                else:
                    yield f"data: Found {ip}\n\n"

            # Logging the current progress
            logger.info(f"Scanned {scanned_ips}/{total_ips} IPs")
            progress = (scanned_ips / total_ips) * 100
            yield f"data: Progress {int(progress)}%\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/control/<ip>', methods=['POST'])
def control_actuator(ip):
    action = request.json.get("action", "default")
    logger.info(f"Received action '{action}' for IP {ip}")
    return jsonify({"status": f"Sent '{action}' command to actuator at {ip}"})

if __name__ == '__main__':
    try:
        app.run(debug=True, threaded=False)
    except KeyboardInterrupt:
        logger.info("Shutting down server gracefully...")
