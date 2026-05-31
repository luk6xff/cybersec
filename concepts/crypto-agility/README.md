# Crypto Agility

## Definition
**Crypto agility** is the ability to replace cryptographic algorithms, parameters, and protocols in a deployed system without requiring hardware changes or full system redesign.

## Why It Matters

| Driver | Impact |
|--------|--------|
| Post-quantum transition | Must swap RSA/ECC → PQC without hardware recall |
| Algorithm deprecation | SHA-1, 3DES, RSA-1024 all deprecated over time |
| Regulatory changes | New mandates (e.g., BSI, CNSA 2.0) |
| Vulnerability discovery | Algorithm broken → emergency rotation needed |
| Vehicle lifecycle | 15-25 years on road; crypto may become insecure |

## Architecture Principles

### 1. Algorithm Abstraction Layer
```
┌─────────────────────────────────────────┐
│         Application Logic                │
│  (SecOC, TLS, Secure Boot, V2X)         │
├─────────────────────────────────────────┤
│      Crypto Abstraction API              │
│  sign(key_id, data) → signature          │
│  verify(key_id, data, sig) → bool        │
│  encrypt(key_id, data) → ciphertext      │
│  kdf(key_id, context) → derived_key      │
├─────────────────────────────────────────┤
│         Algorithm Registry               │
│  ┌─────────┬──────────┬───────────┐     │
│  │ AES-128 │ AES-256  │ ChaCha20  │     │
│  │ SHA-256 │ SHA-384  │ SHA3-256  │     │
│  │ ECDSA   │ Ed25519  │ ML-DSA    │     │
│  │ ECDH    │ X25519   │ ML-KEM    │     │
│  └─────────┴──────────┴───────────┘     │
├─────────────────────────────────────────┤
│      Hardware / Software Backend         │
│  ┌─────────────┐  ┌──────────────┐      │
│  │  HSM/HPSE   │  │  SW Crypto   │      │
│  │  (HW accel) │  │  (fallback)  │      │
│  └─────────────┘  └──────────────┘      │
└─────────────────────────────────────────┘
```

### 2. Algorithm Negotiation Protocol
- Never hardcode a single algorithm in protocol messages
- Include algorithm identifier in headers (like TLS cipher suites)
- Allow server/peer to select from supported set

### 3. Key-Algorithm Binding
- Keys stored with metadata: algorithm, allowed operations, expiry
- Key rotation can change algorithm simultaneously
- Old keys remain for verification of existing signatures

### 4. OTA-Updatable Crypto Libraries
- Crypto library as separate updatable partition
- Version-pinned by application (no silent downgrade)
- Rollback protection on crypto library version

## AUTOSAR Implementation

### Crypto Service Manager (CSM) — Already Agile by Design
```xml
<!-- AUTOSAR CSM Configuration Example -->
<CryptoServiceJob>
  <AlgorithmFamily>AES</AlgorithmFamily>
  <AlgorithmMode>GCM</AlgorithmMode>
  <KeyLength>256</KeyLength>
  <CryptoDriverReference>/Crypto_30_HSM</CryptoDriverReference>
</CryptoServiceJob>
```

The AUTOSAR crypto stack supports agility:
- **CSM** abstracts algorithm selection via job configuration
- **CryIf** routes to appropriate crypto driver
- **Crypto drivers** can be swapped (HSM ↔ software)
- Algorithm changes require only configuration update (if HW supports it)

## Migration Checklist

- [ ] Inventory all cryptographic algorithms in use
- [ ] Identify hardcoded algorithm references in code
- [ ] Ensure key storage supports multiple algorithm families
- [ ] Verify OTA mechanism can update crypto libraries
- [ ] Test hybrid (classical + PQC) operation
- [ ] Plan flash/RAM budget for larger PQC keys
- [ ] Establish algorithm deprecation policy
- [ ] Document minimum supported algorithm versions

## Real-World Examples of Crypto Deprecation

| Year | Event | Impact |
|------|-------|--------|
| 2005 | SHA-1 theoretical collision | Migration to SHA-256 |
| 2017 | SHA-1 practical collision (SHAttered) | Emergency deprecation |
| 2015 | NIST deprecates RSA-1024 | Minimum RSA-2048 enforced |
| 2020 | NIST deprecates 3DES | AES mandatory |
| 2024 | NIST finalizes PQC standards | Transition planning begins |
| 2030 | Quantum computers expected | Classical asymmetric broken |
