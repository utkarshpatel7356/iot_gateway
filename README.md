# IoT Job Management System

## 📖 Project Overview

This project is a comprehensive **Job Management System** and **IoT Testbed**. It facilitates the remote management of IoT devices (such as Raspberry Pis and nRF dongles) via a centralized server. Users can upload code, schedule jobs, remotely compile and flash firmware, and monitor execution logs in real-time through a web dashboard.

## 🚀 Key Features

* **Dockerized Server Setup:** Easy deployment of frontend, backend, and message queues using Docker Compose.
* **Gateway Management:** Securely connect Raspberry Pi gateways to the server using registration tokens.
* **Device Discovery:** Automatically identify and register connected devices (e.g., nRF dongles) via USB.
* **Remote Job Execution:** Upload source code (e.g., C files), create job groups, and assign them to specific devices.
* **Automated Compilation & Flashing:** The gateway handles downloading, compiling, and flashing the code to the target hardware.
* **Live Monitoring & Logging:** Real-time job status tracking (Preparing, Pending, Running, Completed) and centralized log collection available for download.

---

## 🛠️ Installation & Setup

### 1. Server Side

The server infrastructure (frontend, backend, and message queues) is containerized for ease of use.

1. Navigate to the project directory in your terminal.
2. Build and start the services using Docker Compose:
```bash
docker compose up -d --build

```


*This command builds the project from the server side and gets all services running.*
3. Once the build is complete, access the web interface via **localhost** on your browser.
4. Create an account or log in to access the Dashboard.

### 2. Gateway Side (Raspberry Pi)

The gateway software runs on a device like a Raspberry Pi to manage connected hardware.

1. **Register the Gateway:**
* Run the registration script on the Pi:
```bash
python gateway_registration.py

```


* Enter the **Registration Token** provided by the server admin/dashboard to pair the gateway.


2. **Add Devices:**
* Connect your IoT devices (e.g., nRF dongle) to the gateway.
* Run the device addition script:
```bash
python gateway_add_device.py

```


* Select the device from the list of available USB devices to register it.


3. **Start the Client:**
* Run the gateway client to start polling for jobs:
```bash
python gateway_client.py

```


* The gateway will continuously poll for job notifications from the server.



---

## 💻 Usage Workflow

### 1. File Management

* Navigate to the **Files** section in the dashboard.
* Upload your source code files (e.g., `hello-world.c`) to the server.

### 2. Submitting a Job

* Go to **Submit Jobs** in the Job Management System.
* **Job Group Name:** Enter a name for the job group.
* **Select Device:** Choose an available device (e.g., `device1`).
* **Assign File:** Select the previously uploaded code file.
* Click **Submit Job Group**.

### 3. Execution & Monitoring

* **Download & Compile:** The gateway receives the notification, downloads the job, and compiles the code. The status updates from *Preparing* to *Pending*.
* **Execution:** The scheduler waits for the device to be free. Once free, it flashes the code. The status updates to *Running*.
* **Logging:** As the code executes, the gateway captures logs and sends them to the server.

### 4. Retrieving Results

* Once the job is marked as **Completed**, a download button appears next to the job entry.
* Click the button to download the execution log file (e.g., `job-1-log.txt`) to view the output.

