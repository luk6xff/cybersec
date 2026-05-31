# ECDSA (Elliptic Curve Digital Signature Algorithm)

## Overview
ECDSA provides equivalent security to RSA with significantly smaller key sizes, making it the preferred algorithm for resource-constrained automotive ECUs and real-time systems like V2X.

| Security Level | RSA Key Size | ECDSA Key Size | Advantage |
|---------------|-------------|----------------|-----------|
| 128-bit | 3072 bits | 256 bits | 12x smaller |
| 192-bit | 7680 bits | 384 bits | 20x smaller |
| 256-bit | 15360 bits | 521 bits | 30x smaller |

## Curves Used in Automotive

| Curve | Standard | Use Case |
|-------|----------|----------|
| P-256 (secp256r1) | NIST / IEEE 1609.2 | V2X message signing, ISO 15118 |
| P-384 (secp384r1) | NIST | High-security certificates |
| brainpoolP256r1 | BSI / ISO 11770 | European automotive (some OEMs) |
| Ed25519 (EdDSA) | IETF RFC 8032 | Modern protocols, deterministic |

## Automotive Applications

### V2X (Vehicle-to-Everything)
- Every BSM (Basic Safety Message) is signed with ECDSA P-256
- Vehicles must verify 1000-2000 signatures/sec in dense traffic
- IEEE 1609.2 / ETSI TS 103 097 mandate specific curve and hash combinations
- Pseudonym certificates rotated for privacy

### Secure Boot
- Firmware images signed with ECDSA
- Smaller signatures = less flash/ROM storage overhead
- Faster verification than RSA on MCU-class hardware (ARM Cortex-M/R)

### ISO 15118 (Plug & Charge)
- Contract certificates use ECDSA for EV authentication
- TLS mutual authentication between EV and EVSE

## Run
```bash
pip install cryptography
python ecdsa_example.py
```

## Critical Security Notes

1. **Nonce (k) MUST be random and unique per signature**
   - Reusing k → private key recovery (Sony PS3 ECDSA fail)
   - Use RFC 6979 deterministic nonces or a CSPRNG
2. **Curve validation**: Always validate that received public keys are on the curve
3. **Hash truncation**: For P-256, use SHA-256. Hash output must match curve order size
4. **Side-channel attacks**: Power analysis can extract keys from unprotected hardware — use HSM
