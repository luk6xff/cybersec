# Asymmetric Cryptography

Asymmetric (public-key) cryptography uses mathematically related key pairs: a **private key** (kept secret) and a **public key** (shared openly). This enables encryption, digital signatures, and key agreement without pre-shared secrets.

## Core Algorithms

| Algorithm | Type | Key Size | Use Case |
|-----------|------|----------|----------|
| RSA | Encryption/Signature | 2048-4096 bit | Legacy systems, certificates |
| ECDSA | Signature | 256-521 bit curves | TLS, code signing, automotive |
| ECDH | Key Agreement | 256-521 bit curves | TLS key exchange, V2X |
| Ed25519 | Signature | 256 bit (Curve25519) | SSH, modern protocols |
| X25519 | Key Agreement | 256 bit (Curve25519) | WireGuard, Signal, TLS 1.3 |

## Automotive Relevance

- **SecOC key distribution** often relies on asymmetric schemes for initial key provisioning
- **Secure Boot** uses RSA/ECDSA to verify firmware signatures
- **V2X (IEEE 1609.2)** mandates ECDSA with NIST P-256 for message signing
- **UDS 0x29** uses PKI-based certificates for role-based diagnostic access
- **ISO 15118** uses TLS with ECDH for Plug & Charge

## Examples

- [RSA Encryption & Signing](rsa/)
- [ECDSA Signing & Verification](ecdsa/)
- [ECDH Key Exchange](ecdh/)
- [Ed25519 / X25519 Modern Curves](ed25519-x25519/)

## Security Considerations

1. **Key sizes**: RSA < 2048 bits is broken. Prefer ECDSA P-256+ or Ed25519.
2. **Padding**: RSA must use OAEP (encryption) or PSS (signing). PKCS#1 v1.5 is vulnerable to Bleichenbacher attacks.
3. **Nonce reuse**: ECDSA with repeated nonces leaks the private key (see PlayStation 3 hack).
4. **Side-channel**: Constant-time implementations are mandatory in embedded/automotive.
5. **Quantum threat**: All classical asymmetric crypto is broken by Shor's algorithm — see PQC section.
