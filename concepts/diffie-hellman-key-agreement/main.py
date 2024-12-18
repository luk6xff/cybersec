import secrets

# Function to compute modular exponentiation
def mod_exp(base, exponent, modulus):
    return pow(base, exponent, modulus)

# Large prime number p and generator g
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F  # Large prime
g = 2  # Generator

print("Publicly agreed variables:")
print(f"Prime number (p): {p}")
print(f"Generator (g): {g}\n")

# Alice generates her private key
a = secrets.randbelow(p - 2) + 1
A = mod_exp(g, a, p)

print("Alice's calculations:")
print(f"Private key (a): (hidden for security)")
print(f"Public key (A = g^a mod p): {A}\n")

# Bob generates his private key
b = secrets.randbelow(p - 2) + 1
B = mod_exp(g, b, p)

print("Bob's calculations:")
print(f"Private key (b): (hidden for security)")
print(f"Public key (B = g^b mod p): {B}\n")

# Exchange of public keys

# Alice computes the shared secret
s_alice = mod_exp(B, a, p)
print("Alice computes the shared secret.\n")

# Bob computes the shared secret
s_bob = mod_exp(A, b, p)
print("Bob computes the shared secret.\n")

# Verify that both shared secrets are equal
if s_alice == s_bob:
    print("Success! Both Alice and Bob have the same shared secret.")
else:
    print("Error! The shared secrets do not match.")
