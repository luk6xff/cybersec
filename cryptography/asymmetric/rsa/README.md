# RSA (Rivest-Shamir-Adleman)

## Overview
RSA is based on the difficulty of factoring the product of two large prime numbers. While being replaced by ECC in many modern applications, RSA remains prevalent in:
- X.509 certificates (root CAs often use RSA-4096)
- Legacy automotive ECU secure boot (older HPSE implementations)
- Code signing for firmware updates

## Key Points
- **Minimum key size**: 2048 bits (NIST recommendation through 2030)
- **Recommended**: 3072+ bits for protection beyond 2030
- **Encryption padding**: OAEP (PKCS#1 v2) — NEVER use PKCS#1 v1.5 for new systems
- **Signature padding**: PSS — provides provable security reduction

## Automotive Use Cases
1. **Secure Boot**: Verify firmware authenticity using RSA-2048/4096 signatures
2. **OTA Updates**: Server signs update packages; ECU verifies before flashing
3. **Certificate-based authentication**: UDS 0x29 role-based access

## Run
```bash
pip install cryptography
python rsa_example.py
```

## Common Vulnerabilities
| Vulnerability | Impact | Mitigation |
|--------------|--------|------------|
| Bleichenbacher (PKCS#1 v1.5) | Plaintext recovery | Use OAEP |
| Small public exponent + no padding | Root attack | Always pad, use e=65537 |
| Common modulus attack | Key recovery | Unique modulus per key pair |
| Timing side-channel | Key leakage | Constant-time implementation |
