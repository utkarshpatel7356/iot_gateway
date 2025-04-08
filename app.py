from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import serial.tools.list_ports
import os
import subprocess
import threading
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests
DB_PATH = "gateway_devices.db"

# Function to run gateway_client.py in a separate process
def run_gateway_client():
    # Get the directory where app.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    client_path = os.path.join(current_dir, "gateway_client.py")
    
    # Run the gateway client script using Python
    subprocess.Popen(["python3", client_path])
    print("Gateway client started in parallel")

# Initialize database
def initialize_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL UNIQUE,
        name TEXT NOT NULL,
        port TEXT NOT NULL,
        description TEXT,
        gateway_id INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

# Device discovery endpoint
@app.route('/api/v1/devices/discover', methods=['GET'])
def discover_devices():
    ports = serial.tools.list_ports.comports()
    devices = [
        {
            "port": port.device,
            "description": port.description,
            "hwid": port.hwid
        } for port in ports
    ]
    return jsonify(devices)

# Device registration endpoint
@app.route('/api/v1/devices', methods=['POST'])
def register_device():
    data = request.get_json()
    
    # Validate required fields (including 'id' since we're using it)
    if not data or 'id' not in data or 'name' not in data or 'port' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    # Use the id from the payload
    device_id = data['id']
    
    # Store in database
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO devices (device_id, name, port, description, gateway_id)
                VALUES (?, ?, ?, ?, ?)
            """, (
                device_id,
                data['name'],
                data['port'],
                data.get('description', ''),
                data.get('gateway_id', 1)
            ))
            conn.commit()
        return jsonify({
            "id": device_id,
            "name": data['name'],
            "port": data['port'],
            "description": data.get('description', ''),
            "gateway_id": data.get('gateway_id', 1),
            "created_at": datetime.now().isoformat()
        })
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


# Get all devices
@app.route('/api/v1/devices', methods=['GET'])
def get_devices():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM devices")
            devices = [dict(row) for row in cursor.fetchall()]
        return jsonify(devices)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# Get device by ID
@app.route('/api/v1/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM devices WHERE device_id = ?", (device_id,))
            device = cursor.fetchone()
        if device:
            return jsonify(dict(device))
        else:
            return jsonify({"error": "Device not found"}), 404
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

if __name__ == '__main__':
    # Start gateway client in parallel before initializing Flask
    run_gateway_client()
    
    # Initialize database and start Flask app
    initialize_database()
    app.run(host='0.0.0.0', port=8000, debug=True)
