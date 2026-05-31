# Threat Modelling

## Overview

Threat modelling is the structured process of identifying threats, vulnerabilities, and attack vectors against a system, then determining countermeasures to mitigate risk. It answers four key questions:

1. **What are we building?** (System model, data flows, trust boundaries)
2. **What can go wrong?** (Threats, attack scenarios)
3. **What are we going to do about it?** (Mitigations, controls)
4. **Did we do a good job?** (Validation, review, iteration)

---

## Process Flow

```
┌────────────────┐    ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
│  1. Decompose  │───→│  2. Identify   │───→│  3. Rank &     │───→│  4. Determine  │
│  the System    │    │  Threats       │    │  Prioritize    │    │  Countermeasures│
└────────────────┘    └────────────────┘    └────────────────┘    └────────────────┘
                                                                          │
                                                                          ▼
                                                                   ┌────────────────┐
                                                                   │  5. Validate   │
                                                                   │  & Iterate     │
                                                                   └────────────────┘
```

### Step 1: Decompose the System
- Create Data Flow Diagrams (DFDs)
- Identify assets, entry points, trust boundaries
- Document external dependencies, technologies, privilege levels

### Step 2: Identify Threats
- Apply structured frameworks (STRIDE, PASTA, LINDDUN)
- Consider threat actors (nation-state, criminal, insider, hobbyist)
- Map to attack libraries (MITRE ATT&CK, CAPEC, CWE)

### Step 3: Rank & Prioritize
- Use DREAD, CVSS, or risk matrix scoring
- Consider attack feasibility (ISO/SAE 21434 for automotive)
- Focus resources on highest-risk threats

### Step 4: Countermeasures
- Map controls to threats
- Classify: prevent, detect, respond, recover
- Document residual risk

### Step 5: Validate & Iterate
- Verify mitigations through testing (pentest, fuzzing, code review)
- Update model when architecture changes
- Regular review cadence (sprint-level for Agile, milestone-based for V-model)

---

## Frameworks

### STRIDE (Microsoft)

| Category | Threat | Security Property Violated | Example |
|----------|--------|---------------------------|---------|
| **S**poofing | Impersonating another entity | Authentication | Forged CAN message sender ID |
| **T**ampering | Modifying data or code | Integrity | Altering firmware during OTA |
| **R**epudiation | Denying an action occurred | Non-repudiation | Deleting diagnostic logs |
| **I**nformation Disclosure | Exposing data to unauthorized party | Confidentiality | Extracting keys from ECU memory |
| **D**enial of Service | Making service unavailable | Availability | CAN bus flooding |
| **E**levation of Privilege | Gaining unauthorized access level | Authorization | Escaping sandbox to root |

**STRIDE-per-Element:** Apply STRIDE to each element in the DFD:
| DFD Element | Applicable STRIDE Categories |
|-------------|------------------------------|
| External Entity | S, R |
| Process | S, T, R, I, D, E |
| Data Store | T, R, I, D |
| Data Flow | T, I, D |

---

### PASTA (Process for Attack Simulation and Threat Analysis)

Seven-stage risk-centric methodology:

| Stage | Activity | Output |
|-------|----------|--------|
| 1. Define Objectives | Business objectives, compliance needs, risk appetite | Scope document |
| 2. Define Technical Scope | Architecture, technologies, dependencies | System diagrams, DFDs |
| 3. Application Decomposition | Data flows, trust boundaries, entry/exit points | Detailed DFD with trust zones |
| 4. Threat Analysis | Threat intelligence, threat actors, attack patterns | Threat library (CAPEC, ATT&CK mapped) |
| 5. Vulnerability Analysis | Static/dynamic analysis, known CVEs, misconfigs | Vulnerability list per component |
| 6. Attack Modelling | Attack trees, kill chains, exploitation scenarios | Attack tree diagrams |
| 7. Risk & Impact Analysis | Business impact, likelihood, risk scoring | Prioritized risk list + mitigations |

PASTA is **risk-centric** (considers business impact) vs STRIDE which is **threat-centric** (systematic enumeration).

---

### DREAD (Risk Scoring)

| Factor | Question | Scale |
|--------|----------|-------|
| **D**amage | How severe is the damage? | 1 (minimal) – 10 (complete compromise) |
| **R**eproducibility | How easy to reproduce? | 1 (difficult) – 10 (always works) |
| **E**xploitability | How easy to exploit? | 1 (expert + custom tools) – 10 (automated tool) |
| **A**ffected users | How many users affected? | 1 (single user) – 10 (all users) |
| **D**iscoverability | How easy to discover? | 1 (requires insider knowledge) – 10 (publicly visible) |

**Risk Score** = (D + R + E + A + D) / 5

| Score | Rating | Action |
|-------|--------|--------|
| 1–3 | Low | Monitor, address in normal cycle |
| 4–6 | Medium | Plan remediation, implement controls |
| 7–10 | High | Immediate action required |

---

### LINDDUN (Privacy-Focused)

| Category | Privacy Threat |
|----------|---------------|
| **L**inkability | Linking data items to same subject |
| **I**dentifiability | Identifying a subject from data |
| **N**on-repudiation | Inability to deny actions (privacy concern) |
| **D**etectability | Detecting existence of data/communication |
| **D**isclosure | Exposing personal information |
| **U**nawareness | Data processing without subject knowledge |
| **N**on-compliance | Violating privacy regulations (GDPR) |

Useful for systems processing personal data (connected vehicles, telematics, driver monitoring).

---

### Attack Trees

Hierarchical decomposition of an attack goal into sub-goals:

```
Root Goal: Steal Vehicle Cryptographic Keys
├── [OR] Extract from ECU Hardware
│   ├── [AND] Gain physical access to ECU
│   │   ├── Remove ECU from vehicle
│   │   └── Access debug port (JTAG/SWD)
│   └── [AND] Dump firmware
│       ├── Read flash via debug interface
│       └── Analyze binary for key storage
├── [OR] Intercept During OTA Update
│   ├── MITM the update channel
│   └── Compromise update server
├── [OR] Extract via Side-Channel
│   ├── Power analysis during crypto operation
│   └── Electromagnetic emanation analysis
└── [OR] Social Engineering
    ├── Phish developer with key access
    └── Bribe supply chain insider
```

Each leaf node gets an attack feasibility rating → propagate up to determine overall risk.

---

## Automotive Threat Modelling (ISO/SAE 21434 TARA)

### Attack Feasibility Rating

Instead of "likelihood," automotive uses **attack feasibility** based on:

| Parameter | Values |
|-----------|--------|
| Elapsed time | ≤1 day / ≤1 week / ≤1 month / ≤6 months / >6 months |
| Specialist expertise | Layman / Proficient / Expert / Multiple experts |
| Knowledge of item | Public / Restricted / Confidential / Strictly confidential |
| Window of opportunity | Unlimited / Easy / Moderate / Difficult / None |
| Equipment | Standard / Specialized / Bespoke / Multiple bespoke |

Sum of weighted scores → Attack Feasibility Level:
| Total | Feasibility |
|-------|-------------|
| 0–9 | High (easy to attack) |
| 10–13 | Medium |
| 14–19 | Low |
| 20–24 | Very Low |
| ≥25 | Infeasible |

### Impact Rating (ISO/SAE 21434)

| Category | Negligible | Moderate | Major | Severe |
|----------|-----------|----------|-------|--------|
| **Safety** | No injury | Light injuries | Severe injuries | Life-threatening/fatal |
| **Financial** | < €10 | €10–€1000 | €1000–€10,000 | > €10,000 (per stakeholder) |
| **Operational** | No effect | Minor degradation | Significant impact | Vehicle immobilized |
| **Privacy** | Anonymous | Identifiable, non-sensitive | Sensitive PII | Highly sensitive (health, location patterns) |

### Risk Matrix (Feasibility × Impact)

| | Negligible | Moderate | Major | Severe |
|---|---|---|---|---|
| **High Feasibility** | Low | Medium | High | Critical |
| **Medium Feasibility** | Low | Low | Medium | High |
| **Low Feasibility** | Low | Low | Low | Medium |
| **Very Low Feasibility** | Low | Low | Low | Low |

---

## Data Flow Diagram (DFD) Elements

```
┌─────────────────────────────────────────────────────────┐
│                    TRUST BOUNDARY                         │
│                                                          │
│  ┌──────────┐    Data Flow    ┌──────────────┐          │
│  │ External │ ──────────────→ │   Process    │          │
│  │  Entity  │                 │  (transforms │          │
│  └──────────┘                 │    data)     │          │
│                               └──────┬───────┘          │
│                                      │                   │
│                                      ▼                   │
│                               ┌──────────────┐          │
│                               │  Data Store  │          │
│                               │  (at rest)   │          │
│                               └──────────────┘          │
└─────────────────────────────────────────────────────────┘

External Entity = source/sink of data (user, external system)
Process         = transforms or processes data
Data Store      = persists data (database, file, HSM)
Data Flow       = movement of data between elements
Trust Boundary  = where privilege level or ownership changes
```

---

## Threat Modelling Tools

| Tool | Type | Use Case |
|------|------|----------|
| **Microsoft Threat Modeling Tool** | DFD-based | General applications, generates STRIDE threats |
| **OWASP Threat Dragon** | Open source, DFD-based | Web/API applications |
| **IriusRisk** | Commercial, automated | Enterprise, compliance-driven |
| **ThreatSpec** | Code-as-threat-model | DevSecOps, annotate code with threats |
| **draw.io / Miro** | General diagramming | Quick DFDs and attack trees |
| **securiCAD** | Automated attack simulation | Infrastructure and network |
| **CAIRIS** | Requirements + risk | Security requirements engineering |

---

## Integration with Development Lifecycle

| SDLC Phase | Threat Modelling Activity |
|-----------|--------------------------|
| **Requirements** | Identify security requirements, abuse cases, compliance needs |
| **Design** | Full threat model (DFD, STRIDE/PASTA), architecture review |
| **Implementation** | Validate code against identified threats, targeted code review |
| **Testing** | Derive test cases from threat model, pen test against attack trees |
| **Deployment** | Verify controls are deployed as designed |
| **Operations** | Update model for changes, feed incidents back into model |

---

## Common Mistakes

- Treating threat modelling as a one-time activity (should be iterative)
- Focusing only on technical threats (ignore business logic, privacy, safety)
- Not involving developers and architects (only security team models)
- Over-analysis paralysis (100 threats with no prioritization)
- Ignoring the "attacker perspective" (thinking only about defenses)
- Not linking threats to mitigations (identifying without acting)

---

## References

- OWASP Threat Modeling: https://owasp.org/www-community/Threat_Modeling
- Microsoft SDL Threat Modeling: https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling
- ISO/SAE 21434: Road Vehicles — Cybersecurity Engineering (TARA)
- MITRE ATT&CK: https://attack.mitre.org/
- CAPEC (Common Attack Pattern Enumeration): https://capec.mitre.org/
- Adam Shostack — "Threat Modeling: Designing for Security"
- LINDDUN: https://linddun.org/
