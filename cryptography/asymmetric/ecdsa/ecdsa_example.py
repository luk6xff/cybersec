"""
ECDSA (Elliptic Curve Digital Signature Algorithm) Example

Demonstrates:
- Key generation on NIST P-256 (secp256r1) — mandatory for V2X/IEEE 1609.2
- Message signing and verification
- DER-encoded signature handling

Automotive relevance:
- V2X BSM (Basic Safety Message) signing
- Secure boot signature verification
- ISO 15118 Plug & Charge certificate signatures

Dependencies: pip install cryptography
"""

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
import time


def generate_ecdsa_keypair(curve=ec.SECP256R1()):
    """Generate ECDSA key pair on specified curve."""
    private_key = ec.generate_private_key(curve)
    return private_key, private_key.public_key()


def sign_message(private_key, message: bytes) -> bytes:
    """Sign a message using ECDSA with SHA-256."""
    signature = private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256())
    )
    return signature


def verify_signature(public_key, message: bytes, signature: bytes) -> bool:
    """Verify an ECDSA signature."""
    try:
        public_key.verify(
            signature,
            message,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except Exception:
        return False


def benchmark_ecdsa(iterations: int = 100):
    """Benchmark ECDSA sign/verify operations (relevant for real-time automotive)."""
    private_key, public_key = generate_ecdsa_keypair()
    message = b"V2X Basic Safety Message - Position: 48.1234, 11.5678, Speed: 60km/h"

    # Sign benchmark
    start = time.perf_counter()
    for _ in range(iterations):
        sig = sign_message(private_key, message)
    sign_time = (time.perf_counter() - start) / iterations

    # Verify benchmark
    start = time.perf_counter()
    for _ in range(iterations):
        verify_signature(public_key, message, sig)
    verify_time = (time.perf_counter() - start) / iterations

    return sign_time, verify_time


if __name__ == "__main__":
    # --- Key Generation ---
    print("=" * 60)
    print("ECDSA Key Generation (NIST P-256 / secp256r1)")
    print("=" * 60)
    priv_key, pub_key = generate_ecdsa_keypair()

    # Export public key
    pub_pem = pub_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    print(f"Public Key (PEM):\n{pub_pem.decode()}")

    # Get raw public key coordinates
    pub_numbers = pub_key.public_numbers()
    print(f"Public Key X: {pub_numbers.x:064x}")
    print(f"Public Key Y: {pub_numbers.y:064x}")

    # --- Sign a V2X-like message ---
    print("\n" + "=" * 60)
    print("ECDSA Signing (V2X BSM Example)")
    print("=" * 60)
    bsm_payload = b"BSM|lat:48.1234|lon:11.5678|spd:60|hdg:180|ts:1700000000"
    signature = sign_message(priv_key, bsm_payload)

    # Decode DER signature to (r, s) components
    r, s = decode_dss_signature(signature)
    print(f"Message: {bsm_payload}")
    print(f"Signature (DER): {signature.hex()}")
    print(f"  r = {r:064x}")
    print(f"  s = {s:064x}")

    # --- Verify ---
    print("\n" + "=" * 60)
    print("ECDSA Verification")
    print("=" * 60)
    valid = verify_signature(pub_key, bsm_payload, signature)
    print(f"Valid signature: {valid}")

    # Tampered payload
    tampered = b"BSM|lat:48.1234|lon:11.5678|spd:200|hdg:180|ts:1700000000"
    valid_tampered = verify_signature(pub_key, tampered, signature)
    print(f"Tampered payload valid: {valid_tampered}")

    # --- Performance Benchmark ---
    print("\n" + "=" * 60)
    print("ECDSA Performance Benchmark (P-256)")
    print("=" * 60)
    sign_t, verify_t = benchmark_ecdsa(500)
    print(f"Average sign time:   {sign_t*1000:.3f} ms")
    print(f"Average verify time: {verify_t*1000:.3f} ms")
    print(f"Sign throughput:     {1/sign_t:.0f} ops/sec")
    print(f"Verify throughput:   {1/verify_t:.0f} ops/sec")
    print(f"\nNote: V2X requires verifying ~1000-2000 BSMs/sec in dense traffic")

    # --- Multiple curves comparison ---
    print("\n" + "=" * 60)
    print("Curve Comparison")
    print("=" * 60)
    curves = [
        ("P-256 (secp256r1)", ec.SECP256R1()),
        ("P-384 (secp384r1)", ec.SECP384R1()),
        ("P-521 (secp521r1)", ec.SECP521R1()),
    ]
    for name, curve in curves:
        pk, _ = generate_ecdsa_keypair(curve)
        priv_size = pk.key_size
        print(f"  {name}: key size = {priv_size} bits")
