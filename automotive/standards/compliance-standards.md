# Automotive Cybersecurity Compliance & Standards

## Regulatory Landscape

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    AUTOMOTIVE CYBERSECURITY REGULATIONS                    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  INTERNATIONAL                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ UNECE WP.29                                                       │   │
│  │  ├── R155: Cybersecurity (CSMS) — Mandatory July 2024 (new types)│   │
│  │  └── R156: Software Updates (SUMS) — Mandatory July 2024         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  STANDARDS (normative references for R155 compliance)                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ ISO/SAE 21434: Cybersecurity Engineering (full lifecycle)         │   │
│  │ ISO 24089: Software Update Engineering                            │   │
│  │ ISO 11452/11451/11452: EMC (related immunity testing)            │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  REGIONAL                                                                 │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────────────┐    │
│  │ EU: Mandatory  │  │ China: GB/T  │  │ US: NHTSA guidelines    │    │
│  │ (R155 adopted) │  │ (own scheme) │  │ (voluntary, evolving)   │    │
│  └────────────────┘  └──────────────┘  └─────────────────────────┘    │
│                                                                           │
│  INDUSTRY                                                                 │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ TISAX (VDA ISA): Information Security Assessment (supply chain)  │   │
│  │ ASPICE: Automotive SPICE (process maturity)                       │   │
│  │ AUTOSAR: Secure communication specifications                      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

## UNECE R155 — Cybersecurity Management System (CSMS)

### What R155 Requires

```
Two-level approval:
  1. CSMS Certificate: Organization-level approval (process)
     → Demonstrate cybersecurity management capability
     → Valid for 3 years, audited by Technical Service

  2. Vehicle Type Approval: Vehicle-level approval (product)
     → Demonstrate cybersecurity for specific vehicle type
     → Requires valid CSMS certificate first
     → Evidence that TARA and mitigations are applied
```

### CSMS Requirements (Annex 5)

| Area | Requirement | Evidence |
|------|-------------|----------|
| 7.2.1 | Cybersecurity processes for vehicle development | Process documentation, roles, responsibilities |
| 7.2.2 | Identify and manage risks for vehicle types | TARA per vehicle type, risk treatment records |
| 7.2.3 | Risk assessment up to date | Periodic review, new threat monitoring |
| 7.2.4 | Mitigations tested and effective | Test reports, penetration test results |
| 7.2.5 | Supply chain management | Supplier cybersecurity requirements, audits |
| 7.2.6 | Monitoring and incident response | VSOC capability, incident response plan |
| 7.2.7 | Data forensics capability | Logging, evidence preservation |
| 7.2.8 | Relevant, proportionate mitigations | Cost-benefit, risk-based approach |

### R155 Annex 5 — Threat Catalog (Examples)

```
Category: Threats regarding back-end servers
  T1: Abuse of connectivity for attacks on vehicle
  T2: Services from backend disrupted
  T3: Unauthorized access to data on backend

Category: Threats regarding communication channels
  T4: Spoofing of messages from vehicle/infrastructure
  T5: Man-in-the-middle attack
  T6: Replay attack on communication

Category: Threats regarding vehicle update procedures
  T7: Compromise of OTA update process
  T8: Denial of legitimate updates
  T9: Manipulation of update packages

Category: Threats regarding unintended human actions
  T10: Legitimate actors manipulated (social engineering)
  T11: Unauthorized physical access enables attack

Category: Threats regarding external connectivity
  T12: Short-range wireless channels exploitation
  T13: Infection via external interfaces
  T14: Malicious apps on vehicle systems
```

## ISO/SAE 21434 — Cybersecurity Engineering

### Lifecycle Coverage

```
┌────────────────────────────────────────────────────────────────────────┐
│              ISO/SAE 21434 LIFECYCLE PHASES                              │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Clause 5-8: ORGANIZATIONAL (continuous)                               │
│  ──────────────────────────────────────────                            │
│  § 5: Organizational cybersecurity management                          │
│  § 6: Project-dependent cybersecurity management                       │
│  § 7: Distributed cybersecurity activities (supply chain)              │
│  § 8: Continual cybersecurity activities (monitoring, response)        │
│                                                                         │
│  Clause 9: CONCEPT PHASE                                               │
│  ──────────────────────────────────                                    │
│  § 9.3: Item definition                                                │
│  § 9.4: TARA (Threat Analysis and Risk Assessment)                     │
│  § 9.5: Cybersecurity concept                                          │
│                                                                         │
│  Clause 10-11: DEVELOPMENT                                             │
│  ──────────────────────────────                                        │
│  §10: Cybersecurity requirements & design                              │
│  §11: Implementation & integration verification                        │
│                                                                         │
│  Clause 12: VERIFICATION & VALIDATION                                  │
│  ──────────────────────────────────────                                │
│  §12: Cybersecurity validation (including penetration testing)         │
│                                                                         │
│  Clause 13-14: POST-DEVELOPMENT                                        │
│  ──────────────────────────────────                                    │
│  §13: Production (secure manufacturing)                                │
│  §14: Operations, maintenance, decommissioning                         │
│                                                                         │
│  Clause 15: TARA (detailed method)                                     │
│  ──────────────────────────────────                                    │
│  §15: Specific guidance on threat analysis and risk assessment         │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

### CAL (Cybersecurity Assurance Level) — ISO/SAE 21434 §6.4.3

```
CAL determines rigor of cybersecurity activities:

CAL 1 (Low): Minimal rigor
  → Basic TARA, standard testing, documentation review

CAL 2 (Medium): Standard rigor
  → Detailed TARA, structured verification, vulnerability analysis

CAL 3 (High): High rigor
  → Comprehensive TARA, penetration testing, formal methods consideration

CAL 4 (Highest): Stringent rigor
  → In-depth attack simulation, independent verification, state-of-art analysis

Note: CAL is assigned based on Risk Value from TARA
  Risk 1-2 → CAL 1
  Risk 3   → CAL 2
  Risk 4   → CAL 3
  Risk 5   → CAL 4
```

### Work Products (Key Deliverables)

| Clause | Work Product | Description |
|--------|-------------|-------------|
| §5 | Cybersecurity Policy | Organization commitment and approach |
| §5 | Cybersecurity Rules/Processes | Documented procedures |
| §6 | Cybersecurity Plan | Project-specific plan per item |
| §7 | Cybersecurity Interface Agreement | Supplier responsibilities |
| §8 | Cybersecurity Monitoring Report | Vulnerability watch, threat intel |
| §9 | TARA Report | Threats, risks, treatment decisions |
| §9 | Cybersecurity Concept | Goals, requirements, architecture |
| §10 | Cybersecurity Specification | Detailed security requirements |
| §11 | Verification Report | Testing evidence |
| §12 | Validation Report | Penetration test, compliance evidence |
| §13 | Production Control Plan | Key provisioning, secure manufacturing |
| §14 | Incident Response Plan | Detection, response, recovery |

## UNECE R156 — Software Update Management System (SUMS)

### Requirements
```
1. Secure update delivery process
2. Track software versions across fleet (RXSWIN)
3. Protect vehicle integrity during/after update
4. Ensure updates don't compromise safety/type approval
5. Inform driver before/after updates affecting type approval
6. Maintain update records for audit

RXSWIN (Regulatory Software Identification Number):
  Unique identifier linking software version to type approval
  If RXSWIN changes → may require new type approval!

  Implication: OTA updates that change type-approval-relevant SW
  need coordination with approval authority
```

## TISAX (Trusted Information Security Assessment Exchange)

```
VDA ISA (Information Security Assessment) based on ISO 27001

Scope: Entire automotive supply chain information security

Assessment Levels:
  Level 1: Self-assessment (not shared)
  Level 2: Remote audit by provider
  Level 3: On-site audit by provider (required for most OEM contracts)

Assessment Objectives:
  - Information Security (mandatory)
  - Prototype Protection (if handling pre-production parts)
  - Data Protection (if handling personal data)

For cybersecurity suppliers specifically:
  → Must demonstrate secure development environment
  → Code signing infrastructure security
  → Key management and access control
  → Incident response capability
  → Employee security awareness
```

## Supply Chain Requirements (ISO/SAE 21434 §7)

### Cybersecurity Interface Agreement (CIA)
```
OEM → Tier 1 → Tier 2 supplier chain requires:

1. Cybersecurity Requirements Specification
   - Security requirements flow-down to suppliers
   - Reference to applicable standards/regulations

2. Distributed Cybersecurity Activities
   - Who performs TARA? (OEM? Supplier? Joint?)
   - Who implements security mechanisms?
   - Who verifies/validates?

3. Cybersecurity Case
   - Supplier provides evidence of compliance
   - Vulnerability disclosure obligations
   - Incident notification timeline

4. End-of-Support Commitments
   - How long will supplier patch vulnerabilities?
   - Support for security monitoring data
```

### Supplier Cybersecurity Assessment

| Criterion | Required Evidence |
|-----------|------------------|
| CSMS capability | ISO/SAE 21434 conformance statement or TISAX |
| Secure development | ASPICE CYB.1 (Cybersecurity process) at Level 2+ |
| Vulnerability management | Process for disclosure, tracking, patching |
| Incident response | Defined process, SLA for notification |
| Key management | HSM usage, key generation/storage/rotation |
| Access control | Development environment protection |
| SBOM | Software Bill of Materials for supplied components |

## Audit Preparation Checklist

### For CSMS Certificate (R155)
```
□ Cybersecurity policy signed by management
□ Cybersecurity organization chart (roles: CSMS Manager, analysts, etc.)
□ Documented TARA methodology with examples
□ Risk treatment process and criteria
□ Supply chain cybersecurity requirements
□ Monitoring and incident response capability (VSOC)
□ Post-production vulnerability management process
□ Evidence of security testing (pentest reports)
□ Training records for cybersecurity staff
□ Change management process for security-relevant changes
□ Configuration management for security artifacts
□ Decommissioning procedure (key erasure, data wipe)
```

### For Vehicle Type Approval (R155)
```
□ Valid CSMS certificate (prerequisite)
□ Item definition for vehicle type
□ Complete TARA for all items in scope
□ Cybersecurity concept and requirements
□ Verification and validation evidence
□ Penetration test report (by qualified lab)
□ Residual risk acceptance rationale
□ Post-production monitoring plan for this type
□ Software update capability demonstration (if applicable)
□ Mapping to R155 Annex 5 threat catalog
```

## Timeline & Enforcement

```
July 2022:  R155/R156 entered into force (EU, Japan, Korea)
July 2024:  Mandatory for ALL new vehicle types
July 2026:  Mandatory for ALL new vehicles produced (including existing types)

Consequence of non-compliance:
  → Vehicle type approval DENIED or WITHDRAWN
  → Cannot sell vehicle in R155-contracting countries
  → Criminal penalties possible in some jurisdictions

Countries enforcing R155:
  EU (all member states), UK, Japan, South Korea, Australia

Countries NOT yet enforcing:
  USA (NHTSA voluntary guidelines), China (own scheme GB/T), India (developing)
```
