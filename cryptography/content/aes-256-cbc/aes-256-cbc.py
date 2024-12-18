from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Data to encrypt
plaintext = b"Secret message that needs confidentiality only."

# Generate a 256-bit key and a 128-bit IV
key = get_random_bytes(32) # 32 bytes for AES-256
iv = get_random_bytes(16)  # 16 bytes for IV

# Encrypt using AES-CBC
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

# Compute an HMAC over the ciphertext to provide authenticity
hmac = HMAC.new(key, ciphertext, digestmod=SHA256)
auth_tag = hmac.digest()

print("\nAES-256-CBC Encryption:")
print("Key:", key.hex())
print("IV:", iv.hex())
print("Ciphertext:", ciphertext.hex())
print("HMAC:", auth_tag.hex())

# Decrypt and verify integrity
# First verify the HMAC before decrypting
hmac_verify = HMAC.new(key, ciphertext, digestmod=SHA256)
try:
    hmac_verify.verify(auth_tag)  # Will raise ValueError if mismatch
    # If integrity check passes, then decrypt
    decipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_plaintext = unpad(decipher.decrypt(ciphertext), AES.block_size)
    print("Decrypted Text:", decrypted_plaintext)
except ValueError:
    print("Integrity check failed! Ciphertext has been tampered with.")
