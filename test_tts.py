#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testa Piper TTS.
Krav: piper-bin installerad och en .onnx-röst.
Använd:
  python3 test_tts.py --text "Hej!" \
      --model /opt/genio/models/piper/sv-SE-nordic.onnx \
      --out /tmp/tts.wav
Valfritt:
  --device "hw:CARD=...,DEV=0" för aplay -D
"""
import argparse
import subprocess


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--model", required=True, help="Sökväg till Piper .onnx")
    ap.add_argument("--out", default="/tmp/tts.wav")
    ap.add_argument("--device", default=None,
                    help="ALSA device för aplay "
                         "(ex. hw:CARD=UCA222,DEV=0)")
    ap.add_argument("--piper-bin", default="piper",
                    help="piper-bin (default: piper i PATH)")
    args = ap.parse_args()

    cmd = [args.piper_bin, "--model", args.model,
           "--output_file", args.out, "--text", args.text]
    print("🔊 Kör:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    play = ["aplay"]
    if args.device:
        play += ["-D", args.device]
    play += [args.out]
    print("▶️  Spelar upp:", " ".join(play))
    subprocess.run(play, check=False)


if __name__ == "__main__":
    main()
