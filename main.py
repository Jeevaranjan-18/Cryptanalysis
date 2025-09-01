import argparse
from modules.rsa import *
from modules.hashAttacker import *
from modules.aes import *
from pyfiglet import Figlet
def main():
    f = Figlet(font='slant')
    print(f"\033[{random.randint(91,96)}m"+f.renderText('Cryptanalyser')+"\033[0m")

    parser = argparse.ArgumentParser(description="Cryptanalysis Toolkit")

    subparsers = parser.add_subparsers(dest="command", required=False)
    aes_parser = subparsers.add_parser("aes", help="Perform AES attacks")
    aes_parser.add_argument("--server", type=str, help="Oracle server")
    
    rsa_pem_parser = subparsers.add_parser("rsa_pem", help="Perform RSA PEM attacks")
    rsa_pem_parser.add_argument("--public", required=True, help="Path to the public key file")

    rsa_parser = subparsers.add_parser("rsa", help="Perform RSA cryptanalysis")
    rsa_parser.add_argument("-n", type=int, help="Modulus n")
    rsa_parser.add_argument("-e", type=int, help="Public exponent e")
    rsa_parser.add_argument("-c", type=int, help="Ciphertext c")
    rsa_parser.add_argument("-p", type=int, help="Prime factor p")
    rsa_parser.add_argument("-q", type=int, help="Prime factor q")

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

    if args.command == "rsa_pem":
        rsa_pem(args.public)
    elif args.command == "aes":
        cpa(args.server)
    elif args.command == "rsa":
        # Case 1: Given n, e, c
        if args.n and args.e and args.c:
            rsa_fact(args.n, args.e, args.c)

        # Case 2: Given p, q, e, c
        elif args.p and args.q and args.e and args.c:
            rsa(args.p, args.q, args.e, args.c)

        # Case 3: e=3 and c given (likely small exponent attack)
        elif args.e == 3 and args.c:
            rsa_e(args.c, args.e)

        else:
            print("Insufficient or incorrect arguments for rsa command.")
            parser.print_help()
       # Dispatch
    elif args.command == 'crack':
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

if __name__ == "__main__":
    main()

