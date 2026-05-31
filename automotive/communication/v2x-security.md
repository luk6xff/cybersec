# V2X (Vehicle-to-Everything) Security

## Overview
V2X enables vehicles to communicate with other vehicles (V2V), infrastructure (V2I), pedestrians (V2P), and networks (V2N). Security is critical because:
- Messages directly influence driving decisions (collision avoidance)
- Broadcast nature enables eavesdropping and injection
- Privacy concerns (tracking vehicles by signatures)

## Communication Technologies

| Technology | Standard | Range | Latency | Status |
|-----------|----------|-------|---------|--------|
| DSRC/ITS-G5 | IEEE 802.11p | ~300m | <10ms | Deployed (EU/Japan) |
| C-V2X (PC5) | 3GPP Rel-14+ | ~450m | <10ms | Growing (US/China) |
| C-V2X (Uu) | 3GPP Rel-16+ (5G) | Cellular | 20-100ms | Network-based |

## Security Architecture (IEEE 1609.2 / ETSI TS 103 097)

### PKI Structure (SCMS — Security Credential Management System)

```
┌─────────────────────────────────────────────────────────────┐
│                    Root CA                                    │
│         (Offline, air-gapped, highest trust)                │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────────┐
        │            │                │
┌───────▼──────┐ ┌──▼───────────┐ ┌──▼──────────────┐
│ Enrollment CA │ │Pseudonym CA  │ │ Linkage Auth 1+2│
│(Long-term ID) │ │(Short-lived  │ │(Privacy, can    │
│               │ │ certificates)│ │ link if needed) │
└───────┬──────┘ └──────┬───────┘ └─────────────────┘
        │                │
        ▼                ▼
┌──────────────┐ ┌──────────────────┐
│ Enrollment   │ │ Pseudonym Certs  │
│ Certificate  │ │ (20 per week,    │
│ (per vehicle)│ │  rotated for     │
│              │ │  privacy)        │
└──────────────┘ └──────────────────┘
```

### Message Signing Flow

```
Sender (Vehicle A):                    Receiver (Vehicle B):
┌────────────────────────┐            ┌─────────────────────────┐
│ 1. Compose BSM         │            │ 1. Receive signed BSM   │
│    (position, speed,   │            │ 2. Verify cert chain    │
│     heading, brake)    │            │ 3. Check cert validity  │
│ 2. Select pseudonym    │            │ 4. Verify ECDSA sig     │
│    certificate         │            │ 5. Check plausibility   │
│ 3. Sign with ECDSA     │───────────→│ 6. Use data for safety  │
│    P-256               │  Broadcast │    decision              │
│ 4. Attach certificate  │            │                         │
│ 5. Broadcast           │            │ If invalid → discard    │
└────────────────────────┘            │ If misbehaving → report │
                                      └─────────────────────────┘
```

## Cryptographic Requirements

| Function | Algorithm | Standard |
|----------|-----------|----------|
| Message signing | ECDSA P-256 (SHA-256) | IEEE 1609.2, ETSI |
| Message encryption | ECIES (AES-128-CCM) | IEEE 1609.2 |
| Certificate format | Compact (not X.509!) | IEEE 1609.2 |
| Key agreement | ECDH P-256 | For encrypted V2X |
| Hash | SHA-256 | All operations |

### Performance Requirements
- **Signing**: ~1-10ms per BSM (10 Hz broadcast rate)
- **Verification**: Must verify 1000-2000+ incoming messages/sec
- **Certificate validation**: Must handle thousands of unique pseudonym certs
- **Latency budget**: Total crypto < 50ms for safety applications

## Privacy Mechanisms

### Pseudonym Certificates
- Vehicle has pool of ~20 short-lived certificates per week
- Certificates rotated every 5 minutes (geographic/temporal unlinkability)
- No personally identifiable information in certificates
- **Linkage Authority** can link certificates only with legal authorization

### Privacy Threats
| Threat | Attack | Mitigation |
|--------|--------|------------|
| Long-term tracking | Correlate same cert over time | Pseudonym rotation |
| Sybil attack | Create fake vehicles | Limited cert issuance, behavior analysis |
| Certificate fingerprinting | Unique cert patterns | Standardized format |
| Timing analysis | Link rotation patterns | Randomized rotation timing |

## Misbehavior Detection

Vehicles report potentially malicious/faulty V2X messages:

| Misbehavior Type | Detection | Response |
|-----------------|-----------|----------|
| Position spoofing | Inconsistent with physics/sensors | Report to MA |
| Ghost vehicles | No radar/lidar confirmation | Reduce trust score |
| Denial of service | Excessive message rate | Rate limiting |
| Invalid signatures | Cryptographic failure | Immediate discard |
| Expired certificates | Time check | Discard, log |
| Revoked certificates | CRL/OCSP check | Discard, report |

## V2X Hardware Security

```
┌──────────────────────────────────────┐
│         V2X On-Board Unit (OBU)       │
│  ┌──────────────┐  ┌──────────────┐  │
│  │  V2X Radio   │  │  Application │  │
│  │  (802.11p /  │  │  Processor   │  │
│  │   C-V2X)     │  │              │  │
│  └──────┬───────┘  └──────┬───────┘  │
│         │                  │          │
│  ┌──────┴──────────────────┴───────┐  │
│  │         V2X HSM                  │  │
│  │  • Pseudonym key storage         │  │
│  │  • ECDSA sign (hardware accel)   │  │
│  │  • Cert management               │  │
│  │  • Secure key injection           │  │
│  └──────────────────────────────────┘  │
└──────────────────────────────────────┘
```

## PQC Impact on V2X

**Challenge**: ML-DSA signatures (3.3KB) vs ECDSA (64B) = 50x larger
- At 2000 msgs/sec: 64KB/s (ECDSA) vs 6.4MB/s (ML-DSA) bandwidth
- Radio channel cannot support this today
- Research: signature aggregation, hash-based optimization

**Migration path**: Hybrid ECDSA + PQC with backward compatibility

## References
- IEEE 1609.2-2022 (V2X Security Services)
- ETSI TS 103 097 (EU V2X Security)
- SAE J2945/1 (BSM requirements)
- CAMP (Crash Avoidance Metrics Partnership) SCMS
- C2C-CC (Car-to-Car Communication Consortium)
