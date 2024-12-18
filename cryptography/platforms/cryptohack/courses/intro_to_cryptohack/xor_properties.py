# https://cryptohack.org/courses/intro/xor1/

import binascii

KEY1 = binascii.unhexlify('a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313')
KEY2_XOR_KEY1 = binascii.unhexlify('37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e')
KEY2_XOR_KEY3 = binascii.unhexlify('c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1')
FLAG_XOR_KEY1_XOR_KEY3_XOR_KEY2 = binascii.unhexlify('04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf')


# Solution
## 1. KEY2 = KEY2_XOR_KEY1 ^ KEY1
KEY2 = bytes([a ^ b for a, b in zip(KEY2_XOR_KEY1, KEY1)])
print(f'Key2: {binascii.hexlify(KEY2).decode("utf-8")}')

## 2. KEY3 = KEY2_XOR_KEY3 ^ KEY2
KEY3 = bytes([a ^ b for a, b in zip(KEY2_XOR_KEY3, KEY2)])
print(f'Key3: {binascii.hexlify(KEY3).decode("utf-8")}')

## 3. FLAG = FLAG_XOR_KEY1_XOR_KEY3_XOR_KEY2 ^ KEY3 ^ KEY2 ^ KEY1
#LAG = bytes([a ^ b ^ c ^ d for a, b, c, d in zip(FLAG_XOR_KEY1_XOR_KEY3_XOR_KEY2, KEY1, KEY2, KEY3)])

KEY_ALL = bytes([a ^ b for a, b in zip(KEY2_XOR_KEY3 , KEY1)])
FLAG = bytes([a ^ b for a, b in zip(FLAG_XOR_KEY1_XOR_KEY3_XOR_KEY2, KEY_ALL)])
print(f'FLAG: crypto{{{binascii.hexlify(FLAG).decode("ascii")}}}')
print(f'FLAG: {"".join(chr(c) for c in FLAG)}')


