#!/bin/bash
set -e

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip3 could not be found, installing..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Install Python dependencies
pip3 install -r /usr/local/bin/audio_swop/requirements.txt

# Copy desktop entry
sudo cp /usr/local/bin/audio_swop/audio_swop.desktop /usr/share/applications/
sudo chmod 644 /usr/share/applications/audio_swop.desktop

# Ensure the icon is in the correct location
sudo cp /usr/local/bin/audio_swop/icon.png /usr/local/bin/audio_swop/
sudo chmod 644 /usr/local/bin/audio_swop/icon.png

# Copy GIF
sudo cp /usr/local/bin/audio_swop/spinner.gif /usr/local/bin/audio_swop/

echo "Setup completed successfully."