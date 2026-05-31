# Compliance Frameworks & Standards

## Framework Landscape

```
┌──────────────────────────────────────────────────────────────────────┐
│                        GOVERNANCE FRAMEWORKS                          │
│   (What to do — organizational strategy and oversight)               │
│   NIST CSF, ISO 27001, COBIT                                        │
├──────────────────────────────────────────────────────────────────────┤
│                        CONTROL FRAMEWORKS                             │
│   (How to do it — specific security controls)                        │
│   NIST 800-53, CIS Controls, ISO 27002                              │
├──────────────────────────────────────────────────────────────────────┤
│                        REGULATIONS                                    │
│   (Must do — legal/regulatory requirements)                          │
│   GDPR, NIS2, UN R155, HIPAA, PCI DSS, SOX                         │
├──────────────────────────────────────────────────────────────────────┤
│                        INDUSTRY STANDARDS                             │
│   (Best practice for specific domains)                               │
│   ISO/SAE 21434, IEC 62443, TISAX, SOC 2                           │
└──────────────────────────────────────────────────────────────────────┘
```

---

## General Cybersecurity Frameworks

### NIST Cybersecurity Framework (CSF) 2.0

Six core functions (updated from 5 in CSF 2.0):

| Function | Purpose | Key Activities |
|----------|---------|----------------|
| **Govern** (new) | Establish cybersecurity risk management strategy | Risk strategy, roles, policies, supply chain |
| **Identify** | Understand organizational risk | Asset management, risk assessment, governance |
| **Protect** | Implement safeguards | Access control, training, data security, maintenance |
| **Detect** | Identify cybersecurity events | Monitoring, anomaly detection, continuous assessment |
| **Respond** | Take action on detected events | Response planning, communications, mitigation |
| **Recover** | Restore capabilities | Recovery planning, improvements, communications |

Implementation tiers: Partial (1) → Risk Informed (2) → Repeatable (3) → Adaptive (4)

### ISO/IEC 27001:2022
Information Security Management System (ISMS):
- **Plan-Do-Check-Act** cycle
- 93 controls in 4 themes (Organizational, People, Physical, Technological)
- Requires: Context, Leadership, Planning, Support, Operation, Performance Evaluation, Improvement
- Certification audit (Stage 1: documentation, Stage 2: implementation)
- Annual surveillance audits, 3-year recertification

### CIS Controls v8
20 → 18 prioritized safeguards grouped by implementation:

| IG1 (Essential) | IG2 (Standard) | IG3 (Advanced) |
|----------------|----------------|-----------------|
| Basic cyber hygiene | Established security program | Sophisticated defenses |
| 56 safeguards | +74 safeguards | +23 safeguards |
| All orgs should implement | Mid-size/regulated | Critical infrastructure, high-risk |

Top CIS Controls:
1. Inventory of Enterprise Assets
2. Inventory of Software Assets
3. Data Protection
4. Secure Configuration
5. Account Management
6. Access Control Management
7. Continuous Vulnerability Management
8. Audit Log Management

### NIST SP 800-53 Rev. 5
Comprehensive control catalog (1000+ controls) in 20 families:
- AC (Access Control), AU (Audit), AT (Awareness/Training), CM (Config Management)
- CP (Contingency Planning), IA (Identification/Authentication), IR (Incident Response)
- MA (Maintenance), MP (Media Protection), PE (Physical), PL (Planning)
- PM (Program Management), PS (Personnel), PT (PII Processing), RA (Risk Assessment)
- SA (System/Services Acquisition), SC (System/Comms Protection), SI (System Integrity)
- SR (Supply Chain Risk Management)

Control baselines: Low / Moderate / High (aligned with FIPS 199 classification)

---

## Automotive-Specific

### UN R155 (UNECE WP.29)
**Regulation on Cybersecurity and Cybersecurity Management System**

Mandatory for type approval in EU, Japan, Korea (since July 2022 for new types, July 2024 for all).

Requirements:
1. **CSMS** (Cybersecurity Management System) — organizational processes
2. **Vehicle type cybersecurity** — specific vehicle security measures
3. Must address threats across entire vehicle lifecycle
4. Incident monitoring and response capability
5. Security updates capability (relates to UN R156 for software updates)

CSMS must demonstrate:
- Risk management processes
- Vehicle development security (design → production → post-production)
- Threat detection and response
- Supply chain security oversight

### ISO/SAE 21434:2021
**Road Vehicles — Cybersecurity Engineering**

| Clause | Topic |
|--------|-------|
| 5 | Organizational cybersecurity management |
| 6 | Project-dependent cybersecurity management |
| 7 | Continuous cybersecurity activities |
| 8 | Risk assessment (TARA) |
| 9 | Concept phase |
| 10 | Product development |
| 11 | Cybersecurity validation |
| 12 | Production |
| 13 | Operations and maintenance |
| 14 | End of cybersecurity support / decommissioning |
| 15 | Distributed cybersecurity activities (supply chain) |

Key work products: Cybersecurity case, TARA, cybersecurity goals, cybersecurity concept, verification/validation reports

### TISAX (Trusted Information Security Assessment Exchange)
- Automotive industry information security standard (based on ISO 27001 + VDA ISA)
- Required by many OEMs for suppliers
- Three assessment levels: Normal, High, Very High
- Covers: Information security, Prototype protection, Data protection
- Exchange platform for sharing assessment results between companies

### IEC 62443
**Industrial Automation and Control Systems (IACS) Security**

| Part | Scope |
|------|-------|
| 62443-1-x | General concepts |
| 62443-2-x | Policies and procedures |
| 62443-3-x | System requirements |
| 62443-4-x | Component requirements |

Security Levels (SL): SL 1 (casual) → SL 2 (low motivation) → SL 3 (moderate) → SL 4 (nation-state)

Relevant for automotive manufacturing, EV charging infrastructure, industrial IoT.

---

## Data Protection & Privacy

### GDPR (General Data Protection Regulation)
EU regulation effective since May 2018:

| Principle | Requirement |
|-----------|-------------|
| Lawfulness, fairness, transparency | Legal basis for processing, clear communication |
| Purpose limitation | Collect for specified, explicit purpose only |
| Data minimization | Only collect what's necessary |
| Accuracy | Keep data correct and up-to-date |
| Storage limitation | Don't keep longer than needed |
| Integrity & confidentiality | Protect with appropriate technical measures |
| Accountability | Demonstrate compliance |

Key requirements:
- Data Protection Impact Assessment (DPIA) for high-risk processing
- 72-hour breach notification to supervisory authority
- Data Protection Officer (DPO) for certain organizations
- Right to erasure ("right to be forgotten")
- Data portability
- Fines: up to €20M or 4% of global annual turnover

### NIS2 Directive (EU)
Network and Information Security Directive 2 (effective October 2024):
- Expanded scope (more sectors including automotive manufacturing)
- Mandatory incident reporting (24h early warning, 72h notification, 1 month report)
- Supply chain security requirements
- Management body accountability (personal liability for C-level)
- Fines: up to €10M or 2% of global turnover
- Mandatory security measures: risk analysis, incident handling, business continuity, supply chain, encryption, access control, MFA

---

## Financial/Payment

### PCI DSS v4.0
Payment Card Industry Data Security Standard:
- 12 requirements across 6 goals
- Applies to anyone storing, processing, or transmitting cardholder data
- Goals: Build secure network, protect data, manage vulnerabilities, access control, monitor/test, maintain policy

### SOX (Sarbanes-Oxley)
- US financial reporting legislation
- IT controls over financial data integrity
- Requires internal controls documentation and audit

### SOC 2 (Service Organization Control)
- Trust Service Criteria: Security, Availability, Processing Integrity, Confidentiality, Privacy
- Type I: Point-in-time assessment
- Type II: Period assessment (6-12 months)
- Common requirement for SaaS/cloud service providers

---

## Healthcare

### HIPAA (Health Insurance Portability and Accountability Act)
- US regulation for Protected Health Information (PHI)
- Security Rule: Administrative, physical, technical safeguards
- Privacy Rule: Use and disclosure of PHI
- Breach Notification Rule: 60-day notification requirement

---

## Compliance Mapping

Many controls overlap. Map once, comply with many:

| Control Area | ISO 27001 | NIST CSF | CIS v8 | UN R155 | GDPR |
|-------------|-----------|----------|--------|---------|------|
| Asset inventory | A.5.9 | ID.AM | 1, 2 | — | Art. 30 |
| Access control | A.5.15-18 | PR.AC | 5, 6 | 7.3.3 | Art. 25, 32 |
| Encryption | A.8.24 | PR.DS | 3 | 7.3.4 | Art. 32 |
| Logging & monitoring | A.8.15-16 | DE.CM | 8 | 7.3.7 | Art. 32 |
| Incident response | A.5.24-28 | RS | — | 7.3.7 | Art. 33, 34 |
| Vulnerability mgmt | A.8.8 | ID.RA | 7 | 7.3.5 | Art. 32 |
| Supply chain | A.5.19-23 | ID.SC | 15 | 7.3.8 | Art. 28 |
| Risk assessment | A.5.12 | ID.RA | — | 7.2.2 | Art. 35 |

---

## Audit & Certification Process

```
1. Gap Assessment     → Identify what's missing vs. standard requirements
2. Remediation        → Implement controls and processes
3. Internal Audit     → Self-assessment of compliance
4. Pre-audit (opt.)   → Third-party readiness check
5. Certification Audit
   ├── Stage 1: Documentation review
   └── Stage 2: Implementation evidence
6. Certification      → Certificate issued (usually 3 years)
7. Surveillance       → Annual audits to maintain certification
8. Recertification    → Full audit at 3-year renewal
```

---

## References

- NIST CSF 2.0: https://www.nist.gov/cyberframework
- ISO 27001:2022: https://www.iso.org/standard/27001
- CIS Controls v8: https://www.cisecurity.org/controls
- UN R155: UNECE WP.29 Cybersecurity Regulation
- ISO/SAE 21434:2021: Road Vehicles — Cybersecurity Engineering
- GDPR: https://gdpr.eu/
- NIS2 Directive: https://digital-strategy.ec.europa.eu/en/policies/nis2-directive
- IEC 62443: https://www.iec.ch/
- PCI DSS v4.0: https://www.pcisecuritystandards.org/
