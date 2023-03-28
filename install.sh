#!/bin/bash

# Function to check if the script is running with sudo permission
function check_sudo_permission() {
    if [ "$(id -u)" -ne 0 ]; then
        echo "This script must be run with sudo permission."
        exit 1
    fi
}

# Function to start gdm3 service
function start_gdm3_service() {
    sudo systemctl start gdm3.service
    echo "gdm3 service started successfully."
}

# Check if the script is running with sudo permission
check_sudo_permission

# Update package index
sudo apt update

# Install gdm3
sudo apt install gdm3 -y

# Install ubuntu-desktop
sudo apt install ubuntu-desktop -y

# Start gdm3 service
start_gdm3_service
