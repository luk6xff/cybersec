# https://cryptohack.org/courses/intro/xorkey0/

import binascii

data = '73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d'

# Convert the hex string to bytes
data_bytes = bytes.fromhex(data)
data_bytes = binascii.unhexlify(data)

# Guess he key (single byte)
for i in range(256):
    key = bytes([i])
    # XOR the data with the key
    flag_bytes = bytes([a ^ key[0] for a in data_bytes])
    flag = "".join(chr(c) for c in flag_bytes)
    if 'crypto' in flag:
        print(f'Key: {key}')
        print(f'Flag: {flag}')
        break
