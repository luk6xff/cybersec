# https://cryptohack.org/courses/modular/egcd/

import math


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

# Define the primes p and q
p = 26513
q = 32321

# Use the extended_gcd function to find u and v
gcd, u, v = extended_gcd(p, q)

# Print the results
print(f"gcd({p}, {q}) = {gcd}")
print(f"u = {u}, v = {v}")
print(f"Check: {p}*{u} + {q}*{v} = {p*u + q*v}")
