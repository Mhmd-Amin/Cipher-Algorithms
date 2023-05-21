import random

def generate_prime():
    while True:
        p = random.randint(100, 1000)  # Adjust the range as needed
        if is_prime(p):
            return p

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def generate_keys():
    p = generate_prime()
    g = random.randint(2, p-1)
    while pow(g, (p-1)//2, p) != 1:
        g = random.randint(2, p-1)
    private_key = random.randint(2, p-2)
    public_key = pow(g, private_key, p)
    return p, g, public_key, private_key

def generate_shared_secret(public_key, private_key, p):
    return pow(public_key, private_key, p)

# Example usage
# Key generation for Alice
# p, g, public_key_alice, private_key_alice = generate_keys()

# Key generation for Bob
# p, g, public_key_bob, private_key_bob = generate_keys()

# Key exchange
# shared_secret_alice = generate_shared_secret(public_key_bob, private_key_alice, p)
# shared_secret_bob = generate_shared_secret(public_key_alice, private_key_bob, p)

# Verify shared secrets match
# print("Shared Secret for Alice:", shared_secret_alice)
# print("Shared Secret for Bob:", shared_secret_bob)
