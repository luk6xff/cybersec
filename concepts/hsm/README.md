# Hardware Security Modules (HSM) in Automotive

## Overview
An HSM is a dedicated hardware component that provides secure key storage, cryptographic acceleration, and tamper resistance. In automotive, HSMs are integrated into ECUs to protect secrets and enforce security policies.

## Automotive HSM Types

### Embedded HSM (SHE / EVITA)
| Standard | Security Level | Features |
|----------|---------------|----------|
| **SHE** (Secure Hardware Extension) | Basic | 128-bit AES keys, CMAC, limited key slots |
| **EVITA Light** | Medium | SHE + random number generation |
| **EVITA Medium** | Medium-High | + Asymmetric crypto (ECC), secure boot |
| **EVITA Full** | High | + Isolated execution, full PKI support |

### Common Automotive HSM Implementations
- **Infineon AURIX TC3xx HPSE** — Hardware Platform Security Extension
- **NXP S32G HSE** — Hardware Security Engine
- **Renesas RH850/P1x-C ICU-M** — Intelligent Cryptographic Unit
- **ST SPC58** — HSM-equipped Power Architecture MCU

## HSM Architecture

```
┌─────────────────────────────────────────────┐
│              ECU Application                  │
├─────────────────────────────────────────────┤
│         AUTOSAR Crypto Stack                 │
│   CryIf → Crypto Driver → HSM Driver        │
├─────────────────────────────────────────────┤
│          HSM Hardware Boundary               │
│  ┌─────────────────────────────────────┐    │
│  │  Secure Key Storage (OTP/NVM)       │    │
│  │  Crypto Accelerators (AES/ECC/SHA)  │    │
│  │  True Random Number Generator       │    │
│  │  Secure Boot ROM                    │    │
│  │  Monotonic Counter                  │    │
│  │  Tamper Detection                   │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

## Key Management Operations

| Operation | Description | HSM Role |
|-----------|-------------|----------|
| Key Generation | Create new keys | TRNG + secure storage |
| Key Import | Provision keys from KMS | Decrypt wrapped key, store internally |
| Key Export | Share public keys | Export only public part |
| Key Derivation | Derive session keys | KDF within secure boundary |
| Key Destruction | Zeroize keys | Secure erase of NVM slots |

## SHE Key Slots

The SHE (Secure Hardware Extension) specification defines a fixed key slot layout:

| Slot | Name | Purpose |
|------|------|---------|
| 0 | SECRET_KEY | For key update protocol |
| 1 | MASTER_ECU_KEY | ECU identity, key hierarchy root |
| 2 | BOOT_MAC_KEY | Secure boot MAC verification |
| 3 | BOOT_MAC | Stored boot MAC value |
| 4-13 | KEY_1 to KEY_10 | General-purpose symmetric keys |
| 14 | RAM_KEY | Volatile session key |

## AUTOSAR Crypto Stack Integration

```
┌─────────────────────────────────────────────────────┐
│  Application (SecOC, TLS, SecureBoot)                │
├─────────────────────────────────────────────────────┤
│  CSM (Crypto Service Manager)                        │
│  - Job queue management                              │
│  - Asynchronous/synchronous processing               │
├─────────────────────────────────────────────────────┤
│  CryIf (Crypto Interface)                            │
│  - Routes crypto jobs to appropriate driver           │
├──────────────────────┬──────────────────────────────┤
│  Crypto_30_HSM       │  Crypto_30_LibCrypto          │
│  (Hardware driver)   │  (Software fallback)          │
├──────────────────────┴──────────────────────────────┤
│  Hardware: HPSE / HSE / ICU                          │
└─────────────────────────────────────────────────────┘
```

## Security Best Practices

1. **Key hierarchy**: Root key in OTP → derive all other keys
2. **Least privilege**: Each application gets access only to its key slots
3. **Secure boot chain**: HSM verifies bootloader before releasing app cores
4. **Debug lock**: Disable JTAG/SWD in production via HSM-controlled fuses
5. **Rollback protection**: Use monotonic counters to prevent firmware downgrade
6. **Key diversification**: Unique keys per ECU (never share symmetric keys across fleet)

## Attack Surfaces

| Attack | Target | Mitigation |
|--------|--------|------------|
| Side-channel (DPA/SPA) | Key extraction via power analysis | Hardware countermeasures, masking |
| Fault injection (glitching) | Skip security checks | Voltage/clock monitors, redundancy |
| Cold boot | RAM key extraction | Volatile key zeroization on tamper |
| Debug interface | Direct memory access | Fuse-based permanent debug disable |
| Key provisioning MITM | Intercept during manufacturing | Authenticated key wrapping, secure facility |

## References
- AUTOSAR SWS Crypto Stack Architecture
- Infineon AURIX HPSE User Manual
- NXP HSE Firmware Reference Manual
- ISO/SAE 21434 (Cybersecurity Engineering)
