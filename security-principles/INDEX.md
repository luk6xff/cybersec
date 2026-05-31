# Security Principles — Index

## Structure

```
security-principles/
├── INDEX.md                              ← You are here
│
├── cia-triad.md                          — CIA Triad, Parkerian Hexad, security models
├── defense-in-depth.md                   — Layered security controls, automotive DiD
├── zero-trust.md                         — Zero Trust Architecture (NIST 800-207)
│
├── risk-management.md                    — FAIR, NIST 800-30, TARA, risk registers
├── threat-modelling.md                   — STRIDE, PASTA, DREAD, attack trees, ISO 21434 TARA
├── vulnerability-management.md           — CVSS, scanning, prioritization, patch management
│
├── ssdlc.md                              — Secure SDLC, DevSecOps, SBOM, maturity models
├── security-governance.md                — Policies, roles, metrics, maturity, budgets
├── compliance-frameworks.md              — NIST CSF, ISO 27001, UN R155, GDPR, NIS2, IEC 62443
│
├── incident-response-and-management.md   — IR lifecycle, NIST framework, roles, pitfalls
├── cyber-kill-chain.md                   — Lockheed Martin kill chain, MITRE ATT&CK comparison
├── siem.md                               — SIEM architecture, capabilities, deployment
├── public-key-infrasttructure.md         — PKI, CAs, certificate lifecycle, trust chains
│
└── api/                                  — API security
    ├── api-authentication-and-authorization.md
    ├── api-secure-design.md
    ├── api-security-best-practices.md
    ├── api-threat-landscape.md
    ├── owasp-database-security-cheatsheet.md
    └── owasp-rest-api-security-cheatsheet.md
```

## Topic Map

| Category | Files | Key Content |
|----------|-------|-------------|
| **Foundations** | cia-triad, defense-in-depth, zero-trust | Core security properties, layered controls, modern architecture |
| **Risk & Threats** | risk-management, threat-modelling, vulnerability-management | Risk assessment (FAIR/NIST/TARA), threat analysis (STRIDE/PASTA), vuln lifecycle |
| **Process & Governance** | ssdlc, security-governance, compliance-frameworks | DevSecOps, policies, ISO 27001, UN R155, GDPR, NIS2 |
| **Operations** | incident-response, cyber-kill-chain, siem | IR lifecycle, kill chain, detection & monitoring |
| **Trust Infrastructure** | public-key-infrastructure | PKI, certificates, trust chains |
| **API Security** | api/* | Authentication, secure design, OWASP cheatsheets |

## Quick Reference: Which File for What?

| Question | Go To |
|----------|-------|
| "What security properties matter for my system?" | cia-triad.md |
| "How do I assess risk for my automotive product?" | risk-management.md (TARA section) |
| "How do I threat model my architecture?" | threat-modelling.md |
| "What vulnerability scanning tools should I use?" | vulnerability-management.md |
| "How do I build security into my development process?" | ssdlc.md |
| "What compliance standards apply to automotive?" | compliance-frameworks.md (UN R155, ISO 21434, TISAX) |
| "How do I structure a security organization?" | security-governance.md |
| "What does zero trust look like for vehicles?" | zero-trust.md (automotive section) |
| "How do I respond to a security incident?" | incident-response-and-management.md |
| "How do I set up layered defenses?" | defense-in-depth.md |
| "How does an attacker progress through an attack?" | cyber-kill-chain.md |
| "How do I secure my APIs?" | api/ directory |
