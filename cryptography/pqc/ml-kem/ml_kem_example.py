"""
ML-KEM (Module-Lattice Key Encapsulation Mechanism) — formerly Kyber
FIPS 203 Standard

Demonstrates:
- Key generation
- Encapsulation (sender creates ciphertext + shared secret)
- Decapsulation (receiver recovers shared secret)

This is a KEM, not traditional encryption:
- Encaps: generates random shared secret + ciphertext
- Decaps: recovers same shared secret from ciphertext + private key
- The shared secret is then used with a symmetric cipher (AES-GCM)

Automotive relevance:
- Quantum-safe key exchange for OTA update channels
- Future V2X key agreement
- Backend-to-vehicle secure session establishment
- Long-term key encapsulation for certificate provisioning

Dependencies: pip install pqcrypto
Alternative:  pip install oqs (liboqs Python wrapper)

NOTE: As of 2024, use liboqs for production-grade PQC.
      The 'cryptography' library is adding PQC support incrementally.
"""

import os
import hashlib
import time

# Try to use oqs (Open Quantum Safe) - the reference implementation
try:
    import oqs
    HAS_OQS = True
except ImportError:
    HAS_OQS = False
    print("⚠ liboqs not installed. Install with: pip install oqs")
    print("  Or build from: https://github.com/open-quantum-safe/liboqs-python")
    print("  Falling back to simulation mode.\n")


def ml_kem_demo_oqs():
    """ML-KEM using liboqs (production-grade implementation)."""
    print("=" * 60)
    print("ML-KEM-768 (Kyber) — Key Encapsulation")
    print("Using: liboqs (Open Quantum Safe)")
    print("=" * 60)

    # Key generation (receiver side — e.g., ECU)
    kem = oqs.KeyEncapsulation("Kyber768")
    public_key = kem.generate_keypair()

    print(f"Public key size:  {len(public_key)} bytes")
    print(f"Secret key size:  {kem.details['length_secret_key']} bytes")
    print(f"Public key (hex): {public_key[:32].hex()}...")

    # Encapsulation (sender side — e.g., OTA Backend)
    # Sender uses receiver's public key to create:
    #   1. A ciphertext (to send to receiver)
    #   2. A shared secret (known only to sender until receiver decapsulates)
    ciphertext, shared_secret_sender = kem.encap_secret(public_key)

    print(f"\nCiphertext size:  {len(ciphertext)} bytes")
    print(f"Shared secret:    {shared_secret_sender.hex()}")

    # Decapsulation (receiver side — e.g., ECU)
    # Receiver uses their private key + ciphertext to recover the same shared secret
    shared_secret_receiver = kem.decap_secret(ciphertext)

    print(f"Recovered secret: {shared_secret_receiver.hex()}")

    assert shared_secret_sender == shared_secret_receiver
    print("\n✓ Key encapsulation successful — both parties share the same secret")

    # Benchmark
    print("\n" + "-" * 40)
    print("Performance Benchmark (ML-KEM-768)")
    print("-" * 40)
    iterations = 100

    # KeyGen
    start = time.perf_counter()
    for _ in range(iterations):
        kem2 = oqs.KeyEncapsulation("Kyber768")
        pk = kem2.generate_keypair()
    keygen_time = (time.perf_counter() - start) / iterations

    # Encaps
    start = time.perf_counter()
    for _ in range(iterations):
        kem2.encap_secret(pk)
    encaps_time = (time.perf_counter() - start) / iterations

    # Decaps
    ct, _ = kem2.encap_secret(pk)
    start = time.perf_counter()
    for _ in range(iterations):
        kem2.decap_secret(ct)
    decaps_time = (time.perf_counter() - start) / iterations

    print(f"  KeyGen:  {keygen_time*1000:.3f} ms")
    print(f"  Encaps:  {encaps_time*1000:.3f} ms")
    print(f"  Decaps:  {decaps_time*1000:.3f} ms")

    # Compare parameter sets
    print("\n" + "-" * 40)
    print("ML-KEM Parameter Comparison")
    print("-" * 40)
    for variant in ["Kyber512", "Kyber768", "Kyber1024"]:
        k = oqs.KeyEncapsulation(variant)
        pk = k.generate_keypair()
        ct, ss = k.encap_secret(pk)
        print(f"  {variant}: pk={len(pk)}B, ct={len(ct)}B, ss={len(ss)}B")


def ml_kem_demo_simulation():
    """Simulated ML-KEM flow for understanding (no real PQC math)."""
    print("=" * 60)
    print("ML-KEM-768 (Kyber) — Simulated Flow")
    print("(Install liboqs for real implementation)")
    print("=" * 60)

    print("""
    ML-KEM Protocol Flow:

    ┌─────────────┐                    ┌─────────────┐
    │   ECU       │                    │  OTA Server │
    │ (Receiver)  │                    │  (Sender)   │
    └──────┬──────┘                    └──────┬──────┘
           │                                   │
           │  1. KeyGen() → (pk, sk)           │
           │──────── pk ─────────────────────→│
           │                                   │
           │                 2. Encaps(pk) → (ct, ss)
           │←─────── ct ─────────────────────│
           │                                   │
           │  3. Decaps(sk, ct) → ss           │
           │                                   │
           │  Both now share 'ss' (32 bytes)   │
           │  Use ss as AES-256-GCM key        │
           └───────────────────────────────────┘
    """)

    # Simulate with random values for demonstration
    pk_size = 1184  # ML-KEM-768 public key
    ct_size = 1088  # ML-KEM-768 ciphertext
    ss_size = 32    # Shared secret

    pk = os.urandom(pk_size)
    ct = os.urandom(ct_size)
    ss = os.urandom(ss_size)

    print(f"Public key size:  {pk_size} bytes")
    print(f"Ciphertext size:  {ct_size} bytes")
    print(f"Shared secret:    {ss.hex()}")
    print(f"\nNote: These are random values for demonstration.")
    print(f"Install liboqs for real ML-KEM: pip install oqs")


if __name__ == "__main__":
    if HAS_OQS:
        ml_kem_demo_oqs()
    else:
        ml_kem_demo_simulation()

    print("\n" + "=" * 60)
    print("Usage in Automotive Context")
    print("=" * 60)
    print("""
    1. OTA Firmware Update:
       - Vehicle ECU has ML-KEM key pair in HSM
       - Backend encapsulates session key using ECU's public key
       - ECU decapsulates to get session key
       - Firmware is encrypted with AES-256-GCM using session key

    2. Hybrid Key Exchange (recommended during transition):
       - Perform BOTH X25519 and ML-KEM-768
       - Combine shared secrets: final_key = KDF(x25519_ss || mlkem_ss)
       - Secure even if one scheme is broken

    3. Certificate Provisioning:
       - V2X certificates contain ML-KEM public keys
       - Allows quantum-safe key agreement for encrypted V2X
    """)
