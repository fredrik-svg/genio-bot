#!/usr/bin/env bash
set -euo pipefail
sudo apt update && sudo apt -y upgrade
sudo apt install -y python3.11 python3.11-venv portaudio19-dev libssl-dev libasound2-dev ffmpeg git jq mosquitto-clients alsa-utils
sudo mkdir -p /opt/genio && sudo chown $USER /opt/genio
cd /opt/genio
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt -c constraints.txt
