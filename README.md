# Genio Voice Agent (Pi 5, Porcupine + HiveMQ Cloud + n8n)

Raspberry Pi 5-röstassistent med lokal wake word (Porcupine), STT (Whisper), TTS (Piper) och MQTT (HiveMQ Cloud) mot ett n8n-workflow. TLS via systemets CA-bundle.

## 🚀 Snabbstart på Raspberry Pi 5

### 1) Förbered OS
```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### 2) Klona projektet från GitHub
> **Viktigt:** Klona **utan** `sudo` för att undvika rättighetsproblem med `.git/`.

**HTTPS:**
```bash
cd ~
git clone https://github.com/<user>/<repo>.git
sudo mkdir -p /opt
sudo rsync -a --delete "<repo>"/ /opt/genio/
sudo chown -R $USER:$USER /opt/genio
cd /opt/genio
```

**SSH:**
```bash
cd ~
git clone git@github.com:<user>/<repo>.git
sudo mkdir -p /opt
sudo rsync -a --delete "<repo>"/ /opt/genio/
sudo chown -R $USER:$USER /opt/genio
cd /opt/genio
```

*Alternativt klona direkt till /opt utan sudo:*
```bash
sudo mkdir -p /opt && sudo chown $USER:$USER /opt
git clone https://github.com/<user>/<repo>.git /opt/genio
cd /opt/genio
```

### 3) Installera beroenden & skapa venv (Bookworm **och** Bullseye)
```bash
bash scripts/install_pi5.sh
```

### 4) Konfiguration
```bash
sudo mkdir -p /etc/genio
sudo cp configs/config.yaml.example /etc/genio/config.yaml
sudo cp configs/.env.example /etc/genio/genio.env
sudo nano /etc/genio/config.yaml     # sätt mqtt.host, username, password_env=MQTT_PASSWORD
sudo nano /etc/genio/genio.env       # sätt MQTT_PASSWORD=...
```

### 5) Hälsa & TTS-test
```bash
source /opt/genio/venv/bin/activate
genioctl version
genioctl health --config /etc/genio/config.yaml
genioctl say --config /etc/genio/config.yaml --text "Testar ljudsystemet"
```

### 6) Kör som tjänst
```bash
sudo cp systemd/genio-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now genio-agent
journalctl -u genio-agent -f
```

### 7) Uppdatera från GitHub
```bash
sudo systemctl stop genio-agent || true
sudo chown -R $USER:$USER /opt/genio
cd /opt/genio
git pull
source venv/bin/activate
pip install -U -r requirements.txt -c constraints.txt || pip install -U -r requirements.txt
sudo systemctl start genio-agent
```

## 🛠️ Felsökning

**Permission denied (.git/FETCH_HEAD):**
```bash
sudo chown -R $USER:$USER /opt/genio
cd /opt/genio && git pull
```

**Python-paket saknas (python3.11):**
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

**ALSA-enheter:**
```bash
arecord -l
aplay -l
# Ställ wakeword.device_name / tts.output_device i /etc/genio/config.yaml
```

## 🔒 TLS (HiveMQ Cloud)
- Port 8883
- `tls_ca_path: /etc/ssl/certs/ca-certificates.crt`
- Använd **FQDN** i mqtt.host (inte IP)
