# Automotive Threat Modeling

## Methodologies

### STRIDE (Microsoft)
Applied to vehicle systems — classify threats by category:

| Category | Description | Automotive Example |
|----------|-------------|-------------------|
| **S**poofing | Impersonate another entity | Fake ECU on CAN bus, forged V2X BSM |
| **T**ampering | Modify data in transit/at rest | Modify firmware, alter CAN frames |
| **R**epudiation | Deny performing an action | Deny OTA update installation, deny diagnostic session |
| **I**nformation Disclosure | Expose data to unauthorized entity | Sniff CAN traffic, extract keys from flash |
| **D**enial of Service | Disrupt availability | CAN bus flooding, bus-off attack |
| **E**levation of Privilege | Gain unauthorized access | Escape from IVI to gateway, unlock diagnostic services |

### PASTA (Process for Attack Simulation and Threat Analysis)
Seven-stage risk-centric methodology — well-suited for ISO/SAE 21434:

```
Stage 1: Define Objectives        → Safety/security goals for vehicle feature
Stage 2: Define Technical Scope   → ECU architecture, interfaces, data flows
Stage 3: Application Decomposition→ Trust boundaries, entry points, assets
Stage 4: Threat Analysis           → Known threats (CVE, TARA), attacker profiles
Stage 5: Vulnerability Analysis    → Static/dynamic analysis, pentesting results
Stage 6: Attack Modeling           → Attack trees, kill chains
Stage 7: Risk & Impact Analysis    → Severity (safety impact), likelihood, risk rating
```

### Attack Trees
Structured hierarchical representation of attacks:

```
                    [Steal Vehicle]
                    /       |       \
          [Relay Attack] [OBD Theft] [Key Cloning]
           /        \         |          |
   [Amplify Signal] [Jam TPMS] [CAN Inject] [Side-Channel]
```

### TARA (Threat Analysis and Risk Assessment) — ISO/SAE 21434
Required methodology for UNECE R155 compliance:

```
┌─────────────────────────────────────────────────────────────────────┐
│                      TARA PROCESS                                     │
├─────────────────────────────────────────────────────────────────────┤
│  1. Asset Identification                                             │
│     → Identify items of value (ECU firmware, keys, PII, safety)     │
│                                                                      │
│  2. Threat Scenario Identification                                   │
│     → What can go wrong? (STRIDE, known attacks, attacker goals)    │
│                                                                      │
│  3. Impact Rating                                                    │
│     → Safety (S0-S3), Financial (F0-F3), Operational (O0-O3),       │
│       Privacy (P0-P3)                                                │
│                                                                      │
│  4. Attack Path Analysis                                             │
│     → How can the threat be realized? (attack trees)                │
│                                                                      │
│  5. Attack Feasibility Rating                                        │
│     → Time, expertise, knowledge, window, equipment                 │
│       → Very Low / Low / Medium / High / Very High                  │
│                                                                      │
│  6. Risk Value Determination                                         │
│     → Risk = f(Impact, Attack Feasibility)                          │
│     → Risk levels: 1 (negligible) → 5 (unacceptable)               │
│                                                                      │
│  7. Risk Treatment Decision                                          │
│     → Avoid / Reduce / Transfer / Accept                            │
│                                                                      │
│  8. Cybersecurity Goals & Requirements                               │
│     → Derive security requirements for each unacceptable risk       │
└─────────────────────────────────────────────────────────────────────┘
```

## Attack Feasibility Assessment

### Rating Factors (ISO/SAE 21434 Annex H)

| Factor | Values | Description |
|--------|--------|-------------|
| Elapsed Time | ≤1 day / ≤1 week / ≤1 month / >6 months | Time to develop & execute |
| Specialist Expertise | Layman / Proficient / Expert / Multiple experts | Required skill level |
| Knowledge of Item | Public / Restricted / Confidential / Strictly confidential | Info needed |
| Window of Opportunity | Unlimited / Easy / Moderate / Difficult | Access constraints |
| Equipment | Standard / Specialized / Bespoke / Multiple bespoke | Tools required |

### Combined Rating Matrix

| Total Score | Feasibility | Interpretation |
|-------------|------------|----------------|
| 0-9 | High | Easily achievable by typical attacker |
| 10-13 | Medium | Achievable with moderate resources |
| 14-19 | Low | Requires significant investment |
| 20-24 | Very Low | Practically infeasible (nation-state) |
| ≥25 | Negligible | Theoretically possible only |

## Attack Surface Mapping

### External Attack Surfaces (Remote)
```
┌──────────────────────────────────────────────────────────────────┐
│ REMOTE (no physical access required)                              │
├──────────────────────────────────────────────────────────────────┤
│ • Cellular/LTE/5G (TCU) → Backend connectivity                   │
│ • Wi-Fi (IVI, hotspot) → Passenger/attacker in range             │
│ • V2X (DSRC/C-V2X) → Broadcast BSMs                             │
│ • Cloud/OTA servers → Supply chain, backend compromise           │
│ • Companion app → API vulnerabilities, credential theft           │
│ • GNSS → Spoofing navigation                                     │
└──────────────────────────────────────────────────────────────────┘
```

### Short-Range Attack Surfaces
```
┌──────────────────────────────────────────────────────────────────┐
│ SHORT RANGE (proximity required: meters to ~100m)                 │
├──────────────────────────────────────────────────────────────────┤
│ • Bluetooth/BLE (phone key, handsfree)                           │
│ • UWB (digital key ranging)                                       │
│ • TPMS (tire pressure, 315/433 MHz)                              │
│ • Key fob (RKE, 315/433/868 MHz) → Relay attack, rolljam        │
│ • NFC (digital key tap)                                           │
│ • EV charging (PLC, ISO 15118)                                   │
│ • Toll transponder (RFID)                                         │
└──────────────────────────────────────────────────────────────────┘
```

### Physical/Local Attack Surfaces
```
┌──────────────────────────────────────────────────────────────────┐
│ PHYSICAL (direct access to vehicle)                               │
├──────────────────────────────────────────────────────────────────┤
│ • OBD-II port → Diagnostic access, CAN injection                 │
│ • USB ports → Malicious media, firmware update                   │
│ • SD card slot → Map update, malicious content                   │
│ • JTAG/SWD debug ports → ECU flash read/write                    │
│ • CAN bus (direct wire) → Message injection                      │
│ • Ethernet (direct tap) → Traffic interception                   │
│ • Sensors (camera, radar, lidar) → Adversarial inputs            │
│ • Audio input (microphone) → Voice command injection             │
└──────────────────────────────────────────────────────────────────┘
```

## Example TARA: Remote Keyless Entry (RKE)

### Asset: Vehicle access control (lock/unlock/start)

| # | Threat Scenario | Impact | Feasibility | Risk | Treatment |
|---|----------------|--------|-------------|------|-----------|
| 1 | Relay attack on passive entry | S1/F3/O3/P0 → High | High (off-shelf tools, <$50) | 5 — Unacceptable | Reduce: UWB ranging, motion sensor |
| 2 | Rolling code prediction | S0/F3/O3/P0 → High | Low (requires reverse engineering) | 3 — Moderate | Reduce: AES-128 rolling code |
| 3 | RollJam (jam + capture) | S0/F3/O3/P0 → High | Medium (SDR + replay) | 4 — High | Reduce: Challenge-response, timeout |
| 4 | Brute force key fob | S0/F2/O2/P0 → Medium | Very Low (2^128 key space) | 1 — Acceptable | Accept |

### Cybersecurity Goals (from unacceptable risks):
- **CG-1**: Vehicle shall resist relay attacks with distance-bounding verification
- **CG-2**: Key fob protocol shall prevent replay of captured signals
- **CG-3**: Passive entry shall timeout after 30s without user interaction

## Example TARA: OTA Update System

| # | Threat Scenario | Impact | Feasibility | Risk | Treatment |
|---|----------------|--------|-------------|------|-----------|
| 1 | Malicious firmware injection | S3/F3/O3/P2 → Critical | Low (requires backend compromise) | 5 | Reduce: Code signing, secure boot |
| 2 | Rollback to vulnerable version | S2/F2/O2/P0 → High | Medium (modify update metadata) | 4 | Reduce: Anti-rollback counter |
| 3 | DoS on update server | S0/F1/O2/P0 → Medium | High (DDoS easy) | 3 | Reduce: CDN, fallback mechanism |
| 4 | MitM during download | S3/F3/O3/P1 → Critical | Low (TLS + cert pinning) | 2 | Accept (with current mitigations) |

## Trust Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                    VEHICLE TRUST ZONES                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Zone 5 (Highest Trust): Safety-Critical ECUs               │
│  ┌─────────────────────────────────────────────┐            │
│  │ Braking, Steering, Powertrain               │            │
│  │ HSM-protected, SecOC authenticated          │            │
│  └─────────────────────┬───────────────────────┘            │
│                         │ Gateway (firewall)                 │
│  Zone 4: ADAS / Autonomous Driving                          │
│  ┌─────────────────────┼───────────────────────┐            │
│  │ Sensor fusion, Path planning                │            │
│  │ Signed perception data                       │            │
│  └─────────────────────┬───────────────────────┘            │
│                         │ Gateway (filter)                   │
│  Zone 3: Body / Chassis                                     │
│  ┌─────────────────────┼───────────────────────┐            │
│  │ Windows, Doors, Lights, HVAC                │            │
│  │ SecOC on critical commands                   │            │
│  └─────────────────────┬───────────────────────┘            │
│                         │ Central Gateway                    │
│  Zone 2: Infotainment / Connectivity                        │
│  ┌─────────────────────┼───────────────────────┐            │
│  │ IVI, TCU, Wi-Fi, Bluetooth                  │            │
│  │ Sandboxed, limited CAN access               │            │
│  └─────────────────────┬───────────────────────┘            │
│                         │ Firewall / DMZ                     │
│  Zone 1 (Lowest Trust): External Interfaces                 │
│  ┌─────────────────────┼───────────────────────┐            │
│  │ OBD-II, USB, Charging, V2X                  │            │
│  │ Input validation, rate limiting              │            │
│  └─────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

## Threat Modeling Tools

| Tool | Type | Use Case |
|------|------|----------|
| Microsoft Threat Modeling Tool | DFD-based | General STRIDE analysis |
| OWASP Threat Dragon | DFD-based, open source | Web-based threat modeling |
| IriusRisk | Automated, questionnaire | Enterprise TARA at scale |
| Yakindu Security Analyst | Automotive-specific | ISO 21434 TARA compliance |
| securiCAD | Attack graph simulation | Probabilistic risk analysis |
| ANSYS medini analyze | Safety+Security | Combined HARA+TARA |
| draw.io / Miro | Manual | Lightweight attack trees |

## Deliverables (ISO/SAE 21434 §15)

A complete TARA document should contain:
1. **Item Definition** — System boundaries, interfaces, assumptions
2. **Asset Identification** — What we protect (data, functions, availability)
3. **Threat Scenarios** — STRIDE/catalog-based threats
4. **Impact Rating** — Safety, financial, operational, privacy scores
5. **Attack Trees / Paths** — How threats are realized
6. **Feasibility Rating** — Attacker effort assessment
7. **Risk Matrix** — Impact × Feasibility → Risk level
8. **Treatment Decisions** — Accept/reduce/avoid/transfer
9. **Cybersecurity Goals** — High-level security objectives
10. **Cybersecurity Requirements** — Specific implementation requirements
11. **Traceability** — Link requirements back to threats/risks
