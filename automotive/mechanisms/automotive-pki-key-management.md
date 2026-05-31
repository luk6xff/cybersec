# Automotive Key Management & PKI

## Vehicle PKI Architecture

### Certificate Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                        OEM Root CA                                │
│        (Offline, HSM-protected, 20+ year validity)              │
└──────────────┬──────────────────────┬───────────────────────────┘
               │                      │
    ┌──────────▼──────────┐  ┌───────▼────────────────┐
    │   Backend Sub-CA    │  │   Vehicle Sub-CA        │
    │  (OTA, Telemetry)   │  │  (ECU Identity)         │
    └──────────┬──────────┘  └───────┬────────────────┘
               │                      │
    ┌──────────▼──────────┐  ┌───────▼────────────────┐
    │   Server Certs      │  │   ECU Identity Certs   │
    │  (TLS, signing)     │  │  (mTLS, diagnostics)   │
    └─────────────────────┘  └────────────────────────┘
```

### Certificate Types in Automotive

| Certificate | Purpose | Validity | Key Algorithm |
|-------------|---------|----------|---------------|
| OEM Root CA | Trust anchor | 20-30 years | RSA-4096 / ECDSA P-384 |
| Backend Sub-CA | Server authentication | 5-10 years | ECDSA P-256 |
| ECU Identity | Device authentication | Vehicle lifetime | ECDSA P-256 |
| V2X Enrollment | V2X identity | 5 years | ECDSA P-256 |
| V2X Pseudonym | Privacy-preserving V2X | 1 week | ECDSA P-256 |
| Diagnostic Auth | Workshop access | 1-24 hours | ECDSA P-256 |
| OTA Signing | Firmware authenticity | 2-5 years | ECDSA P-256 / RSA-3072 |

## Key Provisioning in Manufacturing

### Secure Manufacturing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Secure Manufacturing Facility                  │
│                    (ISO 27001, physical security)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐     ┌──────────────┐     ┌───────────────────┐   │
│  │   KMS    │────→│  Programming │────→│    ECU under       │   │
│  │ (Backend)│     │   Station    │     │    provisioning    │   │
│  │          │     │              │     │                    │   │
│  │Generate  │     │Inject keys   │     │Store in HSM/OTP   │   │
│  │keys per  │     │via secure    │     │Burn fuses         │   │
│  │ECU (UID) │     │debug channel │     │Lock debug port    │   │
│  └──────────┘     └──────────────┘     └───────────────────┘   │
│                                                                  │
│  Security controls:                                              │
│  • Air-gapped KMS / HSM cluster                                  │
│  • 4-eyes principle for key operations                           │
│  • Audit logging of all provisioning                             │
│  • Physical access control (badge + biometric)                   │
│  • Encrypted key transport (key wrapping)                        │
│  • Unique key per ECU (never duplicate)                          │
└─────────────────────────────────────────────────────────────────┘
```

### Key Injection Methods

| Method | Security | Complexity | Use Case |
|--------|----------|-----------|----------|
| Direct injection (cleartext) | Low | Low | Development only |
| Key wrapping (AES-KW) | High | Medium | Production symmetric keys |
| Certificate enrollment (EST/CMP) | High | High | Production PKI |
| Derived keys (KDF from master) | Medium | Low | Fleet diversification |
| On-device generation + CSR | Highest | High | Private key never leaves HSM |

### Preferred: On-Device Key Generation
```
1. ECU generates key pair internally in HSM
   → Private key NEVER leaves the HSM
2. ECU creates Certificate Signing Request (CSR)
3. CSR sent to CA via secure manufacturing channel
4. CA issues certificate
5. Certificate stored in ECU NVM
6. Root CA cert provisioned separately (can be OTP)
```

## Fleet Key Diversification

**Problem**: If all vehicles share the same key, one compromised vehicle = entire fleet compromised.

**Solution**: Unique keys per ECU, derived from master + unique identifier.

```
Master_Key (in KMS, HSM-protected)
     │
     ├── KDF(Master, VIN_1 || ECU_ID_A) → Key_Vehicle1_ECU_A
     ├── KDF(Master, VIN_1 || ECU_ID_B) → Key_Vehicle1_ECU_B
     ├── KDF(Master, VIN_2 || ECU_ID_A) → Key_Vehicle2_ECU_A
     └── ...

Where KDF = HKDF-SHA256 or NIST SP 800-108 (Counter Mode)
```

## Certificate Lifecycle Management

```
┌────────────┐     ┌────────────┐     ┌────────────┐
│  Request   │────→│   Issue    │────→│   Active   │
│  (CSR)     │     │  (CA sign) │     │  (In use)  │
└────────────┘     └────────────┘     └─────┬──────┘
                                            │
                              ┌──────────────┼──────────────┐
                              │              │              │
                       ┌──────▼──┐    ┌──────▼──┐    ┌─────▼────┐
                       │  Renew  │    │  Revoke │    │  Expire  │
                       │(new cert)│    │  (CRL)  │    │(time out)│
                       └─────────┘    └─────────┘    └──────────┘
```

### Revocation Challenges in Automotive
- Vehicles may be offline for weeks/months
- CRL distribution requires connectivity
- OCSP requires real-time backend connection
- **Solution**: Short-lived certificates (auto-expire) + periodic renewal when online

## OTA Key Update Protocol

### Symmetric Key Update (SHE-based)
```
Backend KMS computes:
  M1 = UID || AuthKeyID || TargetKeyID || 0...0
  M2 = ENC(KEK, Counter || KeyFlags || NewKey)
  M3 = CMAC(AuthKey, M1 || M2)

ECU receives (M1, M2, M3):
  1. Verify M3 using AuthKey
  2. Decrypt M2 using KEK to get NewKey
  3. Verify Counter > stored counter (anti-replay)
  4. Store NewKey in target slot
  5. Compute M4, M5 as proof of successful update
  6. Send (M4, M5) back to backend for confirmation
```

### Asymmetric Key/Certificate Update
```
1. Backend signs new certificate using Sub-CA key
2. ECU verifies Sub-CA signature against stored Root CA
3. If valid: store new certificate, keep old as backup
4. Confirm update to backend
5. Backend marks old certificate for revocation
```

## Practical Considerations

### Key Storage Budget (per ECU)
| Item | Count | Size | Total |
|------|-------|------|-------|
| Root CA cert | 1 | ~300B | 300B |
| Own identity cert | 1 | ~500B | 500B |
| SecOC keys (AES-128) | 10-50 | 16B | 160-800B |
| Secure boot key (ECDSA pub) | 1 | 64B | 64B |
| TLS private key (P-256) | 1 | 32B | 32B |
| **Total** | | | **~2KB typical** |

### Failure Modes
| Failure | Impact | Recovery |
|---------|--------|----------|
| Key corruption (bit flip) | Auth failure, no start | Backup key slot, OTA re-provision |
| Counter desync (SecOC FV) | All messages rejected | Sync protocol, service reset |
| Certificate expired | TLS failure, no backend | Grace period, emergency cert |
| HSM lockout (wrong PIN) | ECU bricked | Manufacturing recovery mode |

## Standards & References
- ISO 11770 (Key Management Techniques)
- SAE J3101 (Hardware Protected Security for Ground Vehicles)
- AUTOSAR KeyM SWS
- NIST SP 800-57 (Key Management Recommendations)
- RFC 7030 (EST — Enrollment over Secure Transport)
- RFC 4210 (CMP — Certificate Management Protocol)
