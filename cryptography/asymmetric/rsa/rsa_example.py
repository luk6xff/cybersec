"""
RSA-2048 Encryption (OAEP) and Signing (PSS) Example

Demonstrates:
- Key generation (2048-bit)
- Encryption with OAEP padding (secure against Bleichenbacher)
- Digital signature with PSS padding
- Verification

Dependencies: pip install cryptography
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


def generate_rsa_keypair(key_size: int = 2048):
    """Generate RSA key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    return private_key, private_key.public_key()


def encrypt_oaep(public_key, plaintext: bytes) -> bytes:
    """Encrypt using RSA-OAEP (recommended padding for encryption)."""
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext


def decrypt_oaep(private_key, ciphertext: bytes) -> bytes:
    """Decrypt using RSA-OAEP."""
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext


def sign_pss(private_key, message: bytes) -> bytes:
    """Sign using RSA-PSS (recommended padding for signing)."""
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def verify_pss(public_key, message: bytes, signature: bytes) -> bool:
    """Verify RSA-PSS signature."""
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


def export_keys(private_key):
    """Export keys in PEM format (for demonstration)."""
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem


if __name__ == "__main__":
    # --- Key Generation ---
    print("=" * 60)
    print("RSA-2048 Key Generation")
    print("=" * 60)
    priv_key, pub_key = generate_rsa_keypair(2048)
    priv_pem, pub_pem = export_keys(priv_key)
    print(f"Private key (first 64 chars): {priv_pem[:64]}...")
    print(f"Public key (first 64 chars):  {pub_pem[:64]}...")
    print(f"Key size: {priv_key.key_size} bits")

    # --- Encryption (OAEP) ---
    print("\n" + "=" * 60)
    print("RSA-OAEP Encryption")
    print("=" * 60)
    message = b"ECU firmware update key: 0xDEADBEEF"
    ct = encrypt_oaep(pub_key, message)
    print(f"Plaintext:  {message}")
    print(f"Ciphertext: {ct.hex()[:80]}...")

    pt = decrypt_oaep(priv_key, ct)
    print(f"Decrypted:  {pt}")
    assert pt == message, "Decryption failed!"

    # --- Digital Signature (PSS) ---
    print("\n" + "=" * 60)
    print("RSA-PSS Digital Signature")
    print("=" * 60)
    firmware_hash_msg = b"firmware_v2.3.1_sha256:a1b2c3d4e5f6..."
    sig = sign_pss(priv_key, firmware_hash_msg)
    print(f"Message:   {firmware_hash_msg}")
    print(f"Signature: {sig.hex()[:80]}...")

    valid = verify_pss(pub_key, firmware_hash_msg, sig)
    print(f"Signature valid: {valid}")

    # Tampered message
    tampered = b"firmware_v2.3.1_sha256:TAMPERED_HASH..."
    valid_tampered = verify_pss(pub_key, tampered, sig)
    print(f"Tampered message signature valid: {valid_tampered}")
