#!/bin/bash

# Set the path to the virtual environment and requirements file using the updated paths
VENV_PATH="$(dirname "$0")/progress/env_pcm"
SETUP_PATH="$(dirname "$0")/progress/env_pcm/snl_quest_pcm"

# Set the equity directory name
pcm_dir="snl_quest_pcm"

# Create the virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    python3.11 -m venv "$VENV_PATH"
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Install system dependencies
sudo apt-get install -y python3-dev libblas-dev liblapack-dev gfortran


# Create a directory within the virtual environment
mkdir -p "$VENV_PATH/$pcm_dir"

# Clone the GitHub repository
git clone --b progress_integration --single-branch  https://github.com/sandialabs/quest_PCM "$VENV_PATH/snl_quest_pcm"

# Install using setup.py
pip install -e "$SETUP_PATH"

# Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate

echo "Setup complete."
