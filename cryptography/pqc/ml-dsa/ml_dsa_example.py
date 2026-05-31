"""
ML-DSA (Module-Lattice Digital Signature Algorithm) — formerly Dilithium
FIPS 204 Standard

Demonstrates:
- Key generation
- Message signing
- Signature verification
- Comparison with ECDSA signature sizes

Automotive relevance:
- Quantum-safe firmware signing for secure boot
- Future V2X message authentication
- Long-lived code signing certificates
- OTA update package verification

Dependencies: pip install oqs (liboqs Python wrapper)
"""

import time
import os

try:
    import oqs
    HAS_OQS = True
except ImportError:
    HAS_OQS = False
    print("⚠ liboqs not installed. Install with: pip install oqs")
    print("  Falling back to simulation mode.\n")


def ml_dsa_demo_oqs():
    """ML-DSA using liboqs."""
    print("=" * 60)
    print("ML-DSA-65 (Dilithium3) — Digital Signatures")
    print("Using: liboqs (Open Quantum Safe)")
    print("=" * 60)

    # Key generation
    signer = oqs.Signature("Dilithium3")
    public_key = signer.generate_keypair()

    print(f"Public key size:  {len(public_key)} bytes")
    print(f"Secret key size:  {signer.details['length_secret_key']} bytes")

    # Sign a firmware image hash (simulated)
    firmware_metadata = b"firmware_v3.2.1|sha256:a1b2c3d4|ecu:gateway|date:2025-01-15"
    signature = signer.sign(firmware_metadata)

    print(f"\nMessage: {firmware_metadata}")
    print(f"Signature size: {len(signature)} bytes")
    print(f"Signature (first 64 bytes): {signature[:64].hex()}...")

    # Verify
    verifier = oqs.Signature("Dilithium3")
    is_valid = verifier.verify(firmware_metadata, signature, public_key)
    print(f"\n✓ Signature valid: {is_valid}")

    # Tampered message
    tampered = b"firmware_v3.2.1|sha256:MALICIOUS|ecu:gateway|date:2025-01-15"
    try:
        is_valid_tampered = verifier.verify(tampered, signature, public_key)
        print(f"✗ Tampered should fail: {is_valid_tampered}")
    except Exception:
        print("✓ Tampered message correctly rejected")

    # Benchmark
    print("\n" + "-" * 40)
    print("Performance Benchmark")
    print("-" * 40)
    iterations = 100

    start = time.perf_counter()
    for _ in range(iterations):
        s = oqs.Signature("Dilithium3")
        pk = s.generate_keypair()
    keygen_time = (time.perf_counter() - start) / iterations

    start = time.perf_counter()
    for _ in range(iterations):
        s.sign(firmware_metadata)
    sign_time = (time.perf_counter() - start) / iterations

    sig = s.sign(firmware_metadata)
    v = oqs.Signature("Dilithium3")
    start = time.perf_counter()
    for _ in range(iterations):
        v.verify(firmware_metadata, sig, pk)
    verify_time = (time.perf_counter() - start) / iterations

    print(f"  KeyGen: {keygen_time*1000:.3f} ms")
    print(f"  Sign:   {sign_time*1000:.3f} ms")
    print(f"  Verify: {verify_time*1000:.3f} ms")

    # All parameter sets
    print("\n" + "-" * 40)
    print("ML-DSA Parameter Comparison")
    print("-" * 40)
    for variant in ["Dilithium2", "Dilithium3", "Dilithium5"]:
        s = oqs.Signature(variant)
        pk = s.generate_keypair()
        sig = s.sign(b"test")
        print(f"  {variant}: pk={len(pk)}B, sig={len(sig)}B")


def ml_dsa_demo_simulation():
    """Simulated ML-DSA for understanding."""
    print("=" * 60)
    print("ML-DSA-65 (Dilithium3) — Simulated Flow")
    print("(Install liboqs for real implementation)")
    print("=" * 60)

    print("""
    ML-DSA Secure Boot Flow:

    ┌──────────────────────────────────────────────────────────┐
    │                 BUILD SERVER (Signing)                     │
    ├──────────────────────────────────────────────────────────┤
    │  1. Compile firmware binary                               │
    │  2. Hash firmware: h = SHA-256(firmware)                  │
    │  3. Sign: sig = ML-DSA.Sign(signing_key, h)              │
    │  4. Package: [firmware || sig || certificate]             │
    └──────────────────────┬───────────────────────────────────┘
                           │ OTA Download
                           ▼
    ┌──────────────────────────────────────────────────────────┐
    │                    ECU (Verification)                      │
    ├──────────────────────────────────────────────────────────┤
    │  1. Receive [firmware || sig || certificate]              │
    │  2. Validate certificate chain (root key in HSM/OTP)     │
    │  3. Extract public key from certificate                   │
    │  4. Hash received firmware: h' = SHA-256(firmware)        │
    │  5. Verify: ML-DSA.Verify(public_key, h', sig)           │
    │  6. If valid → flash firmware; else → reject + alert     │
    └──────────────────────────────────────────────────────────┘
    """)

    # Simulated sizes
    print("Size comparison (secure boot signature):")
    print(f"  ECDSA P-256:    pk=64B,   sig=64B    (current)")
    print(f"  RSA-2048:       pk=256B,  sig=256B   (legacy)")
    print(f"  ML-DSA-44:      pk=1312B, sig=2420B  (PQC Level 2)")
    print(f"  ML-DSA-65:      pk=1952B, sig=3293B  (PQC Level 3)")
    print(f"  ML-DSA-87:      pk=2592B, sig=4595B  (PQC Level 5)")
    print(f"\n  Impact: ~50x larger signatures than ECDSA")
    print(f"  Requires: Sufficient flash for keys + signatures")
    print(f"  Solution: Store root PQC key in secure element/HSM")


if __name__ == "__main__":
    if HAS_OQS:
        ml_dsa_demo_oqs()
    else:
        ml_dsa_demo_simulation()

    print("\n" + "=" * 60)
    print("Automotive Migration Strategy")
    print("=" * 60)
    print("""
    Phase 1 — Hybrid Signatures (NOW):
      signature = ECDSA_Sign(msg) || ML-DSA_Sign(msg)
      verify = ECDSA_Verify(msg, sig1) AND ML-DSA_Verify(msg, sig2)
      → Secure against both classical and quantum attacks

    Phase 2 — PQC-only (2030+):
      Once confidence in PQC is established and hardware supports it

    Challenges for Automotive:
    - Flash/RAM constraints on MCU-class ECUs (Cortex-M)
    - ML-DSA verification is ~10x slower than ECDSA on constrained HW
    - CAN bus cannot carry PQC signatures (need Ethernet backbone)
    - V2X: 3KB signatures × 2000 msgs/sec = 6 MB/s bandwidth
    - Certificate revocation lists grow with larger certificates
    """)
