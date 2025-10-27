#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testa STT (faster-whisper).
Krav: faster-whisper, sounddevice (om du vill spela in), numpy
Använd:
  python3 test_stt.py --wav /path/to/file.wav \
      --model tiny --lang sv
eller spela in nytt klipp (5s):
  python3 test_stt.py --record-seconds 5 --out /tmp/utt.wav \
      --model small --lang sv
"""
import argparse
import wave
import sys
import sounddevice as sd
from faster_whisper import WhisperModel

SR = 16000


def record_wav(seconds: int, out_path: str, device=None):
    print(f"🎙️ Spelar in {seconds}s @ {SR} Hz ...")
    data = sd.rec(int(seconds * SR), samplerate=SR, channels=1,
                  dtype="int16", device=device)
    sd.wait()
    with wave.open(out_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(data.tobytes())
    print(f"💾 Sparat: {out_path}")
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wav", help="Befintlig WAV-fil att transkribera")
    ap.add_argument("--record-seconds", type=int,
                    help="Spela in så här många sekunder")
    ap.add_argument("--out", default="/tmp/utt.wav",
                    help="Väg för inspelad WAV "
                         "(om --record-seconds används)")
    ap.add_argument("--model", default="tiny",
                    help="Whisper-modell (tiny, base, small, ...)")
    ap.add_argument("--lang", default="sv",
                    help="Språk, t.ex. sv eller en")
    ap.add_argument("--device-index", type=int, default=None)
    ap.add_argument("--device-name", type=str, default=None)
    args = ap.parse_args()

    if not args.wav and not args.record_seconds:
        print("Ange --wav eller --record-seconds", file=sys.stderr)
        sys.exit(2)

    wav_path = args.wav
    if args.record_seconds:
        device = args.device_name if args.device_name else args.device_index
        wav_path = record_wav(args.record_seconds, args.out, device=device)

    print(f"🧠 Laddar Whisper-modell: {args.model}")
    model = WhisperModel(args.model)
    segments, info = model.transcribe(wav_path, language=args.lang)
    text = "".join([s.text for s in segments]).strip()
    print("📝 Transkription:")
    print(text)


if __name__ == "__main__":
    main()
