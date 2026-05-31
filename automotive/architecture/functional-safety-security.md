# Functional Safety & Security Co-Engineering

## Why Safety & Security Together?

```
Traditional: Safety (ISO 26262) and Security (ISO/SAE 21434) done separately
Problem:     Security attacks can cause safety hazards!
             Safety measures can interfere with security mechanisms!

Example:
  Attack: CAN injection → fake brake request → unintended braking → crash

  This is BOTH:
  - Safety violation (ASIL-D hazard: unintended vehicle movement)
  - Security violation (unauthorized command execution)

  Must be addressed by BOTH disciplines jointly!
```

## Standards Relationship

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTOMOTIVE STANDARDS MAP                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Safety                          Security                       │
│  ──────                          ────────                       │
│  ISO 26262 (Road vehicles –      ISO/SAE 21434 (Road vehicles – │
│  Functional Safety)              Cybersecurity engineering)      │
│                                                                  │
│      ↕  ← Interaction →  ↕                                     │
│                                                                  │
│  HARA (Hazard Analysis &         TARA (Threat Analysis &        │
│  Risk Assessment)                Risk Assessment)               │
│  → ASIL rating (QM, A-D)        → Risk levels (1-5)            │
│  → Safety Goals                  → Cybersecurity Goals          │
│  → Safety Requirements           → Security Requirements        │
│                                                                  │
│  SOTIF (ISO 21448)               UNECE R155 / R156              │
│  Safety of the Intended          Regulatory cybersecurity       │
│  Functionality                   and software updates            │
│                                                                  │
│  ISO/PAS 21448:                  ISO/SAE 21434 Annex G:         │
│  Triggering conditions,          "Interaction with Safety"       │
│  sensor limitations              → Joint analysis required       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## ASIL Levels (ISO 26262)

| ASIL | Severity | Probability | Controllability | Example |
|------|----------|-------------|-----------------|---------|
| QM | Low | Low | High | Window control |
| A | Low/Med | Low | Medium | Wiper malfunction |
| B | Medium | Medium | Medium | Headlight failure |
| C | High | Medium | Low | Unintended acceleration |
| D | Critical | High | Low | Steering/braking loss |

## Security Impact on Safety

### Attack Scenarios with Safety Impact

| Attack | Safety Hazard | ASIL | Security Mitigation Required |
|--------|--------------|------|------------------------------|
| CAN injection: fake brake cmd | Unintended braking | D | SecOC, message authentication |
| Steering ECU firmware tamper | Loss of steering assist | D | Secure boot, anti-rollback |
| Sensor spoofing (radar/lidar) | ADAS wrong decision | D | Sensor fusion, plausibility checks |
| DoS on CAN bus | Safety messages lost | D | Bus guardian, redundant path |
| GNSS spoofing | Wrong navigation → danger | B | Multi-source positioning, INS |
| OTA malicious update to ABS | Brake algorithm corrupted | D | Code signing, safe state fallback |
| Gateway compromise | All buses accessible | D | Defense in depth, compartmentalization |
| V2X fake emergency brake msg | Unintended hard braking | C | SCMS verification, plausibility |

### Safe State Transitions

```
Normal Operation → Attack Detected → Degraded Mode → Safe State

Degraded Modes:
├── Limp Home Mode: Reduced speed (30km/h), limited features
├── Driver Warning: Alert driver, request manual takeover (ADAS)
├── Feature Disable: Turn off compromised feature, rest works
├── Communication Fallback: Switch to backup bus/path
└── Full Safe State: Controlled stop (autonomous vehicle)

Design Principle:
  "A security failure must NEVER lead to an unsafe state"
  "Security mechanisms must not interfere with safety functions"

Example conflict:
  - Security wants to BLOCK suspicious CAN message
  - But that message is ABS control → blocking causes safety hazard!

Resolution:
  - Safety-critical messages get through (even if suspicious)
  - Log the anomaly for later analysis
  - Apply defense at source (authenticate sender) not at receiver (block)
```

## Co-Engineering Process

### Joint HARA + TARA Workflow
```
Step 1: Item Definition (shared between safety & security)
  └── Same system boundary, same interfaces

Step 2: Parallel Analysis
  ├── Safety: HARA → identify hazardous events → ASIL
  └── Security: TARA → identify threat scenarios → Risk Level

Step 3: Cross-Check (critical step!)
  ├── For each security threat: can it cause a safety hazard?
  │   If YES → inherit ASIL from the safety goal it violates
  │
  └── For each safety mechanism: can an attacker bypass it?
      If YES → security requirement to protect the safety mechanism

Step 4: Combined Requirements
  ├── Security requirements tagged with ASIL impact
  ├── Safety requirements tagged with security assumptions
  └── Shared verification activities

Step 5: Verification
  ├── Safety testing (fault injection, FMEA)
  ├── Security testing (penetration test, fuzzing)
  └── Combined testing (security attack → check safety response)
```

### Requirements Interaction Examples

```
Safety Requirement (ISO 26262):
  "The braking system shall respond to a valid brake request within 150ms (ASIL-D)"

  Security assumption: "The brake request is authenticated (cannot be spoofed)"
  → Derives security requirement:
  "Brake CAN messages shall be authenticated with CMAC (SecOC),
   verification time < 10ms to not violate 150ms deadline"

  Security constraint on safety:
  "SecOC verification overhead must not exceed 10ms for ASIL-D messages"
  → Safety mechanism (plausibility check) as fallback if SecOC fails
```

## Secure Hardware for Safety-Critical ECUs

### Hardware Security Module (HSM) in Safety Context
```
┌──────────────────────────────────────────────┐
│ Safety-Critical ECU (e.g., Brake Controller)  │
├──────────────────────────────────────────────┤
│                                               │
│  ┌─────────────┐     ┌──────────────────┐   │
│  │ Application │     │ HSM (SHE+/EVITA) │   │
│  │ (ASIL-D)    │     │                  │   │
│  │             │←───→│ • SecOC CMAC     │   │
│  │ Brake algo  │     │ • Secure Boot    │   │
│  │ SafetyMgr   │     │ • Key Storage    │   │
│  │             │     │ • Random Gen     │   │
│  └─────────────┘     └──────────────────┘   │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │ Safety Mechanisms                        │ │
│  │ • Dual-core lockstep (computation)       │ │
│  │ • ECC on RAM/Flash (data integrity)      │ │
│  │ • Watchdog (execution monitoring)        │ │
│  │ • MPU (memory protection)                │ │
│  │ • Voltage/clock monitoring               │ │
│  └─────────────────────────────────────────┘ │
│                                               │
│  Security adds: HSM, SecOC, Secure Boot       │
│  Must NOT interfere with safety timing!       │
│  HSM WCET (Worst Case Execution Time)         │
│  must be included in safety timing budget     │
│                                               │
└──────────────────────────────────────────────┘
```

## Timing Constraints: Security vs Safety

| Operation | Typical Duration | Safety Budget Impact |
|-----------|-----------------|---------------------|
| SecOC CMAC-128 generate | 5-15 µs (with HSM) | Minimal |
| SecOC CMAC verify | 5-15 µs | Adds to message processing |
| Secure boot (MCU) | 50-200 ms | Extends boot time |
| Secure boot (SoC/Linux) | 2-5 seconds | Significant for ADAS startup |
| TLS handshake | 50-200 ms | Not for real-time paths |
| Certificate verification | 10-50 ms | Use for session setup only |

### Design Rule:
```
Safety-critical path (CAN message → ECU action):
  Total budget: 10ms (ASIL-D typical)

  Breakdown:
  ├── CAN reception: 1ms
  ├── SecOC verification: 0.05ms (50µs with HSM)  ← Security overhead
  ├── Signal extraction: 0.5ms
  ├── Application logic: 5ms
  ├── Output actuation: 2ms
  └── Margin: 1.45ms

  Security overhead (0.05ms) is < 1% of budget → ACCEPTABLE

  If security added 5ms overhead → would violate safety timing → NOT ACCEPTABLE
  → Need faster HSM or different security approach
```

## Compliance Mapping

| Requirement | ISO 26262 Reference | ISO/SAE 21434 Reference |
|-------------|--------------------|-----------------------|
| Risk assessment | Part 3: HARA | §15: TARA |
| Development process | Part 4-7: V-model | §10-11: Concept & Development |
| Verification | Part 4.8, 5.9 | §12: Verification |
| Production | Part 7 | §13: Production |
| Operations | Part 7.6 | §14: Operations/Maintenance |
| Decommissioning | Part 7.6.4 | §14.4: Decommissioning |
| Supply chain | Part 8: Supporting | §7: Distributed development |

## Key Takeaways for Principal Engineers

1. **Never analyze safety and security in isolation** — attacks cause hazards
2. **Security mechanisms have timing cost** — must fit within safety deadlines
3. **Safety mechanisms need security protection** — integrity of safety code/data
4. **ASIL inheritance** — security threats that impact safety inherit the ASIL level
5. **Safe state must be reachable** — even under active attack
6. **Redundancy helps both** — dual paths improve safety AND resist single-point attacks
7. **Document the interaction** — auditors (R155 + type approval) require evidence of joint analysis
