import random
from sympy import mod_inverse

# Function to generate a random prime number
def generate_prime():
    while True:
        p = random.randint(100, 1000)  # Adjust the range as needed
        if p % 2 != 0 and p % 3 != 0 and p % 5 != 0 and is_prime(p):
            return p

# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

# Extended Euclidean Algorithm to compute gcd and Bézout's coefficients
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

# ElGamal key generation
def generate_keys():
    # Generate a large prime number
    p = generate_prime()

    # Generate a primitive root
    while True:
        g = random.randint(2, p-1)
        if pow(g, (p-1)//2, p) != 1 and pow(g, (p-1)//3, p) != 1:
            break

    # Generate a private key (random number)
    private_key = random.randint(2, p-2)

    # Compute the public key
    public_key = pow(g, private_key, p)

    return p, g, public_key, private_key

# ElGamal encryption
def encrypt(message, p, g, public_key):
    # Generate a random secret number
    secret = random.randint(2, p-2)

    # Compute the shared key
    shared_key = pow(public_key, secret, p)

    # Compute the ciphertext
    ciphertext = []
    for m in message:
        k = random.randint(2, p-2)
        c1 = pow(g, k, p)
        c2 = (pow(public_key, k, p) * m) % p
        ciphertext.append((c1, c2))

    return ciphertext, shared_key

# ElGamal decryption
def decrypt(ciphertext, p, private_key):
    plaintext = []
    for c1, c2 in ciphertext:
        shared_key = pow(c1, private_key, p)
        m = (c2 * mod_inverse(shared_key, p)) % p
        plaintext.append(m)
    return plaintext

# Example usage
# message = [15, 27, 9] Message to encrypt

# Key generation
# p, g, public_key, private_key = generate_keys()

# Encryption
# ciphertext, shared_key = encrypt(message, p, g, public_key)

# Decryption
# plaintext = decrypt(ciphertext, p, private_key)

# print("Original Message:", message)
# print("Decrypted Message:", plaintext)
