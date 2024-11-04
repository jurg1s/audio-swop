#!/bin/bash
# This setup script installs dependencies and copies application files.

# Define the application directory
APP_DIR="/usr/share/audio-swop"
mkdir -p "$APP_DIR"

# Copy application files
cp /usr/share/audio-swop/audio_swop.py "$APP_DIR/"
cp /usr/share/audio-swop/requirements.txt "$APP_DIR/"
cp /usr/share/audio-swop/spinner.gif "$APP_DIR/"
cp /usr/share/audio-swop/setup.sh "$APP_DIR/"

echo "Setup complete. Application files copied."