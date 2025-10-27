#!/usr/bin/env bash
set -euo pipefail
echo "==> Installera systemberoenden"
sudo apt update
sudo apt -y install   python3 python3-venv python3-pip   portaudio19-dev libssl-dev libasound2-dev ffmpeg git jq   mosquitto-clients alsa-utils
echo "==> Python-version:"
python3 --version || true
if [ -d /opt/genio/.git ]; then
  echo "==> Säkerställ ägarskap på /opt/genio"
  sudo chown -R "$USER":"$USER" /opt/genio
fi
echo "==> Skapa venv i /opt/genio"
sudo mkdir -p /opt/genio && sudo chown "$USER":"$USER" /opt/genio
cd /opt/genio
if [ ! -d venv ]; then
  python3 -m venv venv
fi
source venv/bin/activate
echo "==> Uppgradera pip & installera Python-beroenden"
python -m pip install --upgrade pip wheel
if [ -f requirements.txt ] && [ -f constraints.txt ]; then
  pip install -r requirements.txt -c constraints.txt || pip install -r requirements.txt
elif [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi
echo "✅ Klar: venv på /opt/genio/venv (Python: $(python --version 2>/dev/null || echo 'ok'))"
