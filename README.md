# Cipher-Algorithms

---
# ElGamal Encryption Algorithm

The ElGamal encryption algorithm is a public-key encryption scheme that provides confidentiality and allows secure communication between two parties. It is based on the computational difficulty of solving the discrete logarithm problem. The algorithm involves key generation, encryption, and decryption processes.

## Key Generation

The key generation process involves the following steps:

1. Generate a large prime number `p`.
2. Choose a primitive root `g` modulo `p`.
3. Select a private key `private_key`, a random integer between 2 and `p-2`.
4. Compute the public key `public_key` as `g` raised to the power of `private_key` modulo `p`.

## Encryption

To encrypt a message using ElGamal encryption, follow these steps:

1. Generate a random secret number `secret` between 2 and `p-2`.
2. Compute the shared key `shared_key` as the public key raised to the power of `secret` modulo `p`.
3. For each element `m` in the message:
   - Generate a random number `k` between 2 and `p-2`.
   - Compute the ciphertext pair `(c1, c2)` as follows:
     - `c1 = g^k mod p`
     - `c2 = (public_key^k * m) mod p`
   - Append the ciphertext pair `(c1, c2)` to the ciphertext.

## Decryption

To decrypt the ciphertext back to the original message, use the following steps:

1. For each ciphertext pair `(c1, c2)`:
   - Compute the shared key `shared_key` as `c1` raised to the power of the private key modulo `p`.
   - Compute the plaintext `m` as `(c2 * mod_inverse(shared_key, p)) mod p`.
   - Append `m` to the plaintext.

## Example Usage

```python
# Example usage
message = [15, 27, 9]  # Message to encrypt

# Key generation
p, g, public_key, private_key = generate_keys()

# Encryption
ciphertext, shared_key = encrypt(message, p, g, public_key)

# Decryption
plaintext = decrypt(ciphertext, p, private_key)

print("Original Message:", message)
print("Decrypted Message:", plaintext)
```
---

---
# Diffie-Hellman Key Exchange Algorithm

The Diffie-Hellman key exchange algorithm is a method for two parties to securely establish a shared secret over an insecure communication channel. It allows the parties to agree upon a shared secret without directly transmitting it, providing a means for secure key establishment.

## Key Generation

The key generation process involves the following steps for each party:

1. Generate a large prime number `p`.
2. Choose a primitive root `g` modulo `p`.
3. Select a private key `private_key`, a random integer between 2 and `p-2`.
4. Compute the public key `public_key` as `g` raised to the power of `private_key` modulo `p`.

## Key Exchange

To perform the key exchange between two parties, follow these steps:

1. Alice and Bob generate their respective private and public keys using the key generation process.
2. Alice shares her public key `public_key_alice` with Bob, and Bob shares his public key `public_key_bob` with Alice.
3. Alice calculates the shared secret by raising Bob's public key `public_key_bob` to the power of her private key `private_key_alice` modulo `p`.
4. Bob calculates the shared secret by raising Alice's public key `public_key_alice` to the power of his private key `private_key_bob` modulo `p`.

## Example Usage

```python
# Example usage
# Key generation for Alice
p, g, public_key_alice, private_key_alice = generate_keys()

# Key generation for Bob
p, g, public_key_bob, private_key_bob = generate_keys()

# Key exchange
shared_secret_alice = generate_shared_secret(public_key_bob, private_key_alice, p)
shared_secret_bob = generate_shared_secret(public_key_alice, private_key_bob, p)

# Verify shared secrets match
print("Shared Secret for Alice:", shared_secret_alice)
print("Shared Secret for Bob:", shared_secret_bob)
```
---


---
# Miller-Rabin Primality Testing Algorithm

The Miller-Rabin primality testing algorithm is a probabilistic algorithm used to determine whether a given number is likely to be prime. It is based on the concept of witness values that can indicate whether a number is composite.

## Primality Testing

To test for primality using the Miller-Rabin algorithm, follow these steps:

1. Perform base cases:
   - If the number `n` is less than or equal to 1, return `False` (not prime).
   - If the number `n` is 2 or 3, return `True` (prime).
2. Express `n - 1` as `2^r * d`, where `r` is a non-negative integer and `d` is an odd number.
3. Repeat the following `k` times, where `k` is a parameter that determines the accuracy of the test:
   - Choose a random base `a` between 2 and `n - 2`, inclusive.
   - Compute `x = a^d mod n`.
   - If `x` is equal to 1 or `n - 1`, continue to the next iteration.
   - Repeat `r - 1` times:
     - Update `x` to `x^2 mod n`.
     - If `x` is equal to `n - 1`, break the loop.
   - If the loop completes without finding `n - 1`, return `False` (not prime).
4. Return `True` (likely prime).

## Example Usage

```python
# Example usage
num = 37  # Number to test for primality

if is_prime(num):
    print(f"{num} is prime.")
else:
    print(f"{num} is not prime.")
```

---