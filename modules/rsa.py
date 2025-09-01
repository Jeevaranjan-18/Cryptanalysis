from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse
from factordb.factordb import FactorDB

def factor_n(n):
    f = FactorDB(n)
    f.connect()
    factors = f.get_factor_list()
    return factors

def rsa_pem(s):
    with open(s , "rb") as f:
        key = RSA.import_key(f.read())

    n = key.n
    e = key.e
    print(f"Extracted n: {n}")
    print(f"Extracted e: {e}")

    factors = factor_n(n)
    print(f"Factors from FactorDB: {factors}")

    if len(factors) != 2:
        print("Warning: n does not factor into exactly two primes!")
        return

    p, q = factors

    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)

    private_key = RSA.construct((n, e, d, p, q))

    with open("private.pem", "wb") as f:
        f.write(private_key.export_key())

    print("Private key saved to private.pem")

if __name__ == "__main__":
    rsa_pem()

