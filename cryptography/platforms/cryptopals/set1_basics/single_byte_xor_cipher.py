'''
Single-byte XOR cipher
The hex encoded string:

1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
... has been XOR'd against a single character. Find the key, decrypt the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.

Achievement Unlocked
You now have our permission to make "ETAOIN SHRDLU" jokes on Twitter.
'''


import binascii

def xor_decrypt(s: str, c: int) -> str:
    s_bytes = binascii.unhexlify(s)
    xor_bytes = bytes([a ^ c for a in s_bytes])
    return xor_bytes.decode('ascii')


if __name__ == '__main__':
    s = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

    for c in range(ord('a'), ord('z')+1):
        print(f'Key: {chr(c)}\tDecrypted: {xor_decrypt(s, c)}')

    print(xor_decrypt(s, ord('x'))) # Cooking MC's like a pound of bacon

