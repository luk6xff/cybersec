'''
Detect single-character XOR
One of the 60-character strings in this: [file](detect_single_character_xor.txt) has been encrypted by single-character XOR.

Find it.

(Your code from #3 (single_byte_xor_cipher.py) should help.)
'''

import binascii
from single_byte_xor_cipher import xor_decrypt


with open('detect_single_character_xor.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        for c in range(ord('a'), ord('z')+1):
            decrypted = xor_decrypt(line, c)
            if all([(c > 'A' and c < 'z')  for c in decrypted]):
                print(f'Key: {chr(c)}\tDecrypted: {decrypted}')
                break
