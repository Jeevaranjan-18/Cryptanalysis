import argparse
import hashlib
import hmac
import json
import random
import string
import sys
import base64
import binascii
from urllib.parse import unquote, quote


# =========================================================
# HASH ATTACK FUNCTIONS
# =========================================================

# -------- Brute-force/Dictionary Cracking --------
def crack_hash(args):
    try:
        with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            for pwd in f:
                candidate = pwd.strip()
                h = hashlib.new(args.algo, candidate.encode()).hexdigest()
                if h == args.hash:
                    print(f'[+] Found: {candidate}')
                    return
        print('[-] No match found.')
    except Exception as e:
        print(f'Error: {e}')

# -------- Rainbow Table Generation --------
def rainbow_generate(args):
    table = {}
    try:
        with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            for pwd in f:
                candidate = pwd.strip()
                h = hashlib.new(args.algo, candidate.encode()).hexdigest()
                table[h] = candidate
        with open(args.output, 'w') as out:
            json.dump(table, out)
        print(f'Rainbow table saved to {args.output}')
    except Exception as e:
        print(f'Error: {e}')

# -------- Rainbow Table Lookup --------
def rainbow_lookup(args):
    try:
        with open(args.table, 'r') as f:
            table = json.load(f)
        if args.hash in table:
            print(f'[+] Cracked: {table[args.hash]}')
        else:
            print('[-] Not found in this rainbow table.')
    except Exception as e:
        print(f'Error: {e}')

# -------- HMAC Brute-Force --------
def hmac_brute(args):
    try:
        with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            for key in f:
                candidate = key.strip()
                digest = hmac.new(candidate.encode(), args.msg.encode(), getattr(hashlib, args.algo)).hexdigest()
                if digest == args.hmac:
                    print(f'[+] Found secret: {candidate}')
                    return
        print('[-] Secret key not found in wordlist.')
    except Exception as e:
        print(f'Error: {e}')

# -------- Birthday Attack --------
def birthday_attack(args):
    seen = dict()
    attempts = 0
    try:
        while True:
            s = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(args.length))
            h = hashlib.new(args.algo, s.encode()).hexdigest()
            if h in seen:
                print(f'[!] Collision after {attempts} tries:')
                print(f'    {seen[h]} <-> {s}')
                print(f'    Hash: {h}')
                break
            seen[h] = s
            attempts += 1
    except Exception as e:
        print(f'Error: {e}')


# =========================================================
# ENCODING / DECODING FUNCTIONS
# =========================================================

def decode_base64(data):
    try:
        return base64.b64decode(data).decode()
    except Exception as e:
        return str(e)

def encode_base64(data):
    try:
        return base64.b64encode(data.encode()).decode()
    except Exception as e:
        return str(e)

def decode_hex(data):
    try:
        return binascii.unhexlify(data).decode()
    except Exception as e:
        return str(e)

def encode_hex(data):
    try:
        return binascii.hexlify(data.encode()).decode()
    except Exception as e:
        return str(e)

def decode_url(data):
    try:
        return unquote(data)
    except Exception as e:
        return str(e)

def encode_url(data):
    try:
        return quote(data)
    except Exception as e:
        return str(e)


# =========================================================
# CLI SETUP
# =========================================================

def main():
    parser = argparse.ArgumentParser(
        description='Hash Algorithms, Attacks & Encoding/Decoding CLI Tool',
        usage="""hash_attacks.py <command> [<args>]

Available commands:
  crack           Brute-force/dictionary attack to crack a hash
  rainbow-gen     Generate a rainbow table from a wordlist
  rainbow-lookup  Look up a hash in a rainbow table
  hmac-brute      Brute-force HMAC secret from a wordlist
  birthday        Demonstrate birthday attack/collision

  base64-encode   Encode data in Base64
  base64-decode   Decode Base64-encoded data
  hex-encode      Encode data in Hex
  hex-decode      Decode Hex-encoded data
  url-encode      URL-encode data
  url-decode      URL-decode data

Use hash_attacks.py <command> --help for details on each command.
"""
    )
    subparsers = parser.add_subparsers(dest='command', help='Modules')

    # Crack
    crack_parser = subparsers.add_parser('crack', help='Brute-force/dictionary attack on a hash')
    crack_parser.add_argument('--hash', required=True, help='Target hash to crack')
    crack_parser.add_argument('--algo', choices=hashlib.algorithms_guaranteed, required=True, help='Hash algorithm')
    crack_parser.add_argument('--wordlist', required=True, help='Wordlist file')

    # Rainbow Table Generate
    rainbow_gen_parser = subparsers.add_parser('rainbow-gen', help='Generate rainbow table')
    rainbow_gen_parser.add_argument('--algo', choices=hashlib.algorithms_guaranteed, required=True, help='Hash algorithm')
    rainbow_gen_parser.add_argument('--wordlist', required=True, help='Wordlist file')
    rainbow_gen_parser.add_argument('--output', required=True, help='Output file for table')

    # Rainbow Lookup
    rainbow_lookup_parser = subparsers.add_parser('rainbow-lookup', help='Lookup hash in rainbow table')
    rainbow_lookup_parser.add_argument('--hash', required=True, help='Hash to lookup')
    rainbow_lookup_parser.add_argument('--table', required=True, help='Rainbow table file')

    # HMAC Brute-force
    hmac_brute_parser = subparsers.add_parser('hmac-brute', help='Brute-force HMAC secret from wordlist')
    hmac_brute_parser.add_argument('--hmac', required=True, help='Target HMAC hex digest')
    hmac_brute_parser.add_argument('--msg', required=True, help='Message')
    hmac_brute_parser.add_argument('--algo', choices=hashlib.algorithms_guaranteed, required=True, help='Hash algo for HMAC')
    hmac_brute_parser.add_argument('--wordlist', required=True, help='Wordlist file for keys')

    # Birthday Attack
    birthday_parser = subparsers.add_parser('birthday', help='Demonstrate birthday paradox collision finding')
    birthday_parser.add_argument('--algo', choices=hashlib.algorithms_guaranteed, required=True, help='Hash algorithm')
    birthday_parser.add_argument('--length', type=int, default=8, help='Random string length')

    # Encoding/Decoding commands
    base64_enc = subparsers.add_parser('base64-encode', help='Encode string to Base64')
    base64_enc.add_argument('--data', required=True, help='String to encode')

    base64_dec = subparsers.add_parser('base64-decode', help='Decode Base64 string')
    base64_dec.add_argument('--data', required=True, help='Base64 string to decode')

    hex_enc = subparsers.add_parser('hex-encode', help='Encode string to Hex')
    hex_enc.add_argument('--data', required=True, help='String to encode')

    hex_dec = subparsers.add_parser('hex-decode', help='Decode Hex string')
    hex_dec.add_argument('--data', required=True, help='Hex string to decode')

    url_enc = subparsers.add_parser('url-encode', help='URL-encode a string')
    url_enc.add_argument('--data', required=True, help='String to URL-encode')

    url_dec = subparsers.add_parser('url-decode', help='URL-decode a string')
    url_dec.add_argument('--data', required=True, help='URL-encoded string to decode')

    args = parser.parse_args()

    # Dispatch
    if args.command == 'crack':
        crack_hash(args)
    elif args.command == 'rainbow-gen':
        rainbow_generate(args)
    elif args.command == 'rainbow-lookup':
        rainbow_lookup(args)
    elif args.command == 'hmac-brute':
        hmac_brute(args)
    elif args.command == 'birthday':
        birthday_attack(args)
    elif args.command == 'base64-encode':
        print(encode_base64(args.data))
    elif args.command == 'base64-decode':
        print(decode_base64(args.data))
    elif args.command == 'hex-encode':
        print(encode_hex(args.data))
    elif args.command == 'hex-decode':
        print(decode_hex(args.data))
    elif args.command == 'url-encode':
        print(encode_url(args.data))
    elif args.command == 'url-decode':
        print(decode_url(args.data))
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
