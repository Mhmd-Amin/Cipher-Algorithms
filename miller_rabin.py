import random

def is_prime(n, k=5):
    # Base cases
    if n <= 1:
        return False
    if n <= 3:
        return True

    # Find r and d such that n-1 = 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Perform Miller-Rabin primality tests
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

# Example usage
# num = 37  # Number to test for primality
# if is_prime(num):
    # print(f"{num} is prime.")
# else:
    # print(f"{num} is not prime.")
