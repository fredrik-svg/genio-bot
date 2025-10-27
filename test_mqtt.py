#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Snabbtest av MQTT-anslutning (HiveMQ Cloud) via TLS.
Krav: paho-mqtt
Använd:
  python3 test_mqtt.py --host <HOST> --user <USER> --password-env MQTT_PASSWORD --topic genio/pi5/req --payload "hej"
"""
import argparse
import os
import json
import ssl
import time
import paho.mqtt.client as mqtt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True)
    ap.add_argument("--port", type=int, default=8883)
    ap.add_argument("--user", required=True)
    ap.add_argument("--password-env", default="MQTT_PASSWORD")
    ap.add_argument("--topic", required=True)
    ap.add_argument("--payload", default="ping")
    ap.add_argument("--cafile", default="/etc/ssl/certs/ca-certificates.crt")
    ap.add_argument("--client-id", default="genio-test")
    ap.add_argument("--subscribe", default=None, help="Valfritt: topic att lyssna på efter publish")
    args = ap.parse_args()

    pw = os.environ.get(args.password_env)
    if not pw:
        raise SystemExit(f"Env-var {args.password_env} saknas (exportera lösenordet innan körning).")

    client = mqtt.Client(client_id=args.client_id, protocol=mqtt.MQTTv311)
    client.username_pw_set(args.user, pw)
    client.tls_set(ca_certs=args.cafile)

    if args.subscribe:
        def on_msg(_c,_u,m):
            print(f"[recv] {m.topic}: {m.payload.decode('utf-8','ignore')}")
        client.on_message = on_msg

    print(f"🔐 Ansluter TLS → {args.host}:{args.port}")
    client.connect(args.host, args.port, keepalive=30)
    client.loop_start()

    if args.subscribe:
        client.subscribe(args.subscribe, qos=1)

    print(f"[send] {args.topic}: {args.payload}")
    client.publish(args.topic, args.payload, qos=1)

    time.sleep(2.0)
    client.loop_stop(); client.disconnect()
    print("✅ Klart.")

if __name__ == "__main__":
    main()
