#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testa Porcupine wake word lokalt.
Krav: pvporcupine, sounddevice
Använd:
  python3 test_wakeword.py --keyword /opt/genio/models/porcupine/hey-genio.ppn --sensitivity 0.6
Valfritt:
  --device-index N  (ALSA index)  eller  --device-name "hw:CARD=...,DEV=..."
"""
import argparse
import sys
import time
import pvporcupine
import sounddevice as sd
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keyword", required=True, help="Sökväg till .ppn")
    ap.add_argument("--model", default=None, help="Sökväg till porcupine_params.pv (om krävs)")
    ap.add_argument("--sensitivity", type=float, default=0.6)
    ap.add_argument("--device-index", type=int, default=None)
    ap.add_argument("--device-name", type=str, default=None)
    args = ap.parse_args()

    porcupine = pvporcupine.create(
        keyword_paths=[args.keyword],
        model_path=args.model,
        sensitivities=[args.sensitivity],
    )

    device = args.device_name if args.device_name else args.device_index

    def callback(indata, frames, time_info, status):
        if status:
            # print(status, file=sys.stderr)
            pass
        # indata is bytes when using RawInputStream, but float array when InputStream.
        # We will use RawInputStream for exact int16 PCM.
        # (this callback will not be used; see below)
        pass

    print("🎧 Lyssnar... säg wakeword. Avsluta med Ctrl+C")
    detected = 0
    try:
        with sd.RawInputStream(
            samplerate=porcupine.sample_rate,
            blocksize=porcupine.frame_length,
            dtype="int16",
            channels=1,
            device=device,
        ) as stream:
            while True:
                # Läs exakt en ram (porcupine.frame_length * 2 bytes)
                buf = stream.read(porcupine.frame_length)[0]
                if not buf:
                    continue
                pcm = np.frombuffer(buf, dtype=np.int16)
                res = porcupine.process(pcm)
                if res >= 0:
                    detected += 1
                    print(f"✅ Wake word detected ({detected})")
    except KeyboardInterrupt:
        pass
    finally:
        porcupine.delete()

if __name__ == "__main__":
    main()
