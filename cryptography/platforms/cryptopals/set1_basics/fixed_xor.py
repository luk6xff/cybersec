'''
Fixed XOR
Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:

1c0111001f010100061a024b53535009181c
... after hex decoding, and when XOR'd against:

686974207468652062756c6c277320657965
... should produce:

746865206b696420646f6e277420706c6179
'''

import binascii

def fixed_xor(s1: str, s2: str) -> str:
    s1_bytes = binascii.unhexlify(s1)
    s2_bytes = binascii.unhexlify(s2)
    xor_bytes = bytes([a ^ b for a, b in zip(s1_bytes, s2_bytes)])
    return binascii.hexlify(xor_bytes).decode()

s1 = '1c0111001f010100061a024b53535009181c'
s2 = '686974207468652062756c6c277320657965'
s_expected = '746865206b696420646f6e277420706c6179'

print(fixed_xor(s1, s2))
assert(fixed_xor(s1, s2) == s_expected)
