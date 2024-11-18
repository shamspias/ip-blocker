# IP Blocker

A simple Python script to manage IP blocking on an Ubuntu server using UFW (Uncomplicated Firewall). This tool allows you to add, remove, check, and list IP addresses in your blocklist, ensuring that unwanted IPs are effectively blocked from accessing your machine.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Add an IP to the Blocklist](#add-an-ip-to-the-blocklist)
  - [Remove an IP from the Blocklist](#remove-an-ip-from-the-blocklist)
  - [Check if an IP is in the Blocklist](#check-if-an-ip-is-in-the-blocklist)
  - [List All Blocked IPs](#list-all-blocked-ips)
- [How It Works](#how-it-works)
- [Notes](#notes)
- [Contributing](#contributing)
- [License](#license)

## Features

- **System-Level Blocking:** Blocks IPs at the Ubuntu firewall level using UFW.
- **Persistent Blocklist:** Stores blocked IPs in a JSON file for persistence.
- **Easy Management:** Simple commands to add, remove, check, and list IPs.
- **Validation:** Validates IP addresses before blocking or unblocking.
- **Logging:** Actions and errors are logged for auditing purposes.

## Requirements

- **Python 3.11**
- **Ubuntu Server**
- **UFW (Uncomplicated Firewall)**

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/shamspias/ip-blocker.git
   cd ip-blocker
   ```

2. **Install UFW**

   Ensure that UFW is installed and enabled on your Ubuntu server.

   ```bash
   sudo apt-get update
   sudo apt-get install ufw
   sudo ufw enable
   ```

3. **Check UFW Status**

   Verify that UFW is active.

   ```bash
   sudo ufw status verbose
   ```

4. **Set Permissions**

   Make the script executable.

   ```bash
   chmod +x ip_blocker.py
   ```

5. **Install Dependencies**

   The script uses only standard library modules, so no additional packages are required. If you plan to extend the script, you can list new dependencies in `requirements.txt`.

## Usage

**Note:** When adding or removing IPs, you must run the script with root privileges (`sudo`) because it modifies system firewall rules.

### Add an IP to the Blocklist

Blocks an IP address by adding it to UFW's deny rules and the persistent blocklist.

```bash
sudo python3 ip_blocker.py add <IP_ADDRESS>
```

**Example:**

```bash
sudo python3 ip_blocker.py add 192.168.1.100
```

### Remove an IP from the Blocklist

Unblocks an IP address by removing it from UFW's deny rules and the persistent blocklist.

```bash
sudo python3 ip_blocker.py remove <IP_ADDRESS>
```

**Example:**

```bash
sudo python3 ip_blocker.py remove 192.168.1.100
```

### Check if an IP is in the Blocklist

Checks whether an IP address is currently in the blocklist.

```bash
python3 ip_blocker.py check <IP_ADDRESS>
```

**Example:**

```bash
python3 ip_blocker.py check 192.168.1.100
```

### List All Blocked IPs

Displays all IP addresses currently in the blocklist.

```bash
python3 ip_blocker.py list
```

## How It Works

The `ip_blocker.py` script uses UFW to manage firewall rules at the system level. When you add an IP, it:

1. **Validates the IP Address**

   Ensures the IP address is correctly formatted using Python's `ipaddress` module.

2. **Updates the Blocklist**

   Adds the IP to `blocklist.json` for persistent storage.

3. **Modifies UFW Rules**

   Executes `ufw deny from <IP>` to block all incoming traffic from the specified IP address.

4. **System-Level Blocking**

   The IP is blocked at the firewall level, preventing any requests from reaching your machine.

**Removing an IP** reverses these steps, ensuring the IP is no longer blocked.

## Notes

- **Root Privileges**

  - Adding or removing IPs requires root access.
  - Always run these commands with `sudo`.

- **Logging**

  - Actions and errors are logged to `ip_blocker.log`.
  - Check this file for detailed logs.

- **Blocklist File**

  - The blocklist is stored in `blocklist.json`.
  - This file should be in the same directory as the script.

- **Safety Precautions**

  - Be careful not to block your own IP, especially if accessing the server remotely.
  - Double-check IP addresses before adding them to the blocklist.

- **Firewall Rules Persistence**

  - UFW rules persist across reboots.
  - The blocklist ensures that your blocked IPs are maintained.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the Repository**

   ```bash
   git clone https://github.com/shamspias/ip-blocker.git
   ```

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Your Changes**

   ```bash
   git commit -am 'Add new feature'
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**By using this script, any IP address you add will be effectively blocked at the system level on your Ubuntu machine. The script modifies UFW firewall rules to ensure that the IPs are genuinely blocked from making any requests to your machine.**

---