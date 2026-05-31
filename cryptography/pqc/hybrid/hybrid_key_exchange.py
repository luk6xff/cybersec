"""
Hybrid Key Exchange: X25519 + ML-KEM-768

Combines classical (X25519) and post-quantum (ML-KEM) key exchange.
The final shared secret is derived from BOTH — secure even if one is broken.

This is the recommended approach during the PQC transition period.
Used in: TLS 1.3 (draft-ietf-tls-hybrid-design), Signal Protocol, WireGuard PQ.

Automotive use case:
- OTA update channel between ECU and backend
- Secure even against "harvest now, decrypt later" quantum attacks
- Backwards-compatible with existing TLS infrastructure

Dependencies: pip install cryptography oqs
"""

from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import hashlib
import os

try:
    import oqs
    HAS_OQS = True
except ImportError:
    HAS_OQS = False


def hybrid_key_exchange():
    """
    Perform hybrid X25519 + ML-KEM-768 key exchange.

    Protocol:
    1. Both parties do X25519 key exchange → ss_classical
    2. Sender encapsulates with ML-KEM using receiver's PQC public key → ss_pqc
    3. Combine: shared_secret = KDF(ss_classical || ss_pqc)
    """
    print("=" * 60)
    print("Hybrid Key Exchange: X25519 + ML-KEM-768")
    print("=" * 60)

    # === RECEIVER (ECU) SETUP ===
    print("\n[ECU] Generating key pairs...")

    # Classical: X25519
    ecu_x25519_private = X25519PrivateKey.generate()
    ecu_x25519_public = ecu_x25519_private.public_key()
    ecu_x25519_pub_bytes = ecu_x25519_public.public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw
    )

    # PQC: ML-KEM-768
    if HAS_OQS:
        ecu_kem = oqs.KeyEncapsulation("Kyber768")
        ecu_kem_public = ecu_kem.generate_keypair()
    else:
        ecu_kem_public = os.urandom(1184)  # Simulated

    print(f"  X25519 public key: {ecu_x25519_pub_bytes.hex()}")
    print(f"  ML-KEM-768 public key: {ecu_kem_public[:32].hex()}... ({len(ecu_kem_public)}B)")

    # === SENDER (BACKEND) SETUP ===
    print("\n[Backend] Generating ephemeral X25519 key pair...")

    backend_x25519_private = X25519PrivateKey.generate()
    backend_x25519_public = backend_x25519_private.public_key()
    backend_x25519_pub_bytes = backend_x25519_public.public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw
    )
    print(f"  X25519 public key: {backend_x25519_pub_bytes.hex()}")

    # === KEY EXCHANGE ===
    print("\n[Key Exchange]")

    # Step 1: X25519 shared secret
    backend_x25519_ss = backend_x25519_private.exchange(ecu_x25519_public)
    ecu_x25519_ss = ecu_x25519_private.exchange(backend_x25519_public)
    assert backend_x25519_ss == ecu_x25519_ss
    print(f"  X25519 shared secret: {backend_x25519_ss.hex()}")

    # Step 2: ML-KEM encapsulation
    if HAS_OQS:
        kem_ciphertext, backend_kem_ss = ecu_kem.encap_secret(ecu_kem_public)
        ecu_kem_ss = ecu_kem.decap_secret(kem_ciphertext)
        assert backend_kem_ss == ecu_kem_ss
    else:
        # Simulation
        kem_ciphertext = os.urandom(1088)
        backend_kem_ss = os.urandom(32)
        ecu_kem_ss = backend_kem_ss  # In simulation, same value

    print(f"  ML-KEM shared secret: {backend_kem_ss.hex()}")
    print(f"  ML-KEM ciphertext:    {kem_ciphertext[:32].hex()}... ({len(kem_ciphertext)}B)")

    # Step 3: Combine shared secrets with KDF
    # CRITICAL: Concatenate both shared secrets and derive final key
    combined_ss = backend_x25519_ss + backend_kem_ss

    # Use HKDF to derive the final session key
    final_key_backend = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"hybrid-x25519-mlkem768-session-key",
    ).derive(combined_ss)

    combined_ss_ecu = ecu_x25519_ss + ecu_kem_ss
    final_key_ecu = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"hybrid-x25519-mlkem768-session-key",
    ).derive(combined_ss_ecu)

    assert final_key_backend == final_key_ecu
    print(f"\n  Final hybrid session key: {final_key_backend.hex()}")
    print("  ✓ Both parties derived the same key")

    # === SECURITY ANALYSIS ===
    print("\n" + "=" * 60)
    print("Security Properties")
    print("=" * 60)
    print("""
    Scenario 1: Classical computer breaks ML-KEM
      → X25519 still provides 128-bit security
      → Session remains confidential

    Scenario 2: Quantum computer breaks X25519 (Shor's)
      → ML-KEM-768 provides NIST Level 3 security
      → Session remains confidential

    Scenario 3: Both broken simultaneously
      → Extremely unlikely with current understanding
      → Would require breakthrough in BOTH lattice AND ECDLP

    Wire format overhead:
      Classical only:  32B (X25519 public key)
      Hybrid:          32B + 1184B (X25519 + ML-KEM public key) = 1216B
                       + 1088B ciphertext in response
      → ~2.3KB additional per handshake (acceptable for OTA/TLS)
    """)


if __name__ == "__main__":
    hybrid_key_exchange()
