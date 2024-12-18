# https://cryptohack.org/courses/modular/ma1/


p = 17
print(pow(3, p) % p)
print(pow(5, p) % p)
print(pow(7, p-1) % p)


# Solution
p = 65537
print(pow(273246787654, p-1) % p)
