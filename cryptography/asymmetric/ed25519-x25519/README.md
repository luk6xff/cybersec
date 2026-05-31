# Ed25519 / X25519 (Modern Curve Cryptography)

## Overview
Daniel J. Bernstein's Curve25519 family provides high-speed, high-security cryptography with implementation safety built into the design.

| Algorithm | Function | RFC |
|-----------|----------|-----|
| Ed25519 | Digital signature (EdDSA) | RFC 8032 |
| X25519 | Key exchange (DH) | RFC 7748 |

## Why Modern Curves?

| Property | NIST P-256 | Curve25519 |
|----------|-----------|------------|
| Constant-time | Implementation effort | By design |
| Deterministic signing | Requires RFC 6979 | Built-in |
| Twist security | No | Yes |
| Patent-free | Yes | Yes |
| Implementation complexity | Higher | Lower |
| Misuse resistance | Lower | Higher |

## Where Used

- **WireGuard** VPN (X25519 + ChaCha20-Poly1305)
- **Signal Protocol** (X25519 + AES-GCM)
- **SSH** (Ed25519 keys, default in modern OpenSSH)
- **TLS 1.3** (X25519 key exchange, most popular curve)
- **age** encryption tool
- **Minisign** code signing

## Automotive Applicability
- Backend-to-backend communication (not yet standardized for V2X)
- Internal tooling and development infrastructure
- Emerging consideration for next-gen V2X standards
- WireGuard tunnels for remote diagnostics

## Run
```bash
pip install cryptography
python ed25519_x25519_example.py
```
