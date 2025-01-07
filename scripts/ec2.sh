#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Ensure the key file exists
if [ ! -f "$KEY_FILE" ]; then
    echo "Error: Key file not found at $KEY_FILE. Exiting."
    exit 1
fi

# Set key file permissions
chmod 600 "$KEY_FILE"

# Function to connect to the EC2 instance
connect_instance() {
    echo "Connecting to EC2 instance..."
    ssh -i "$KEY_FILE" "$USER@$HOST"
}

# Function to upload files/folders to EC2
upload_to_ec2() {
    # Ask for the directory to copy
    read -p "Enter the full path of the file or folder you want to copy: " source_path

    # Verify if the path exists
    if [ ! -e "$source_path" ]; then
        echo "Error: The path '$source_path' does not exist. Exiting."
        return
    fi

    # Ask for the subdirectory within /home/ec2-user/
    read -p "Enter the subdirectory within /home/ec2-user/ to push to (leave blank for root of /home/ec2-user/): " subdirectory
    destination_path="/home/ec2-user/${subdirectory#/}"  # Ensure no leading slash in subdirectory

    # Copy file or folder to EC2
    echo "Copying '$source_path' to '$USER@$HOST:$destination_path'..."
    scp -i "$KEY_FILE" -r "$source_path" "$USER@$HOST:$destination_path"

    # Check if the command succeeded
    if [ $? -eq 0 ]; then
        echo "Successfully copied '$source_path' to EC2 instance at '$destination_path'."
    else
        echo "Failed to copy '$source_path'. Please check the details and try again."
    fi
}

# Main menu
while true; do
    echo "======================="
    echo "1. Connect to instance"
    echo "2. Upload file/folder"
    echo "3. Exit"
    echo "======================="
    read -p "Choose an option: " choice

    case $choice in
        1)
            connect_instance
            ;;
        2)
            upload_to_ec2
            ;;
        3)
            echo "Exiting. Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
done
