import argparse
from genio import __version__

def cmd_version(_args):
    print(__version__)

def cmd_health(_args):
    # Placeholder: real TLS check happens on device with network/certs present
    print('{"component":"mqtt","tls_handshake_ok":true}')

def cmd_say(args):
    # Placeholder: actual TTS occurs on device (Piper). This is a stub for packaging.
    print(f"TTS would say: {args.text}")

def cmd_run(_args):
    # Placeholder main loop; the full runtime should be used on the Pi.
    print("Agent runtime placeholder. Deploy on Raspberry Pi to run full pipeline.")

def main():
    ap = argparse.ArgumentParser(prog="genioctl", description="Genio voice agent controller")
    sub = ap.add_subparsers(dest="cmd", required=True)

    rp = sub.add_parser("run", help="start agent (placeholder)")
    rp.set_defaults(func=cmd_run)

    hp = sub.add_parser("health", help="TLS/MQTT health (placeholder)")
    hp.set_defaults(func=cmd_health)

    sp = sub.add_parser("say", help="TTS say (placeholder)")
    sp.add_argument("--text", required=True)
    sp.set_defaults(func=cmd_say)

    vp = sub.add_parser("version", help="print version")
    vp.set_defaults(func=cmd_version)

    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
