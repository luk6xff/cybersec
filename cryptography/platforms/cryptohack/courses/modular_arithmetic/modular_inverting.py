# https://cryptohack.org/courses/modular/mdiv/



# g * d = 1 mod p

from sympy import mod_inverse

# Given values
a = 3
modulus = 13

# Compute the modular inverse of a modulo modulus
inverse_d = mod_inverse(a, modulus)

print(f"The modular inverse of {a} modulo {modulus} is {inverse_d}.")
