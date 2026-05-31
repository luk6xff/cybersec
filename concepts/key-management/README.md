# Key Management in Automotive

## Overview
Key management is arguably the most critical aspect of automotive cybersecurity. A compromised key hierarchy can undermine all other security controls.

## Key Lifecycle

```
┌──────────┐    ┌───────────┐    ┌────────────┐    ┌──────────┐    ┌────────────┐
│ Generate  │───→│ Provision │───→│   Use      │───→│  Rotate  │───→│  Destroy   │
│           │    │ /Install  │    │            │    │ /Renew   │    │ /Revoke    │
└──────────┘    └───────────┘    └────────────┘    └──────────┘    └────────────┘
     │                │                │                │                │
   TRNG/HSM      Secure Mfg       Runtime          OTA/Service       Zeroize
   Key Derivation  Key Injection    Crypto Ops      New Key Material   End of Life
```

## Key Hierarchy (Typical Automotive)

```
                    ┌─────────────────────┐
                    │  Root Key (OTP/Fuse) │  ← Never leaves HSM, burned at manufacturing
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
    ┌─────────▼──────┐ ┌──────▼───────┐ ┌─────▼─────────┐
    │ Secure Boot Key │ │  SecOC Keys  │ │  TLS Identity │
    │ (Signature      │ │  (Symmetric) │ │  (ECC Key Pair)│
    │  Verification)  │ │              │ │               │
    └────────────────┘ └──────┬───────┘ └───────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
              ┌─────▼──┐ ┌───▼───┐ ┌───▼───┐
              │ Key_CAN1│ │Key_CAN2│ │Key_ETH│
              │ (Domain │ │(Domain │ │(Domain│
              │  ctrl)  │ │ ADAS)  │ │ info) │
              └────────┘ └───────┘ └───────┘
```

## Key Types in Automotive

| Key Type | Algorithm | Purpose | Storage |
|----------|-----------|---------|---------|
| Secure Boot Root | RSA-2048/ECDSA P-256 | Firmware authentication | OTP/eFuse |
| SecOC MAC Key | AES-128-CMAC | CAN message auth | HSM NVM |
| MACsec Key | AES-128/256-GCM | Ethernet frame encryption | HSM NVM |
| TLS Private Key | ECDSA P-256 | Backend authentication | HSM NVM |
| OTA Encryption Key | AES-256-GCM | Firmware confidentiality | Derived per session |
| V2X Signing Key | ECDSA P-256 | BSM signing | V2X HSM |
| Diagnostic Auth Key | AES-128/ECC | UDS 0x27/0x29 access | HSM NVM |

## Key Provisioning Approaches

### 1. Manufacturing Injection
- Keys injected during ECU production in secure facility
- Root keys burned into OTP/eFuse (one-time programmable)
- Requires secure manufacturing environment (ISO 27001 compliant)

### 2. Key Derivation (KDF)
- Derive child keys from root using KDF (HKDF, NIST SP 800-108)
- Only root key needs secure injection
- Child keys can be regenerated if corrupted

### 3. Key Agreement (ECDH)
- Establish shared secrets without pre-shared keys
- Used for TLS session keys and V2X peer communication
- Requires authenticated public key exchange (certificates)

### 4. Key Wrapping
- Transport keys encrypted under a Key Encryption Key (KEK)
- KEK pre-installed in HSM
- Allows secure OTA key updates

## Key Rotation Strategies

| Strategy | When | How |
|----------|------|-----|
| Time-based | Every N days/months | OTA key update, certificate renewal |
| Event-based | After compromise/recall | Emergency key revocation + re-provisioning |
| Usage-based | After N operations | ECDSA keys rotated per privacy (V2X pseudonyms) |
| Version-based | Each firmware update | Derive new keys from updated master + version |

## SecOC Key Distribution

### Challenge: Symmetric Keys Across Multiple ECUs
SecOC uses shared symmetric keys — every ECU pair sharing a CAN message needs the same key.

### Solutions:
1. **Per-link unique keys**: ECU-A ↔ ECU-B has unique key (best security, high complexity)
2. **Group keys**: All ECUs on a bus share one key (simpler, weaker isolation)
3. **Key server ECU**: Central ECU distributes session keys (more complex, single point of failure)

### Key Update Protocol (SHE-based):
```
M1 = UID || Key_Slot_ID || AuthID
M2 = AES-CBC(KEK, Counter || Flags || New_Key)
M3 = CMAC(Key_AuthID, M1 || M2)
→ Verified by SHE before updating key slot
```

## Fleet-Wide Key Management System (KMS)

```
┌────────────────────────────────────────────────────────┐
│                   Backend KMS                           │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐   │
│  │ Key Gen  │  │ Key Store│  │ Policy Engine      │   │
│  │ (HSM     │  │ (Vault/  │  │ (Who gets what key)│   │
│  │  cluster)│  │  CloudHSM│  │                    │   │
│  └──────────┘  └──────────┘  └───────────────────┘   │
└─────────────────────────┬──────────────────────────────┘
                          │ Secure Channel (mTLS)
              ┌───────────┼───────────┐
              │           │           │
        ┌─────▼──┐  ┌────▼───┐  ┌───▼────┐
        │Vehicle 1│  │Vehicle 2│  │Vehicle N│
        │   ECU   │  │   ECU   │  │   ECU   │
        └────────┘  └────────┘  └────────┘
```

## Common Pitfalls

1. **Hardcoded keys in firmware** — Extractable via reverse engineering
2. **Same key across entire fleet** — One compromise = all vehicles compromised
3. **No key rotation mechanism** — Keys valid forever
4. **Key stored in plaintext NVM** — Readable via debug/glitch attacks
5. **Weak key derivation** — Using predictable inputs (VIN alone)
6. **No key revocation** — Cannot invalidate compromised certificates

## Standards & References
- NIST SP 800-57 (Key Management)
- AUTOSAR SecOC Key Management
- ISO 11770 (Key Management Techniques)
- SAE J3101 (Hardware Protected Security for Ground Vehicles)
