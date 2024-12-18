from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Data to encrypt
plaintext = b"Secret message that needs confidentiality and authenticity."

# Generate a 256-bit key and a 96-bit nonce
key = get_random_bytes(32)   # 32 bytes for AES-256
nonce = get_random_bytes(12) # 12 bytes for GCM

# Encrypt
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
ciphertext, tag = cipher.encrypt_and_digest(plaintext)

print("AES-256-GCM Encryption:")
print("Key:", key.hex())
print("Nonce:", nonce.hex())
print("Ciphertext:", ciphertext.hex())
print("Tag:", tag.hex())

# Decrypt and verify authenticity
decipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
deciphered_text = decipher.decrypt_and_verify(ciphertext, tag)
print("Decrypted Text:", deciphered_text)
