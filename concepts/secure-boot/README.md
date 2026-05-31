# Secure Boot and Chain of Trust

## Concept
Secure boot ensures that only authenticated, unmodified software executes on a device. It establishes a **chain of trust** from an immutable Root of Trust (RoT) through every stage of the boot process.

## Chain of Trust

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Chain of Trust                                 │
│                                                                      │
│  ┌─────────┐    ┌──────────┐    ┌───────────┐    ┌───────────────┐ │
│  │  RoT    │───→│ 1st Stage│───→│ 2nd Stage │───→│  Application  │ │
│  │(BootROM)│    │Bootloader│    │ Bootloader│    │    / RTOS     │ │
│  │         │    │          │    │           │    │               │ │
│  │Immutable│    │Verify sig│    │Verify sig │    │Verify sig     │ │
│  │OTP key  │    │of next   │    │of next    │    │(runtime       │ │
│  │         │    │stage     │    │stage      │    │ integrity)    │ │
│  └─────────┘    └──────────┘    └───────────┘    └───────────────┘ │
│       │              │                │                │             │
│    eFuse/OTP     Flash Partition  Flash Partition   Flash Partition  │
│    Root PK Hash  + Signature     + Signature       + Signature      │
└─────────────────────────────────────────────────────────────────────┘
```

## Automotive Secure Boot Implementations

### MCU-based ECU (e.g., Infineon AURIX TC3xx)

```
Power-On
   │
   ▼
┌──────────────────────────────────────┐
│ HPSE BootROM (Hardware)              │
│ • Read root public key hash from OTP │
│ • Load HPSE firmware from flash      │
│ • Verify HPSE FW signature           │
│ • If fail → halt, set error flag     │
└──────────────┬───────────────────────┘
               │ (HPSE holds app cores in reset)
               ▼
┌──────────────────────────────────────┐
│ HPSE Firmware (Verified)             │
│ • Load application bootloader        │
│ • Verify signature against root key  │
│ • If fail → try backup partition     │
│ • If pass → release app core 0       │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│ Application Bootloader               │
│ • Initialize peripherals             │
│ • Load application from flash        │
│ • Verify application signature       │
│ • If pass → jump to application      │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│ Application (AUTOSAR / Custom)       │
│ • Normal ECU operation               │
│ • Optional runtime integrity checks  │
└──────────────────────────────────────┘
```

### SoC-based ECU (e.g., NXP S32G, Qualcomm SA8xx)

Multi-stage boot with ARM TrustZone:

| Stage | Component | Trust |
|-------|-----------|-------|
| BL1 | BootROM (SoC) | Hardware RoT, OTP keys |
| BL2 | Trusted Firmware-A | Verified by BL1, sets up TrustZone |
| BL31 | Secure Monitor (EL3) | Runtime secure world services |
| BL32 | Secure OS (OP-TEE) | Trusted execution environment |
| BL33 | Normal World Bootloader (U-Boot) | Loads Linux/Hypervisor |
| OS | Linux/QNX/Hypervisor | Application environment |

## Signature Verification Methods

### Hash + RSA/ECDSA
```
Sign (at build time):
  hash = SHA-256(firmware_binary)
  signature = ECDSA_Sign(private_key, hash)
  package = firmware_binary || signature || certificate

Verify (at boot):
  hash' = SHA-256(received_firmware)
  valid = ECDSA_Verify(public_key, hash', signature)
  if valid → proceed; else → halt
```

### Code Authentication Container (NXP)
```
┌──────────────────────────────────┐
│ Container Header                  │
│ • Signature algorithm             │
│ • Key index                       │
│ • Image entry point               │
├──────────────────────────────────┤
│ Signature Block                   │
│ • RSA/ECDSA signature             │
│ • Certificate (public key)        │
├──────────────────────────────────┤
│ Firmware Image (encrypted, opt.)  │
└──────────────────────────────────┘
```

## Measured Boot vs Secure Boot

| Property | Secure Boot | Measured Boot |
|----------|-------------|---------------|
| Action on failure | Halt/refuse boot | Log measurement, continue |
| Mechanism | Signature verification | Hash extension into PCR/TPM |
| Trust decision | Local (ECU decides) | Remote (attestation server) |
| Flexibility | Binary pass/fail | Gradual trust, policy-based |
| Standard | Vendor-specific | TCG TPM, DICE |

## Anti-Rollback Protection

Prevent attacker from flashing an older (vulnerable) firmware version:

1. **Monotonic counter** in HSM/OTP:
   - Each firmware has a version number
   - Counter incremented on successful update
   - Boot refuses firmware with version < counter value

2. **Anti-rollback fuse**:
   - Hardware fuse blown per major version
   - Physically irreversible

## Common Attacks & Mitigations

| Attack | Description | Mitigation |
|--------|-------------|------------|
| Fault injection | Glitch voltage to skip verification | Redundant checks, HW detection |
| TOC/TOU | Modify image between check and use | Verify in-place, lock memory |
| Rollback | Flash vulnerable old firmware | Monotonic counter / fuses |
| Key extraction | Read root key from debug port | OTP storage, debug disable |
| Compression bomb | Overflow memory during decompress | Verify before decompress |
| Parallel boot race | Tamper via parallel core | Hold all cores in reset until verified |
