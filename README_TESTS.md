# Genio – Testscripts

Detta paket innehåller fristående testskript för att verifiera varje del:
- `test_wakeword.py` – Porcupine wakeword
- `test_stt.py` – Whisper STT (faster-whisper)
- `test_tts.py` – Piper TTS
- `test_mqtt.py` – MQTT TLS mot HiveMQ Cloud

## Förbered
```bash
source /opt/genio/venv/bin/activate
pip install pvporcupine faster-whisper sounddevice webrtcvad pydub pyyaml rich paho-mqtt numpy
```

## Wakeword
```bash
python3 test_wakeword.py --keyword /opt/genio/models/porcupine/hey-genio.ppn --sensitivity 0.6
# ev. --device-name "hw:CARD=...,DEV=0" eller --device-index 2
```

## STT
```bash
# spela in 5s och transkribera
python3 test_stt.py --record-seconds 5 --out /tmp/utt.wav --model tiny --lang sv

# transkribera befintlig fil
python3 test_stt.py --wav /path/to/file.wav --model small --lang sv
```

## TTS
```bash
python3 test_tts.py --text "Hej från Genio!" --model /opt/genio/models/piper/sv-SE-nordic.onnx --out /tmp/tts.wav
aplay /tmp/tts.wav
```

## MQTT
```bash
export MQTT_PASSWORD='<ditt-lösen>'
python3 test_mqtt.py --host <hivemq-host> --user <user> --password-env MQTT_PASSWORD --topic genio/pi5/req --payload "hej" --subscribe genio/pi5/resp
```
