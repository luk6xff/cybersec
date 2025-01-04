#  https://cryptohack.org/courses/modular/root0/

# Given prime modulus
p = 29

# List of integers
ints = [14, 6, 11]

res = []
for a in range(1, p):
    if (a ** 2) % p in ints:
        res.append(a)

print(min(res))

