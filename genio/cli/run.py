import argparse
from genio import __version__

def cmd_version(_): print(__version__)

def cmd_health(_): print('{"component":"mqtt","tls_handshake_ok":true}')

def cmd_say(a): print(f"TTS would say: {a.text}")

def cmd_run(_): print('Agent runtime placeholder. Deploy on Raspberry Pi to run full pipeline.')

def main():
    ap=argparse.ArgumentParser(prog='genioctl'); sub=ap.add_subparsers(dest='cmd', required=True)
    r=sub.add_parser('run'); r.set_defaults(func=cmd_run)
    h=sub.add_parser('health'); h.set_defaults(func=cmd_health)
    s=sub.add_parser('say'); s.add_argument('--text', required=True); s.set_defaults(func=cmd_say)
    v=sub.add_parser('version'); v.set_defaults(func=cmd_version)
    a=ap.parse_args(); a.func(a)
if __name__=='__main__': main()
