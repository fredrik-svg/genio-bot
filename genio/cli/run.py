import argparse

def cmd_version(_args):
    print("0.1.0")

def cmd_health(args):
    print(f'{{"component":"mqtt","tls_handshake_ok":true,"config":"{args.config}"}}')

def cmd_say(args):
    print(f'[TTS] ({args.config}) {args.text}')

def cmd_run(args):
    print(f"Agent runtime placeholder. Using config: {args.config}")

def main():
    ap = argparse.ArgumentParser(prog="genioctl", description="Genio voice agent controller")
    ap.add_argument("--config", default="/etc/genio/config.yaml", help="Sökväg till konfigfilen")
    sub = ap.add_subparsers(dest="cmd", required=True)
    rp = sub.add_parser("run", help="starta agenten (placeholder)")
    rp.set_defaults(func=cmd_run)
    hp = sub.add_parser("health", help="TLS/MQTT-hälsa (placeholder)")
    hp.set_defaults(func=cmd_health)
    sp = sub.add_parser("say", help="TTS (placeholder)")
    sp.add_argument("--text", required=True)
    sp.set_defaults(func=cmd_say)
    vp = sub.add_parser("version", help="visa version")
    vp.set_defaults(func=cmd_version)
    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
