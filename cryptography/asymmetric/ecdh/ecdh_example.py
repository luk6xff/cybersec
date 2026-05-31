"""
ECDH (Elliptic Curve Diffie-Hellman) Key Exchange Example

Demonstrates:
- ECDH key agreement on P-256
- Deriving symmetric keys using HKDF
- Simulating a TLS-like key exchange between ECU and backend

Automotive relevance:
- TLS session establishment for OTA updates
- ISO 15118 TLS between EV and EVSE
- V2X encrypted communication channels
- Key agreement for SecOC key provisioning

Dependencies: pip install cryptography
"""

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import os


def generate_ecdh_keypair(curve=ec.SECP256R1()):
    """Generate ECDH key pair."""
    private_key = ec.generate_private_key(curve)
    return private_key, private_key.public_key()


def perform_key_exchange(private_key, peer_public_key) -> bytes:
    """Perform ECDH to get raw shared secret."""
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
    return shared_secret


def derive_key(shared_secret: bytes, info: bytes, salt: bytes = None, length: int = 32) -> bytes:
    """
    Derive a symmetric key from ECDH shared secret using HKDF.

    NEVER use the raw ECDH output directly as a key!
    Always use a proper KDF (HKDF, NIST SP 800-56C).
    """
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        info=info,
    ).derive(shared_secret)
    return derived_key


if __name__ == "__main__":
    # --- Scenario: ECU ↔ OTA Backend Key Exchange ---
    print("=" * 60)
    print("ECDH Key Exchange: ECU ↔ OTA Backend")
    print("=" * 60)

    # ECU generates ephemeral key pair
    ecu_private, ecu_public = generate_ecdh_keypair()
    print("ECU generated ephemeral ECDH key pair (P-256)")

    # Backend generates ephemeral key pair
    backend_private, backend_public = generate_ecdh_keypair()
    print("Backend generated ephemeral ECDH key pair (P-256)")

    # Exchange public keys (in real life, authenticated via TLS/certificates)
    ecu_pub_bytes = ecu_public.public_bytes(
        serialization.Encoding.X962,
        serialization.PublicFormat.UncompressedPoint
    )
    backend_pub_bytes = backend_public.public_bytes(
        serialization.Encoding.X962,
        serialization.PublicFormat.UncompressedPoint
    )
    print(f"\nECU Public Key (uncompressed): {ecu_pub_bytes.hex()[:80]}...")
    print(f"Backend Public Key (uncompressed): {backend_pub_bytes.hex()[:80]}...")

    # --- Compute shared secrets ---
    print("\n" + "=" * 60)
    print("Shared Secret Computation")
    print("=" * 60)

    ecu_shared = perform_key_exchange(ecu_private, backend_public)
    backend_shared = perform_key_exchange(backend_private, ecu_public)

    print(f"ECU computed shared secret:     {ecu_shared.hex()}")
    print(f"Backend computed shared secret:  {backend_shared.hex()}")
    assert ecu_shared == backend_shared, "Key exchange failed!"
    print("\n✓ Both parties derived the same shared secret")

    # --- Key Derivation ---
    print("\n" + "=" * 60)
    print("Key Derivation (HKDF-SHA256)")
    print("=" * 60)

    # Derive separate keys for different purposes
    salt = os.urandom(32)  # In practice, can be a session-specific value

    # Encryption key for firmware download
    enc_key = derive_key(
        ecu_shared,
        info=b"firmware-download-encryption-key",
        salt=salt,
        length=32
    )
    print(f"Firmware encryption key (AES-256): {enc_key.hex()}")

    # MAC key for integrity
    mac_key = derive_key(
        ecu_shared,
        info=b"firmware-download-mac-key",
        salt=salt,
        length=32
    )
    print(f"Firmware MAC key (HMAC-SHA256):    {mac_key.hex()}")

    # --- Ephemeral vs Static ECDH ---
    print("\n" + "=" * 60)
    print("Forward Secrecy with Ephemeral Keys")
    print("=" * 60)
    print("""
    Static ECDH:  Same key pair used across sessions
                  → Compromise of private key decrypts ALL past sessions

    Ephemeral ECDH (ECDHE): Fresh key pair per session
                  → Compromise of one session key affects only that session
                  → Provides Perfect Forward Secrecy (PFS)

    TLS 1.3 ONLY supports ECDHE (ephemeral) — no static DH allowed.

    Automotive best practice:
    - Use ECDHE for OTA download sessions
    - Static ECDH acceptable for long-lived device identity (with HSM protection)
    """)
