#!/usr/bin/env python3

"""
IP Blocker Script

This script allows you to manage IP blocking on an Ubuntu server using UFW (Uncomplicated Firewall).
You can add, remove, check, and list blocked IP addresses.

Usage:
    sudo python3 ip_blocker.py add <IP_ADDRESS>
    sudo python3 ip_blocker.py remove <IP_ADDRESS>
    python3 ip_blocker.py check <IP_ADDRESS>
    python3 ip_blocker.py list
"""

import argparse
import ipaddress
import json
import logging
import os
import subprocess
import sys
from typing import List

# Constants
BLOCKLIST_FILE = 'blocklist.json'
LOG_FILE = 'ip_blocker.log'


class IPBlocker:
    """Class to manage IP blocking using UFW."""

    def __init__(self, blocklist_file: str = BLOCKLIST_FILE):
        self.blocklist_file = blocklist_file
        self.blocklist = self.load_blocklist()
        self.setup_logging()

    def setup_logging(self) -> None:
        """Configure logging for the application."""
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def load_blocklist(self) -> List[str]:
        """Load the blocklist from the JSON file."""
        try:
            with open(self.blocklist_file, 'r') as f:
                blocklist = json.load(f)
                logging.debug("Blocklist loaded successfully.")
                return blocklist
        except FileNotFoundError:
            logging.debug("Blocklist file not found. Starting with an empty blocklist.")
            return []

    def save_blocklist(self) -> None:
        """Save the blocklist to the JSON file."""
        with open(self.blocklist_file, 'w') as f:
            json.dump(self.blocklist, f, indent=4)
        logging.debug("Blocklist saved successfully.")

    def check_root(self) -> None:
        """Check if the script is run as root."""
        if os.geteuid() != 0:
            logging.error("This script must be run as root. Please use sudo.")
            sys.exit("This script must be run as root. Please use sudo.")

    def validate_ip(self, ip: str) -> bool:
        """Validate the IP address format."""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            logging.error(f"Invalid IP address: {ip}")
            print(f"Invalid IP address: {ip}")
            return False

    def add_ip(self, ip: str) -> None:
        """Add an IP to the blocklist and block it using UFW."""
        if not self.validate_ip(ip):
            return

        if ip in self.blocklist:
            logging.info(f"IP {ip} is already in the blocklist.")
            print(f"IP {ip} is already in the blocklist.")
            return

        self.blocklist.append(ip)
        self.save_blocklist()

        # Block the IP using UFW
        cmd = ["ufw", "deny", "from", ip]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logging.info(f"IP {ip} has been blocked via UFW.")
            print(f"IP {ip} has been blocked.")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode().strip()
            logging.error(f"Failed to block IP {ip}: {error_msg}")
            print(f"Failed to block IP {ip}: {error_msg}")

    def remove_ip(self, ip: str) -> None:
        """Remove an IP from the blocklist and unblock it using UFW."""
        if not self.validate_ip(ip):
            return

        if ip not in self.blocklist:
            logging.info(f"IP {ip} is not in the blocklist.")
            print(f"IP {ip} is not in the blocklist.")
            return

        self.blocklist.remove(ip)
        self.save_blocklist()

        # Unblock the IP using UFW
        cmd = ["ufw", "--force", "delete", "deny", "from", ip]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logging.info(f"IP {ip} has been unblocked via UFW.")
            print(f"IP {ip} has been unblocked.")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode().strip()
            logging.error(f"Failed to unblock IP {ip}: {error_msg}")
            print(f"Failed to unblock IP {ip}: {error_msg}")

    def check_ip(self, ip: str) -> None:
        """Check if an IP is in the blocklist."""
        if not self.validate_ip(ip):
            return

        if ip in self.blocklist:
            logging.info(f"IP {ip} is in the blocklist.")
            print(f"IP {ip} is in the blocklist.")
        else:
            logging.info(f"IP {ip} is not in the blocklist.")
            print(f"IP {ip} is not in the blocklist.")

    def list_ips(self) -> None:
        """List all IPs in the blocklist."""
        if self.blocklist:
            logging.info("Listing all blocked IPs.")
            print("Blocked IPs:")
            for ip in self.blocklist:
                print(ip)
        else:
            logging.info("Blocklist is empty.")
            print("Blocklist is empty.")


def main():
    parser = argparse.ArgumentParser(description='IP Blocker Script')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add command
    parser_add = subparsers.add_parser('add', help='Add IP to blocklist')
    parser_add.add_argument('ip', help='IP address to block')

    # Remove command
    parser_remove = subparsers.add_parser('remove', help='Remove IP from blocklist')
    parser_remove.add_argument('ip', help='IP address to unblock')

    # Check command
    parser_check = subparsers.add_parser('check', help='Check if IP is in blocklist')
    parser_check.add_argument('ip', help='IP address to check')

    # List command
    subparsers.add_parser('list', help='List all blocked IPs')

    args = parser.parse_args()

    ip_blocker = IPBlocker()

    if args.command == 'add':
        ip_blocker.check_root()
        ip_blocker.add_ip(args.ip)
    elif args.command == 'remove':
        ip_blocker.check_root()
        ip_blocker.remove_ip(args.ip)
    elif args.command == 'check':
        ip_blocker.check_ip(args.ip)
    elif args.command == 'list':
        ip_blocker.list_ips()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
