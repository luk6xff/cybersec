# https://cryptohack.org/courses/intro/xor0/

DATA = "label"
NUM = 13

# XOR each byte with 13
xored = [chr(ord(c) ^ NUM) for c in DATA]
print(''.join(xored))
