"""
SLH-DSA (Stateless Hash-Based Digital Signature Algorithm) — formerly SPHINCS+
FIPS 205 Standard

Key properties:
- Based ONLY on hash functions (SHA-256, SHAKE) — no lattice math
- Conservative security assumption (hash function security is well-understood)
- Stateless (unlike XMSS/LMS which require state management)
- Very large signatures but tiny public keys
- Slow signing, moderate verification

Automotive relevance:
- Root certificate signatures (signed once, verified many times)
- Code signing for critical firmware (where signature size isn't bandwidth-limited)
- "Belt and suspenders" backup alongside ML-DSA
- Root of Trust key in HSM/OTP (only 32-64 bytes for public key!)

Dependencies: pip install oqs
"""

import time
import os

try:
    import oqs
    HAS_OQS = True
except ImportError:
    HAS_OQS = False
    print("⚠ liboqs not installed. Showing conceptual flow.\n")


def slh_dsa_demo():
    """SLH-DSA demonstration."""
    if not HAS_OQS:
        print("=" * 60)
        print("SLH-DSA (SPHINCS+) — Conceptual Overview")
        print("=" * 60)
        print("""
    SLH-DSA is unique among PQC signatures:

    ✓ Security based ONLY on hash function properties
    ✓ No number-theoretic assumptions (lattices, codes, etc.)
    ✓ Stateless — no counter management required
    ✓ Tiny public keys (32-64 bytes!)
    ✗ Very large signatures (8KB - 50KB)
    ✗ Slow signing (~100ms on desktop)

    Parameter sets (FIPS 205):
    ┌──────────────────┬────────┬──────────┬───────────┬──────────┐
    │ Parameter Set    │ SecLvl │ PK Size  │ Sig Size  │ Speed    │
    ├──────────────────┼────────┼──────────┼───────────┼──────────┤
    │ SLH-DSA-SHA2-128s│ 1      │ 32 B     │ 7856 B    │ Small/Slow│
    │ SLH-DSA-SHA2-128f│ 1      │ 32 B     │ 17088 B   │ Fast     │
    │ SLH-DSA-SHA2-192s│ 3      │ 48 B     │ 16224 B   │ Small/Slow│
    │ SLH-DSA-SHA2-192f│ 3      │ 48 B     │ 35664 B   │ Fast     │
    │ SLH-DSA-SHA2-256s│ 5      │ 64 B     │ 29792 B   │ Small/Slow│
    │ SLH-DSA-SHA2-256f│ 5      │ 64 B     │ 49856 B   │ Fast     │
    └──────────────────┴────────┴──────────┴───────────┴──────────┘

    's' variants: smaller signatures, slower signing
    'f' variants: faster signing, larger signatures
        """)
        return

    print("=" * 60)
    print("SLH-DSA (SPHINCS+) — Hash-Based Signatures")
    print("=" * 60)

    # Use SPHINCS+-SHA2-128s (smallest signatures)
    variant = "SPHINCS+-SHA2-128s-simple"
    signer = oqs.Signature(variant)
    public_key = signer.generate_keypair()

    print(f"Algorithm: {variant}")
    print(f"Public key size:  {len(public_key)} bytes  ← Tiny!")
    print(f"Secret key size:  {signer.details['length_secret_key']} bytes")

    # Sign
    message = b"Root CA certificate for vehicle fleet PKI - valid 2025-2045"
    start = time.perf_counter()
    signature = signer.sign(message)
    sign_time = time.perf_counter() - start

    print(f"\nMessage: {message}")
    print(f"Signature size: {len(signature)} bytes  ← Large!")
    print(f"Sign time: {sign_time*1000:.1f} ms")

    # Verify
    verifier = oqs.Signature(variant)
    start = time.perf_counter()
    is_valid = verifier.verify(message, signature, public_key)
    verify_time = time.perf_counter() - start

    print(f"Verify time: {verify_time*1000:.1f} ms")
    print(f"Valid: {is_valid}")

    # Compare all SPHINCS+ variants
    print("\n" + "-" * 40)
    print("All SLH-DSA Variants")
    print("-" * 40)
    sphincs_variants = [v for v in oqs.get_enabled_sig_mechanisms() if "SPHINCS" in v]
    for v in sphincs_variants[:6]:  # First 6
        s = oqs.Signature(v)
        pk = s.generate_keypair()
        sig = s.sign(b"test")
        print(f"  {v}: pk={len(pk)}B, sig={len(sig)}B")


if __name__ == "__main__":
    slh_dsa_demo()

    print("\n" + "=" * 60)
    print("When to Use SLH-DSA in Automotive")
    print("=" * 60)
    print("""
    BEST USE CASES:
    ✓ Root of Trust public key in OTP/eFuse (only 32B!)
    ✓ Root CA certificate signatures (signed once, stored)
    ✓ Long-term firmware signing keys
    ✓ Backup/fallback signature scheme alongside ML-DSA

    POOR USE CASES:
    ✗ V2X real-time message signing (too slow, signatures too large)
    ✗ CAN/CAN-FD authentication (no bandwidth)
    ✗ High-frequency operations

    IDEAL STRATEGY:
    - Root CA: SLH-DSA (maximum conservative security)
    - Intermediate CA: ML-DSA (practical for certificate chains)
    - End-entity (V2X, ECU): ML-DSA or hybrid ECDSA+ML-DSA
    """)
