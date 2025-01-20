#!/bin/bash

# Load .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found!"
    exit 1
fi

if [ ! -f "$KEY_FILE" ]; then
    echo "Error: Key file not found at $KEY_FILE. Exiting."
    exit 1
fi

chmod 600 "$KEY_FILE"

print_smiley() {
    echo -ne "🙂 Connecting...\r"
    sleep 0.5
}

# EC2 instance
connect_instance() {
    print_smiley
    echo "Connecting to EC2 instance..."
    ssh -i "$KEY_FILE" "$USER@$HOST"
    exit 0 
}

# upload files/folders to EC2
upload_to_ec2() {
    read -p "Enter the full path of the file or folder you want to copy: " source_path

    if [ ! -e "$source_path" ]; then
        echo "Error: The path '$source_path' does not exist. Exiting."
        return
    fi
    read -p "Enter the subdirectory within /home/ec2-user/ to push to (leave blank for root of /home/ec2-user/): " subdirectory
    destination_path="/home/ec2-user/${subdirectory#/}"  

    print_smiley
    echo "Copying '$source_path' to '$USER@$HOST:$destination_path'..."
    scp -i "$KEY_FILE" -r "$source_path" "$USER@$HOST:$destination_path"

    if [ $? -eq 0 ]; then
        echo "Successfully copied '$source_path' to EC2 instance at '$destination_path'."
    else
        echo "Failed to copy '$source_path'. Please check the details and try again."
    fi
}

# PostgreSQL database
connect_database() {
    if [ -z "$DATABASE" ]; then
        echo "DATABASE_URL is not set in the environment."
        return
    fi

    print_smiley
    echo "Connecting to PostgreSQL database..."
    psql "$DATABASE"
    exit 0 
}

# Main menu
while true; do
    echo "======================="
    echo "1. Connect to EC2 instance"
    echo "2. Upload file/folder to EC2"
    echo "3. Connect to PostgreSQL database"
    echo "4. Exit"
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
            connect_database
            ;;
        4)
            echo "🎉 Happy Coding! 🎉"
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
done
