# AUTOSAR Cybersecurity Architecture

## Overview
AUTOSAR (AUTomotive Open System ARchitecture) provides standardized software architecture for automotive ECUs. Cybersecurity is integrated through dedicated modules in both Classic Platform (CP) and Adaptive Platform (AP).

## AUTOSAR Classic Platform (CP) — Security Modules

### Architecture Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                     Application Layer                             │
│  ┌──────────┐  ┌─────────┐  ┌──────────┐  ┌─────────────────┐  │
│  │  SecOC   │  │ KeyM    │  │  IdsM    │  │  Application SW │  │
│  │  Client  │  │ Client  │  │ Reporter │  │                 │  │
│  └────┬─────┘  └────┬────┘  └────┬─────┘  └────────────────┘  │
├───────┼──────────────┼───────────┼──────────────────────────────┤
│       │    RTE (Runtime Environment)    │                        │
├───────┼──────────────┼───────────┼──────────────────────────────┤
│       ▼              ▼           ▼                               │
│  ┌──────────┐  ┌─────────┐  ┌──────────┐                       │
│  │  SecOC   │  │  KeyM   │  │  IdsM    │   BSW (Basic SW)      │
│  └────┬─────┘  └────┬────┘  └────┬─────┘                       │
│       │              │           │                               │
│  ┌────▼──────────────▼───────────▼──────────────────────────┐   │
│  │              CSM (Crypto Service Manager)                  │   │
│  └────────────────────────┬──────────────────────────────────┘   │
│                           │                                       │
│  ┌────────────────────────▼──────────────────────────────────┐   │
│  │              CryIf (Crypto Interface)                      │   │
│  └───────────┬──────────────────────────┬────────────────────┘   │
│              │                          │                         │
│  ┌───────────▼──────────┐  ┌───────────▼──────────────────┐     │
│  │  Crypto_30_HSM       │  │  Crypto_30_LibCrypto         │     │
│  │  (Hardware driver)   │  │  (Software implementation)   │     │
│  └───────────┬──────────┘  └──────────────────────────────┘     │
├──────────────┼───────────────────────────────────────────────────┤
│              ▼                                                    │
│       HSM Hardware (HPSE/HSE)                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Key Security Modules

### SecOC (Secure Onboard Communication)
**Purpose**: Authenticate PDUs (Protocol Data Units) on CAN/Ethernet.

```
┌──────────────────────────────────────────────────────┐
│              SecOC Secured I-PDU Format               │
├────────────────────┬───────────────┬─────────────────┤
│  Authentic I-PDU   │  Freshness    │  Truncated MAC  │
│  (Original data)   │  Value (FV)   │  (Authenticator)│
│                    │  (partial)    │                 │
│    n bytes         │  0-m bits     │   t bits        │
└────────────────────┴───────────────┴─────────────────┘

Authentication Generation:
  Full_Auth = CMAC(Key, Authentic_IPDU || Full_Freshness_Value || DataID)
  Truncated_MAC = Full_Auth[0:t]  (typically 24-64 bits)
  Secured_IPDU = Authentic_IPDU || Partial_FV || Truncated_MAC
```

**Key parameters**:
| Parameter | Typical CAN 2.0 | CAN FD | Ethernet |
|-----------|-----------------|--------|----------|
| MAC truncation | 24 bits | 48-64 bits | 128 bits |
| Freshness bits in PDU | 4 bits | 8-16 bits | 32+ bits |
| Algorithm | AES-128-CMAC | AES-128-CMAC | AES-128-GCM |

### KeyM (Key Manager)
**Purpose**: Manage cryptographic key lifecycle within an ECU.

Operations:
- Certificate storage and parsing (X.509, CVC)
- Key installation and update
- Certificate verification (chain validation)
- Interface to CSM for crypto operations

### IdsM (Intrusion Detection System Manager)
**Purpose**: Collect and manage security events from qualified security sensors.

```
Security Event Flow:
  Sensor (SecOC/FW/App) → IdsM → Security Event Memory
                                       │
                                       ▼
                              Reporting to Backend
                              (via Diagnostic/DoIP)
```

### CSM (Crypto Service Manager)
**Purpose**: Unified interface for all cryptographic services.

Supported operations:
- Hash (SHA-256, SHA-384)
- MAC (CMAC, HMAC)
- Symmetric encryption (AES-CBC, AES-GCM, AES-CTR)
- Asymmetric operations (ECDSA sign/verify, ECDH)
- Key derivation, key exchange
- Random number generation

## AUTOSAR Adaptive Platform (AP) — Security

The Adaptive Platform targets high-performance ECUs (Linux-based):

### Key Differences from Classic
| Aspect | Classic Platform | Adaptive Platform |
|--------|-----------------|-------------------|
| OS | AUTOSAR OS (static) | POSIX (Linux/QNX) |
| Communication | Signal-based (CAN) | Service-oriented (SOME/IP, DDS) |
| Crypto | CSM + CryIf | Crypto API (ara::crypto) |
| Update | Full reflash | Container/package updates |
| Identity | Static ECU config | PKI + identity management |

### ara::crypto (Adaptive Crypto API)
```cpp
// Example: ECDSA signature verification (ara::crypto)
#include <ara/crypto/cryp/verifier_public_ctx.h>

auto verifier = cryptoProvider->CreateVerifierPublicCtx(algId::kECDSA_SHA256);
verifier->SetKey(publicKey);
verifier->Update(messageData);
auto result = verifier->Finish(signature);
// result.Value() == true if signature valid
```

### IAM (Identity and Access Management)
- Process-level access control
- Manifest-declared capabilities
- Service authentication via TLS/DTLS
- Role-based access to adaptive services

## SecOC Freshness Management

### Challenge
CAN has limited bandwidth → cannot send full freshness counter in every frame.

### Freshness Value Manager (FVM) Strategies:

#### 1. Trip Counter + Message Counter + Reset Counter
```
Full_FV = Trip_Counter (16 bit) || Reset_Counter (8 bit) || Msg_Counter (8 bit)
Sent in PDU: only lower bits of Msg_Counter (4 bits)
Receiver reconstructs full FV from synchronized counters
```

#### 2. Timestamp-based
```
Full_FV = Synchronized_Timestamp (from StbM)
Acceptable window: ±tolerance
```

#### 3. Challenge-Response (for low-frequency messages)
```
Verifier sends random challenge → Prover includes challenge in MAC
```

### Synchronization Problem
```
Sender increments counter:  FV = 100, 101, 102, ...
Receiver expects:           FV ≥ last_verified_FV

If receiver misses messages (bus-off, reset):
  → Receiver's FV < Sender's FV
  → All messages rejected until sync!

Solution: Freshness Value sync protocol (OEM-specific)
```

## Configuration Example (SecOC)

```xml
<!-- SecOC Configuration (simplified) -->
<SecOCTxPduProcessing>
  <SecOCTxAuthenticPduId>CAN_Msg_BrakeCmd</SecOCTxAuthenticPduId>
  <SecOCAuthAlgorithm>CMAC_AES128</SecOCAuthAlgorithm>
  <SecOCFreshnessValueLength>32</SecOCFreshnessValueLength>
  <SecOCFreshnessValueTxLength>4</SecOCFreshnessValueTxLength>
  <SecOCAuthInfoTruncLength>24</SecOCAuthInfoTruncLength>
  <SecOCDataId>0x0042</SecOCDataId>
  <SecOCKeyRef>/CsmKeys/SecOC_BrakeCmd_Key</SecOCKeyRef>
</SecOCTxPduProcessing>
```

## Security Best Practices for AUTOSAR

1. **Use HSM for all key operations** — never store keys in application flash
2. **Enable SecOC on all safety-critical CAN messages** (brake, steering, throttle)
3. **Implement IdsM** with backend reporting for fleet-wide visibility
4. **Separate crypto keys by purpose** — boot key ≠ SecOC key ≠ TLS key
5. **MAC truncation trade-off**: shorter MAC = less bandwidth but lower forgery resistance
6. **Freshness sync must survive ECU reset** — persist counters in NVM
7. **Test SecOC under bus-off conditions** — verify recovery mechanism

## References
- AUTOSAR CP SWS SecOC (R22-11)
- AUTOSAR CP SWS CSM
- AUTOSAR CP SWS KeyM
- AUTOSAR CP SWS IdsM
- AUTOSAR AP SWS Cryptography
- AUTOSAR AP SWS Identity and Access Management
