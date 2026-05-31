# OTA (Over-The-Air) Update Security

## OTA Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          OTA UPDATE SYSTEM                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐    TLS 1.3     ┌──────────────┐                      │
│  │  OTA Backend │ ←──────────── │  TCU / OTA   │                       │
│  │  (OEM Cloud) │ ──────────→  │  Client      │                       │
│  │              │   Signed pkg   │  (Vehicle)   │                       │
│  └──────┬───────┘                └──────┬───────┘                       │
│         │                               │                                │
│    ┌────┴────┐                    ┌─────┴──────┐                        │
│    │ Build   │                    │ OTA Master │                         │
│    │ Server  │                    │ (Gateway/  │                         │
│    │ (CI/CD) │                    │  HPC)      │                         │
│    └────┬────┘                    └─────┬──────┘                        │
│         │                               │ Internal (CAN/Ethernet)        │
│    ┌────┴────┐              ┌───────────┼──────────────┐                │
│    │ Signing │              │           │              │                 │
│    │ Server  │         ┌────┴───┐  ┌────┴───┐  ┌──────┴──┐             │
│    │ (HSM)   │         │ ECU A  │  │ ECU B  │  │ ECU C   │             │
│    └─────────┘         │(flash) │  │(flash) │  │(flash)  │             │
│                         └────────┘  └────────┘  └─────────┘             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Update Package Security

### Package Structure
```
┌──────────────────────────────────────────┐
│         OTA Update Package                │
├──────────────────────────────────────────┤
│ Manifest (signed)                         │
│   ├── Package version                    │
│   ├── Target ECU(s) + HW compatibility   │
│   ├── Minimum allowed rollback version   │
│   ├── Dependencies (required co-updates) │
│   ├── Installation instructions          │
│   ├── Hashes of all payload files        │
│   └── Digital signature (RSA/ECDSA)      │
├──────────────────────────────────────────┤
│ Payload (encrypted)                       │
│   ├── Firmware binary (full or delta)    │
│   ├── Calibration data                   │
│   └── Configuration files                │
├──────────────────────────────────────────┤
│ Metadata                                  │
│   ├── Release notes (human readable)     │
│   ├── Installation time estimate         │
│   └── Rollback strategy                  │
└──────────────────────────────────────────┘
```

### Signing & Verification
```
Build Pipeline (Secure Environment):
  1. Developer commits code → CI builds firmware binary
  2. Build server computes SHA-256 hash of binary
  3. Hash sent to Signing Server (HSM-backed, air-gapped)
  4. HSM signs hash with OEM private key (ECDSA P-256 or Ed25519)
  5. Signature + binary + manifest → OTA package
  6. Package encrypted with AES-256-GCM (key = per-vehicle or per-model)
  7. Package uploaded to CDN for distribution

Vehicle Verification:
  1. Download package (TLS 1.3 from CDN)
  2. Decrypt payload (using vehicle-specific key from HSM/SHE)
  3. Verify manifest signature (OEM public key in ECU secure storage)
  4. Check anti-rollback counter (new version > current version)
  5. Verify payload hash matches manifest hash
  6. Check HW compatibility (HW revision, variant)
  7. If ALL checks pass → proceed to installation
  8. If ANY check fails → abort, report error to backend
```

### Cryptographic Requirements

| Component | Algorithm | Key Size | Purpose |
|-----------|-----------|----------|---------|
| Package signing | ECDSA (P-256) or Ed25519 | 256-bit | Authenticity + integrity |
| Payload encryption | AES-256-GCM | 256-bit | Confidentiality (IP protection) |
| Hash verification | SHA-256 or SHA-384 | 256/384-bit | Integrity of individual files |
| Transport | TLS 1.3 | Session keys | Channel encryption |
| Key wrapping | AES-KW or RSA-OAEP | 256-bit / 2048-bit | Distribute payload decryption key |

## Anti-Rollback Protection

### Why Anti-Rollback?
```
Without anti-rollback:
  Attacker downloads old vulnerable firmware (v1.0) with known exploit
  → Installs v1.0 (which has valid OEM signature!)
  → Exploits known vulnerability in v1.0
  → Full ECU compromise

With anti-rollback:
  ECU stores monotonic counter: current_version = 5
  Old package has version = 3
  ECU rejects: version 3 < current 5 → INSTALL REFUSED
```

### Implementation Methods

| Method | Storage | Security | Notes |
|--------|---------|----------|-------|
| eFuse counter | OTP (one-time programmable) | Highest (hardware) | Limited increments (64-256 typical) |
| Secure NVM counter | HSM/SHE protected NVM | High | Unlimited increments, wear-leveled |
| Signed metadata | Flash + signature verify | Medium | Counter in signed manifest only |
| Backend validation | Server checks VIN+version | Medium | Requires connectivity |

### eFuse Anti-Rollback Example
```
eFuse bank (64 fuses):
  Version 1:  1000 0000 0000 ... (fuse 0 blown)
  Version 2:  1100 0000 0000 ... (fuse 1 blown)
  Version 3:  1110 0000 0000 ... (fuse 2 blown)

  Boot ROM reads fuse count → current minimum version = 3
  Any firmware with version < 3 is REJECTED by hardware

  After update to version 4: blow fuse 3 → 1111 0000 ...

  Note: Fuses cannot be unblown! This is permanent.
  OEM must carefully manage version increments.
```

## A/B Update Strategy (Dual-Bank)

```
┌────────────────────────────────────────────────┐
│ ECU Flash Memory                                │
├────────────────────┬───────────────────────────┤
│ Bank A (Active)    │ Bank B (Staging)           │
│ Running firmware   │ New firmware written here  │
│ v2.1.0            │ v2.2.0 (being installed)   │
├────────────────────┼───────────────────────────┤
│ Boot selector: A   │ After verification: → B    │
└────────────────────┴───────────────────────────┘

Update Flow:
1. Download new firmware → write to Bank B (inactive)
2. Verify Bank B integrity (hash check)
3. Atomically switch boot selector: A → B
4. Reboot → boot from Bank B (new firmware)
5. New firmware validates itself (self-test)
6. If self-test passes → mark Bank B as "confirmed"
7. If self-test fails → automatic rollback to Bank A

Advantages:
✓ No downtime during download (vehicle can drive)
✓ Instant rollback if update fails (boot from old bank)
✓ Power loss safe (atomic bank switch)
✓ No bricking risk (always have working fallback)
```

## Update Campaign Management

### Campaign Lifecycle
```
1. Development → Build → Sign → Package
2. Internal Testing (HiL, SiL, fleet test vehicles)
3. Staged Rollout:
   a. Canary (0.1% of fleet) — monitor 72 hours
   b. Early adopter (5%) — monitor 7 days
   c. General (25% batches) — monitor 48 hours per batch
   d. Full fleet
4. Monitoring: error rates, rollback rates, DTC spikes
5. Emergency halt: stop campaign if error rate > threshold
```

### Campaign Security Considerations
```
- Package availability: CDN with DDoS protection
- Bandwidth management: P2P update distribution (Tesla approach)
- User consent: Driver must approve (safety critical while driving)
- Installation window: Only when parked, ignition off, battery >50%
- Dependency management: ECU A update requires ECU B at version X first
- Partial failure recovery: If 3/10 ECUs updated and vehicle loses power
  → All ECUs must be able to operate in mixed-version state temporarily
```

## Uptane Framework

Standardized secure OTA framework for automotive (adopted by multiple OEMs):

```
Uptane Architecture:
┌────────────────────────────────────────────────┐
│ Repository Servers                              │
│                                                 │
│  ┌─────────────┐     ┌─────────────────────┐  │
│  │ Director    │     │ Image Repository     │  │
│  │ Repository  │     │ (Firmware Store)     │  │
│  │             │     │                       │  │
│  │ Per-vehicle │     │ Signed metadata +    │  │
│  │ targeting   │     │ firmware images      │  │
│  └──────┬──────┘     └──────────┬───────────┘  │
│         │                        │              │
└─────────┼────────────────────────┼──────────────┘
          │                        │
          ▼                        ▼
┌──────────────────────────────────────────────┐
│ Vehicle (Primary ECU)                         │
│  • Verifies Director metadata (freshness)    │
│  • Verifies Image repo metadata (integrity)  │
│  • Both must agree on target image           │
│  • Downloads and distributes to Secondary ECUs│
└──────────────────────────────────────────────┘

Key Security Properties:
1. Compromise resilience: Attacker must compromise BOTH Director + Image repo
2. Freshness: Timestamp metadata prevents freeze attacks (serving stale versions)
3. Mix-and-match prevention: Snapshot metadata prevents partial target list manipulation
4. Selective targeting: Director specifies exact versions for each VIN
```

## Threat Scenarios & Mitigations

| Threat | Attack | Mitigation |
|--------|--------|------------|
| Malicious firmware | Compromise build server | Code signing with HSM (offline key) |
| Rollback | Install old vulnerable version | Anti-rollback counter (eFuse/NVM) |
| Freeze attack | Prevent vehicle from seeing new update | Uptane freshness metadata (timestamp) |
| Partial bundle | Install incomplete update (mismatch) | Atomic A/B switching, dependency graph |
| Targeted attack | Push malicious update to specific VIN | Multi-signature, dual repository verification |
| DoS on update | Prevent update installation | Fallback CDN, local caching, retry logic |
| MitM on download | Modify package in transit | TLS + package signature verification |
| Key compromise | Attacker obtains signing key | Key rotation, multi-party signing, HSM audit log |
| Supply chain | Compromised third-party component | SBOM validation, binary composition analysis |

## UNECE R156 Requirements (Software Update Management System)

```
OEM must demonstrate:
1. Secure update delivery process
2. Software identification (RXSWIN) — identify SW version for type approval
3. Protect against unauthorized modification
4. Verify integrity and authenticity before installation
5. Protect update process against interruption
6. Safe failure handling (don't brick vehicle)
7. Log all update activities
8. Inform vehicle owner about update status
```
