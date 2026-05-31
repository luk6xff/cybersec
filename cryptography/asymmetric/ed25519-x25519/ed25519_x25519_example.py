"""
Ed25519 & X25519 — Modern Curve Cryptography

Ed25519: Edwards-curve Digital Signature Algorithm (EdDSA)
X25519:  Diffie-Hellman key exchange on Curve25519

Why modern curves?
- Constant-time by design (resistant to timing side-channels)
- Deterministic signatures (no random nonce — immune to nonce reuse attacks)
- Faster than P-256 ECDSA on most platforms
- Simple, auditable implementations

Automotive relevance:
- WireGuard VPN tunnels (backend connectivity)
- Signal Protocol (V2X privacy)
- Modern TLS libraries support X25519 key exchange
- Emerging use in next-gen V2X (not yet standardized in IEEE 1609.2)

Dependencies: pip install cryptography
"""

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import time


# ============================================================
# Ed25519 — Digital Signatures
# ============================================================

def ed25519_demo():
    print("=" * 60)
    print("Ed25519 Digital Signatures")
    print("=" * 60)

    # Key generation
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Export keys
    pub_raw = public_key.public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw
    )
    print(f"Public key (32 bytes): {pub_raw.hex()}")

    # Sign
    message = b"ECU diagnostic session token: session_id=0x1234ABCD"
    signature = private_key.sign(message)
    print(f"\nMessage: {message}")
    print(f"Signature (64 bytes): {signature.hex()}")

    # Verify
    try:
        public_key.verify(signature, message)
        print("✓ Signature valid")
    except Exception:
        print("✗ Signature invalid")

    # Tampered message
    try:
        public_key.verify(signature, b"TAMPERED")
        print("✗ Should not reach here")
    except Exception:
        print("✓ Tampered message correctly rejected")

    # Benchmark
    iterations = 1000
    start = time.perf_counter()
    for _ in range(iterations):
        private_key.sign(message)
    sign_time = (time.perf_counter() - start) / iterations

    start = time.perf_counter()
    for _ in range(iterations):
        public_key.verify(signature, message)
    verify_time = (time.perf_counter() - start) / iterations

    print(f"\nBenchmark ({iterations} iterations):")
    print(f"  Sign:   {sign_time*1000:.3f} ms/op ({1/sign_time:.0f} ops/sec)")
    print(f"  Verify: {verify_time*1000:.3f} ms/op ({1/verify_time:.0f} ops/sec)")


# ============================================================
# X25519 — Key Exchange
# ============================================================

def x25519_demo():
    print("\n" + "=" * 60)
    print("X25519 Key Exchange")
    print("=" * 60)

    # Alice (e.g., ECU)
    alice_private = X25519PrivateKey.generate()
    alice_public = alice_private.public_key()

    # Bob (e.g., Backend Server)
    bob_private = X25519PrivateKey.generate()
    bob_public = bob_private.public_key()

    # Export public keys (32 bytes each)
    alice_pub_raw = alice_public.public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw
    )
    bob_pub_raw = bob_public.public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw
    )
    print(f"Alice public key: {alice_pub_raw.hex()}")
    print(f"Bob public key:   {bob_pub_raw.hex()}")

    # Key exchange
    alice_shared = alice_private.exchange(bob_public)
    bob_shared = bob_private.exchange(alice_public)

    assert alice_shared == bob_shared
    print(f"\nShared secret (32 bytes): {alice_shared.hex()}")
    print("✓ Both parties derived the same shared secret")

    # Derive application keys using HKDF
    session_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"wireguard-tunnel-key",
    ).derive(alice_shared)
    print(f"\nDerived session key: {session_key.hex()}")

    # Benchmark
    iterations = 1000
    start = time.perf_counter()
    for _ in range(iterations):
        alice_private.exchange(bob_public)
    exchange_time = (time.perf_counter() - start) / iterations
    print(f"\nKey exchange benchmark: {exchange_time*1000:.3f} ms/op ({1/exchange_time:.0f} ops/sec)")


# ============================================================
# Comparison Table
# ============================================================

def print_comparison():
    print("\n" + "=" * 60)
    print("Comparison: Ed25519/X25519 vs ECDSA/ECDH (P-256)")
    print("=" * 60)
    print("""
    ┌─────────────────┬──────────────────┬──────────────────┐
    │ Property        │ Ed25519/X25519   │ ECDSA/ECDH P-256 │
    ├─────────────────┼──────────────────┼──────────────────┤
    │ Key size        │ 32 bytes         │ 32 bytes         │
    │ Signature size  │ 64 bytes         │ ~72 bytes (DER)  │
    │ Deterministic   │ Yes              │ No (needs RFC6979│
    │ Constant-time   │ By design        │ Implementation   │
    │ Standards       │ RFC 8032/7748    │ FIPS 186-4       │
    │ V2X (IEEE1609)  │ Not yet          │ Mandatory        │
    │ TLS 1.3         │ Supported        │ Supported        │
    │ FIPS certified  │ Limited          │ Yes              │
    │ HSM support     │ Growing          │ Widespread       │
    └─────────────────┴──────────────────┴──────────────────┘

    Recommendation for automotive:
    - Use P-256 where standards mandate (V2X, ISO 15118)
    - Use Ed25519/X25519 for internal/backend communications
    - Evaluate migration path for post-quantum transition
    """)


if __name__ == "__main__":
    ed25519_demo()
    x25519_demo()
    print_comparison()
