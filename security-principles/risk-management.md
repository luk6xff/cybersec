# Risk Management

## Core Concepts

**Risk** = Threat × Vulnerability × Impact (or Likelihood × Consequence)

| Term | Definition |
|------|-----------|
| **Asset** | Anything of value (data, systems, personnel, reputation) |
| **Threat** | Potential cause of an unwanted event (attacker, natural disaster, human error) |
| **Vulnerability** | Weakness exploitable by a threat |
| **Likelihood** | Probability the threat exploits the vulnerability |
| **Impact** | Consequence to the organization if risk materializes |
| **Risk Appetite** | Level of risk an organization is willing to accept |
| **Residual Risk** | Risk remaining after controls are applied |
| **Inherent Risk** | Risk before any controls |

---

## Risk Assessment Methodologies

### Qualitative Risk Assessment
Uses descriptive scales (Low/Medium/High/Critical) rather than numerical values.

**5×5 Risk Matrix:**
```
              Impact
           1   2   3   4   5
         ┌───┬───┬───┬───┬───┐
    5    │ 5 │10 │15 │20 │25 │  ← Almost Certain
         ├───┼───┼───┼───┼───┤
L   4    │ 4 │ 8 │12 │16 │20 │  ← Likely
i        ├───┼───┼───┼───┼───┤
k   3    │ 3 │ 6 │ 9 │12 │15 │  ← Possible
e        ├───┼───┼───┼───┼───┤
l   2    │ 2 │ 4 │ 6 │ 8 │10 │  ← Unlikely
y        ├───┼───┼───┼───┼───┤
    1    │ 1 │ 2 │ 3 │ 4 │ 5 │  ← Rare
         └───┴───┴───┴───┴───┘
           Negligible → Catastrophic

Score ranges: 1-4 Low | 5-9 Medium | 10-15 High | 16-25 Critical
```

### Quantitative Risk Assessment
Uses numerical/monetary values for precise calculation.

| Metric | Formula | Example |
|--------|---------|---------|
| **SLE** (Single Loss Expectancy) | Asset Value × Exposure Factor | €500,000 × 0.3 = €150,000 |
| **ARO** (Annualized Rate of Occurrence) | Expected frequency per year | 0.5 (once every 2 years) |
| **ALE** (Annualized Loss Expectancy) | SLE × ARO | €150,000 × 0.5 = €75,000/year |

If a control costs less than the ALE reduction it provides → control is justified.

### FAIR (Factor Analysis of Information Risk)
Industry standard for quantitative cyber risk analysis.

```
Risk
├── Loss Event Frequency (LEF)
│   ├── Threat Event Frequency (TEF)
│   │   ├── Contact Frequency
│   │   └── Probability of Action
│   └── Vulnerability (susceptibility)
│       ├── Threat Capability
│       └── Resistance Strength
└── Loss Magnitude (LM)
    ├── Primary Loss
    │   ├── Productivity
    │   ├── Response
    │   └── Replacement
    └── Secondary Loss
        ├── Fines & Judgments
        ├── Reputation
        └── Competitive Advantage
```

---

## Risk Assessment Frameworks

### NIST SP 800-30
Risk assessment methodology from NIST. Four-step process:
1. **Frame Risk** — Establish context (assumptions, constraints, risk tolerance, priorities)
2. **Assess Risk** — Identify threats, vulnerabilities, likelihood, impact
3. **Respond to Risk** — Select risk response (accept, avoid, mitigate, transfer, share)
4. **Monitor Risk** — Continuously verify effectiveness of controls

### ISO 27005
Information security risk management standard aligned with ISO 27001:
- Context establishment → Risk identification → Risk analysis → Risk evaluation → Risk treatment
- Emphasizes iterative approach and management review

### OCTAVE (Operationally Critical Threat, Asset, and Vulnerability Evaluation)
Carnegie Mellon methodology:
- **OCTAVE Allegro** (streamlined): Asset-centric, uses worksheets
- Focuses on organizational risk rather than technical vulnerability
- Identifies critical assets → maps threats → develops protection strategies

### FRAP (Facilitated Risk Analysis Process)
- Group-based collaborative risk assessment
- Stakeholders identify and evaluate risks together
- Fast (typically one day) but less rigorous than FAIR/NIST

### FMEA (Failure Modes and Effect Analysis)
Common in automotive/manufacturing (ISO 26262, AIAG):
- Identify potential failure modes
- Calculate RPN = Severity × Occurrence × Detection
- Prioritize mitigation for highest RPN items

### TARA (Threat Analysis and Risk Assessment) — ISO/SAE 21434
Automotive-specific:
- Asset identification → Threat scenario development → Impact rating → Attack path analysis → Attack feasibility rating → Risk determination → Risk treatment decision
- Uses attack feasibility instead of likelihood (considers attacker skill, equipment, access, time)
- Aligned with UN R155 cybersecurity regulation

---

## Risk Treatment Options

| Strategy | Description | Example |
|----------|-------------|---------|
| **Avoid** | Eliminate the risk by removing the activity | Don't deploy remote diagnostics if risk exceeds benefit |
| **Mitigate** | Reduce likelihood or impact with controls | Add encryption, IDS, access controls |
| **Transfer** | Shift risk to a third party | Cyber insurance, outsource to managed SOC |
| **Accept** | Acknowledge the risk without action | Low-impact risk below risk appetite threshold |
| **Share** | Distribute risk among multiple parties | Joint ventures, shared responsibility models |

---

## Risk Register

A living document tracking all identified risks:

| ID | Risk Description | Category | Likelihood | Impact | Risk Score | Owner | Treatment | Controls | Residual Risk | Review Date |
|----|-----------------|----------|-----------|--------|-----------|-------|-----------|----------|--------------|-------------|
| R-001 | Unauthorized CAN bus access | Technical | 3 | 5 | 15 (High) | Security Architect | Mitigate | Firewall, IDS, SecOC | 6 (Medium) | 2026-Q3 |
| R-002 | Supply chain malware | Supply Chain | 2 | 5 | 10 (High) | CISO | Mitigate+Transfer | SBOM, code signing, insurance | 4 (Low) | 2026-Q3 |
| R-003 | OTA update MITM | Technical | 2 | 4 | 8 (Medium) | OTA Lead | Mitigate | mTLS, code signing, rollback | 3 (Low) | 2026-Q4 |

---

## Risk-Based Decision Making

### Cost-Benefit Analysis for Security Controls
```
Control Value = (ALE_before - ALE_after) - Annual_Cost_of_Control

If Control Value > 0 → Implement the control
If Control Value ≤ 0 → Seek alternative or accept risk
```

### Risk Acceptance Criteria (example)
| Risk Level | Decision Authority | Required Documentation |
|------------|-------------------|----------------------|
| Critical (16-25) | Board / C-Suite | Full risk treatment plan + timeline |
| High (10-15) | CISO / VP Engineering | Risk treatment plan required |
| Medium (5-9) | Risk Owner / Manager | Documented acceptance with justification |
| Low (1-4) | Any staff member | Log in risk register |

---

## Continuous Risk Monitoring

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Identify   │────→│   Assess    │────→│   Treat     │────→│   Monitor   │
│  New Risks  │     │  & Analyze  │     │  & Control  │     │  & Review   │
└─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘
       ↑                                                           │
       └───────────────────────────────────────────────────────────┘
                            Continuous Cycle
```

Key activities:
- Regular risk reassessment (quarterly minimum, after changes)
- KRI (Key Risk Indicator) dashboards
- Threat intelligence integration
- Post-incident risk register updates
- Control effectiveness testing (audits, pen tests)

---

## References

- NIST SP 800-30 Rev. 1: Guide for Conducting Risk Assessments
- NIST SP 800-39: Managing Information Security Risk
- ISO 27005:2022: Information Security Risk Management
- ISO/SAE 21434: Road Vehicles — Cybersecurity Engineering
- FAIR Institute: https://www.fairinstitute.org/
- OWASP Risk Rating Methodology: https://owasp.org/www-community/OWASP_Risk_Rating_Methodology
