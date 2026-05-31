# ECDH (Elliptic Curve Diffie-Hellman)

## Overview
ECDH enables two parties to establish a shared secret over an insecure channel. Combined with a KDF (Key Derivation Function), it produces symmetric keys for encryption and authentication.

## Variants

| Variant | Forward Secrecy | Use Case |
|---------|----------------|----------|
| Static ECDH | No | Device identity, long-lived associations |
| Ephemeral ECDH (ECDHE) | Yes | TLS 1.3, OTA sessions |
| Semi-static (one ephemeral) | Partial | Some IoT protocols |

## Key Derivation — CRITICAL

**NEVER use the raw ECDH shared secret directly as a key.**

The raw output has structure (it's a point coordinate) and lacks uniformity. Always apply:
- **HKDF** (RFC 5869) — recommended for most applications
- **NIST SP 800-56C** (two-step KDF) — required for FIPS compliance
- **X9.63 KDF** — used in some automotive standards

## Automotive Applications

1. **TLS for OTA**: ECDHE in TLS 1.3 handshake between ECU and update server
2. **ISO 15118**: TLS mutual auth between EV and charging station
3. **Key Provisioning**: Derive SecOC symmetric keys via ECDH + KDF
4. **V2X Session Keys**: Encrypted V2X communication channels

## Run
```bash
pip install cryptography
python ecdh_example.py
```
