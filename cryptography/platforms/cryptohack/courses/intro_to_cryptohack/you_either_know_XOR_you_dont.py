# https://cryptohack.org/courses/intro/xorkey1/

secret_data = '0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104'


# Convert the hex string to bytes
data_bytes = bytes.fromhex(secret_data)


# Solution
# FLAG ^ KEY = CIPHER (secret_data)
# FLAG = CIPHER ^ KEY => KEY = CIPHER ^ FLAG
# FLAG = crypto{...}

flag = 'crypto{'.encode()

# Guess the key
key = bytes([a ^ b for a, b in zip(flag, data_bytes)])

print(f'Key: {key}')
key = key + b'y'
print(f'Key: {key}')


# Ensure key is repeated to match the length of data_bytes
repeated_key = (key * (len(data_bytes) // len(key) + 1))[:len(data_bytes)]
FLAG = bytes([a ^ b for a, b in zip(repeated_key, data_bytes)])
print(f'FLAG: {"".join(chr(c) for c in FLAG)}')
