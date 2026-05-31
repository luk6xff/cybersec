# Security Governance

## Definition

Security governance is the system of policies, processes, standards, and organizational structures that ensure cybersecurity activities align with business objectives, manage risk effectively, and comply with legal/regulatory requirements.

---

## Governance vs Management vs Operations

| Level | Focus | Responsibility | Timeframe |
|-------|-------|---------------|-----------|
| **Governance** | Direction, oversight, accountability | Board, C-Suite | Strategic (years) |
| **Management** | Planning, implementation, coordination | CISO, security managers | Tactical (months) |
| **Operations** | Day-to-day execution | SOC, engineers, analysts | Operational (hours/days) |

---

## Governance Framework Structure

```
┌─────────────────────────────────────────────────┐
│              BOARD / EXECUTIVE MANAGEMENT         │
│  Sets risk appetite, approves strategy, oversight│
├─────────────────────────────────────────────────┤
│              SECURITY STEERING COMMITTEE          │
│  Cross-functional, reviews policies, budgets     │
├──────────────┬──────────────┬───────────────────┤
│   POLICIES   │  STANDARDS   │   PROCEDURES      │
│  (What)      │  (Measure)   │   (How)           │
├──────────────┼──────────────┼───────────────────┤
│  GUIDELINES  │   BASELINES  │   PLAYBOOKS       │
│  (Suggest)   │  (Minimum)   │   (Step-by-step)  │
└──────────────┴──────────────┴───────────────────┘
```

---

## Document Hierarchy

| Document | Purpose | Authority | Example |
|----------|---------|-----------|---------|
| **Policy** | High-level statement of intent and direction | Mandatory, board-approved | "All data at rest must be encrypted" |
| **Standard** | Specific, measurable requirements | Mandatory | "AES-256 with FIPS-validated module" |
| **Procedure** | Step-by-step instructions | Mandatory for covered processes | "Key rotation procedure for HSM" |
| **Guideline** | Recommended best practices | Advisory (not mandatory) | "Consider using Ed25519 for new SSH keys" |
| **Baseline** | Minimum acceptable configuration | Mandatory | "CIS Level 1 Benchmark for Ubuntu 22.04" |

---

## Essential Security Policies

| Policy | Covers |
|--------|--------|
| **Information Security Policy** | Overarching security direction, scope, objectives |
| **Acceptable Use Policy** | Rules for using organizational systems and data |
| **Access Control Policy** | Who gets access to what, authentication requirements |
| **Data Classification Policy** | Categories (Public, Internal, Confidential, Restricted) |
| **Incident Response Policy** | When/how to report, escalation procedures |
| **Business Continuity/DR Policy** | Recovery objectives, backup requirements |
| **Change Management Policy** | How changes are proposed, approved, implemented |
| **Vendor/Third-Party Security Policy** | Requirements for external partners |
| **Cryptographic Policy** | Approved algorithms, key management requirements |
| **Physical Security Policy** | Facility access, equipment handling |
| **Remote Work/BYOD Policy** | Device security, network access for remote users |
| **Software Development Security Policy** | SSDLC requirements, security gates |
| **Patch Management Policy** | Timelines, testing, exception handling |

---

## Roles & Responsibilities

### RACI Matrix (Cybersecurity)

| Activity | Board | CISO | IT Director | Security Team | All Staff |
|----------|-------|------|-------------|---------------|-----------|
| Set risk appetite | **A** | C | I | I | — |
| Security strategy | I | **A/R** | C | C | — |
| Policy approval | **A** | R | C | C | I |
| Risk assessment | I | **A** | C | **R** | — |
| Control implementation | — | A | **R** | **R** | — |
| Security monitoring | — | A | — | **R** | — |
| Incident response | I | **A** | C | **R** | I |
| Awareness training | — | A | — | R | **R** |
| Compliance reporting | **A** | **R** | C | C | — |

A = Accountable, R = Responsible, C = Consulted, I = Informed

### Key Roles

| Role | Responsibility |
|------|---------------|
| **CISO** | Overall security strategy, risk management, board reporting |
| **Security Architect** | Design secure systems, review architectures, technology standards |
| **Security Engineer** | Implement and maintain security controls |
| **SOC Analyst** | Monitor, detect, respond to security events |
| **GRC Manager** | Governance, risk, compliance management and reporting |
| **DPO** | Data protection compliance (GDPR requirement for some orgs) |
| **Product Security Lead** | Security for product development (critical in automotive) |

---

## Security Metrics & Reporting

### Board-Level Metrics (KRIs — Key Risk Indicators)
| Metric | Why It Matters |
|--------|---------------|
| Open critical/high vulnerabilities | Exposure level |
| Mean Time to Detect (MTTD) | Detection capability |
| Mean Time to Respond (MTTR) | Response capability |
| Security incidents by severity | Threat landscape |
| Compliance status (% controls met) | Regulatory risk |
| Phishing simulation click rate | Human risk |
| Patch compliance (% within SLA) | Hygiene level |
| Third-party risk score | Supply chain exposure |

### Operational Metrics
| Metric | Target |
|--------|--------|
| Security events processed/day | Tracking volume |
| False positive rate | < 20% |
| Alert-to-incident ratio | Trending improvement |
| Security training completion | > 95% |
| Assets with current inventory | > 98% |
| Password policy compliance | 100% |

### Reporting Cadence
| Audience | Frequency | Content |
|----------|-----------|---------|
| Board | Quarterly | KRIs, risk posture, major incidents, compliance status |
| Executive team | Monthly | Risk dashboard, security program progress, budget |
| Security committee | Biweekly | Operational metrics, project status, emerging threats |
| Security team | Weekly/Daily | Operational dashboards, ticket queues, incidents |

---

## Risk Governance

### Three Lines of Defense Model

```
┌─────────────────────────────────────────────────────────────────┐
│                   GOVERNING BODY / BOARD                          │
│              Oversight, accountability, direction                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1st Line          │  2nd Line              │  3rd Line           │
│  MANAGEMENT &      │  RISK & COMPLIANCE     │  INTERNAL AUDIT     │
│  OPERATIONS        │  FUNCTIONS             │                     │
│                    │                        │                     │
│  • Own and manage  │  • Policies/standards  │  • Independent      │
│    risk            │  • Monitor compliance  │    assurance        │
│  • Implement       │  • Risk frameworks     │  • Evaluate 1st &  │
│    controls        │  • Challenge 1st line  │    2nd line         │
│  • Day-to-day ops  │  • Advisory            │  • Report to board  │
│                    │                        │                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Security Program Maturity

### CMM-Based Maturity Levels

| Level | Name | Characteristics |
|-------|------|----------------|
| 1 | **Initial** | Ad-hoc, reactive, no formal processes |
| 2 | **Developing** | Some processes documented, inconsistent execution |
| 3 | **Defined** | Standardized processes, organization-wide policies |
| 4 | **Managed** | Measured and controlled, KPIs tracked |
| 5 | **Optimizing** | Continuous improvement, proactive, automated |

### Maturity Assessment Areas
- Governance & Strategy
- Risk Management
- Asset Management
- Identity & Access Management
- Threat Management
- Vulnerability Management
- Incident Response
- Security Architecture
- Data Protection
- Third-Party Management
- Security Awareness
- Compliance Management

---

## Budget & Resource Justification

### Approaches to Security Budget Justification

| Approach | Method |
|----------|--------|
| **Risk-based** | ALE reduction vs. control cost (quantitative) |
| **Benchmark** | Industry average security spend (typically 5-15% of IT budget) |
| **Compliance** | Cost of non-compliance (fines, lost contracts) |
| **Incident-driven** | Cost of recent breach × probability of recurrence |
| **Business enablement** | Security as revenue enabler (customer trust, contract requirements) |

### Common Budget Categories
- Personnel (50-60% typically)
- Tools and technology (20-30%)
- Consulting and professional services (10-15%)
- Training and awareness (5-10%)
- Incident response retainer
- Compliance/audit costs

---

## Automotive Governance (ISO/SAE 21434 CSMS)

Cybersecurity Management System requirements for automotive:

| Area | Requirements |
|------|-------------|
| **Organization** | Defined roles, culture of security, management support |
| **Process** | TARA, development security, production, post-production |
| **Competence** | Skilled personnel, continuous training |
| **Continuous improvement** | Lessons learned, monitoring, updates |
| **Supply chain** | Cybersecurity interface agreement (CIA), distributed activities |
| **Information sharing** | Threat intelligence, vulnerability disclosure |

The CSMS is audited for type approval under UN R155 — without it, vehicles cannot be sold in regulated markets.

---

## References

- ISO 27014: Information Security Governance
- NIST CSF 2.0: Govern function
- COBIT 2019: IT Governance Framework
- ISO/SAE 21434: Clause 5 (Organizational Cybersecurity Management)
- IIA Three Lines Model (2020)
- ISACA: Cybersecurity Governance
