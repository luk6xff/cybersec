# Post-Quantum Cryptography (PQC)

## Why PQC Matters for Automotive

Vehicles have a **15-25 year lifecycle**. A car designed today will still be on the road in 2045+. Quantum computers capable of breaking RSA/ECC (via Shor's algorithm) are expected by 2030-2035.

**"Harvest Now, Decrypt Later"**: Adversaries can record encrypted OTA traffic today and decrypt it when quantum computers are available. This makes PQC migration urgent for:
- Long-lived vehicle certificates
- OTA firmware update channels
- V2X communication
- Connected vehicle telemetry

## NIST PQC Standards (Finalized 2024)

| Algorithm | Type | Standard | Based On | Use Case |
|-----------|------|----------|----------|----------|
| **ML-KEM** (Kyber) | Key Encapsulation | FIPS 203 | Lattice (M-LWE) | Key exchange, encryption |
| **ML-DSA** (Dilithium) | Digital Signature | FIPS 204 | Lattice (M-LWE/SIS) | Code signing, certificates |
| **SLH-DSA** (SPHINCS+) | Digital Signature | FIPS 205 | Hash-based | Stateless backup signature |

### Parameter Sets

#### ML-KEM (Key Encapsulation)
| Parameter Set | Security Level | Public Key | Ciphertext | Shared Secret |
|--------------|---------------|------------|------------|---------------|
| ML-KEM-512 | NIST Level 1 (AES-128) | 800 B | 768 B | 32 B |
| ML-KEM-768 | NIST Level 3 (AES-192) | 1184 B | 1088 B | 32 B |
| ML-KEM-1024 | NIST Level 5 (AES-256) | 1568 B | 1568 B | 32 B |

#### ML-DSA (Digital Signatures)
| Parameter Set | Security Level | Public Key | Signature |
|--------------|---------------|------------|-----------|
| ML-DSA-44 | NIST Level 2 | 1312 B | 2420 B |
| ML-DSA-65 | NIST Level 3 | 1952 B | 3293 B |
| ML-DSA-87 | NIST Level 5 | 2592 B | 4595 B |

#### SLH-DSA (Hash-based Signatures)
| Parameter Set | Security Level | Public Key | Signature |
|--------------|---------------|------------|-----------|
| SLH-DSA-128s | Level 1 | 32 B | 7856 B |
| SLH-DSA-192f | Level 3 | 48 B | 35664 B |
| SLH-DSA-256s | Level 5 | 64 B | 29792 B |

## Size Comparison with Classical Crypto

```
                  Public Key    Signature/Ciphertext
ECDSA P-256:      64 B          64 B
RSA-2048:         256 B         256 B
ML-DSA-65:        1952 B        3293 B     ← 30x larger than ECDSA!
ML-KEM-768:       1184 B        1088 B     ← 4x larger than RSA
SLH-DSA-128s:     32 B          7856 B     ← Huge signatures
```

**Automotive impact**: CAN/CAN-FD cannot carry PQC signatures. Ethernet-based architectures are required for PQC.

## Hybrid Approach (Recommended for Transition)

Combine classical + PQC to maintain security even if one scheme is broken:

```
Hybrid Key Exchange:  X25519 + ML-KEM-768
Hybrid Signature:     ECDSA P-256 + ML-DSA-65
```

This is mandated by:
- **BSI (German Federal Office)**: Recommends hybrid for critical infrastructure
- **ANSSI (France)**: Requires hybrid during transition period
- **CNSA 2.0 (NSA)**: Timeline for PQC migration in national security systems

## Examples

- [ML-KEM (Kyber) Key Encapsulation](ml-kem/)
- [ML-DSA (Dilithium) Digital Signatures](ml-dsa/)
- [SLH-DSA (SPHINCS+) Hash-based Signatures](slh-dsa/)
- [Hybrid Key Exchange (X25519 + ML-KEM)](hybrid/)

## Migration Timeline for Automotive

| Timeframe | Action |
|-----------|--------|
| 2024-2025 | Inventory all cryptographic assets; assess PQC readiness |
| 2025-2026 | Implement crypto-agility in ECU software architecture |
| 2026-2028 | Deploy hybrid schemes for backend/OTA; begin V2X PQC trials |
| 2028-2030 | Full PQC for new vehicle platforms; update PKI |
| 2030+ | Deprecate classical-only; quantum-safe mandatory |

## Crypto-Agility

**Crypto-agility** = the ability to swap cryptographic algorithms without redesigning the system.

Requirements for automotive ECUs:
1. Algorithm negotiation protocol (not hardcoded cipher suites)
2. Sufficient flash/RAM for larger PQC keys and signatures
3. Hardware accelerator abstraction layer
4. OTA-updatable crypto libraries
5. Certificate format supporting multiple signature algorithms (X.509 hybrid)
