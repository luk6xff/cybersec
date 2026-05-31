# Secure Software Development Lifecycle (SSDLC)

## Why Shift Left?

Cost of fixing vulnerabilities increases exponentially the later they're found:

```
Phase:        Requirements → Design → Implementation → Testing → Production
Cost Factor:       1×          5×          10×            20×        100×
```

Integrating security at every phase catches issues early, reduces business risk, and avoids costly rework.

---

## SSDLC vs Traditional SDLC

| Traditional SDLC | Secure SDLC |
|------------------|-------------|
| Security testing at the end | Security integrated at every phase |
| Security team as gatekeepers | Security as shared responsibility |
| Penetration test before release | Continuous security activities |
| Compliance-driven | Risk-driven |
| Fixes are expensive patches | Fixes are design decisions |

---

## Phase-by-Phase Security Activities

### 1. Requirements & Planning
| Activity | Description | Tools/Methods |
|----------|-------------|---------------|
| Security requirements | Define security/privacy requirements alongside functional ones | OWASP ASVS, abuse cases |
| Compliance mapping | Identify regulatory requirements (GDPR, ISO 21434, UN R155) | Compliance matrix |
| Risk assessment | Initial risk classification of the project | FAIR, qualitative matrix |
| Data classification | Identify sensitive data and handling requirements | Data flow mapping |

**Key outputs:** Security requirements document, abuse cases, data classification, compliance checklist

### 2. Architecture & Design
| Activity | Description | Tools/Methods |
|----------|-------------|---------------|
| Threat modelling | STRIDE/PASTA analysis of architecture | Microsoft TMT, OWASP Threat Dragon |
| Secure design patterns | Apply security patterns (defense-in-depth, least privilege, fail-secure) | Design review checklist |
| Architecture review | Security-focused review of design decisions | SARA (Software Architecture Review and Assessment) |
| Crypto selection | Choose appropriate algorithms, key lengths, protocols | NIST guidelines, BSI recommendations |

**Key outputs:** Threat model, architecture security review report, design decisions log

### 3. Implementation
| Activity | Description | Tools/Methods |
|----------|-------------|---------------|
| Secure coding standards | Language-specific secure coding guidelines | CERT C/C++, OWASP Secure Coding |
| SAST (Static Analysis) | Automated source code scanning | SonarQube, Semgrep, CodeQL, Coverity |
| Code review | Security-focused peer review | Pull request review, Crucible |
| SCA (Software Composition Analysis) | Check dependencies for known vulns | Snyk, Dependabot, OWASP Dep-Check |
| Secret scanning | Detect hardcoded credentials/keys | GitLeaks, TruffleHog |

**Key outputs:** Clean SAST/SCA reports, reviewed code, SBOM (Software Bill of Materials)

### 4. Testing & Verification
| Activity | Description | Tools/Methods |
|----------|-------------|---------------|
| DAST (Dynamic Analysis) | Test running application | Burp Suite, OWASP ZAP, Nuclei |
| Penetration testing | Manual security testing by experts | Internal team or third party |
| Fuzzing | Input mutation testing for crashes/vulns | AFL++, libFuzzer, Peach |
| Security regression tests | Automated tests for previously found vulns | CI test suite |
| IAST (Interactive Analysis) | Instrument running app during QA testing | Contrast Security |

**Key outputs:** Pentest report, fuzz results, security test pass/fail gate

### 5. Release & Deployment
| Activity | Description | Tools/Methods |
|----------|-------------|---------------|
| Security gate review | Final go/no-go based on security criteria | Sign-off checklist |
| Container/image scanning | Scan deployment artifacts | Trivy, Grype |
| Configuration hardening | Validate production configs against baseline | CIS Benchmarks, SCAP |
| SBOM generation | Generate and publish software bill of materials | CycloneDX, SPDX |

**Key outputs:** Release security sign-off, deployment hardening report, published SBOM

### 6. Operations & Maintenance
| Activity | Description | Tools/Methods |
|----------|-------------|---------------|
| Vulnerability monitoring | Continuous scanning + CVE monitoring | Qualys, Nessus, CISA KEV |
| Incident response | Detect and respond to security events | SIEM, EDR, IR playbooks |
| Patch management | Timely application of security updates | Automated patching pipelines |
| Security monitoring | Runtime protection and anomaly detection | RASP, WAF, IDS/IPS |
| Post-incident review | Feed lessons back into requirements | Blameless postmortems |

**Key outputs:** Vulnerability reports, incident reports, updated threat models

---

## DevSecOps Pipeline Integration

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  Code   │──→│  Build  │──→│  Test   │──→│ Release │──→│ Deploy  │──→│ Monitor │
└────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘
     │              │              │              │              │              │
  Pre-commit     SAST           DAST          Sign-off      Image scan     SIEM
  Lint + Secrets  SCA           Pentest       SBOM          IaC scan       EDR
  Code review     Build scan    Fuzz          Approval      Hardening      WAF
                  SBOM gen      IAST                        Config audit   Alerting
```

### Quality Gates (Break the Build)

| Gate | Criteria | Action on Failure |
|------|----------|-------------------|
| Pre-commit | No secrets, passes linter | Block commit |
| Build | No critical/high SAST findings, no critical SCA vulns | Fail pipeline |
| Test | Pentest findings ≤ Medium, fuzz coverage met | Block release |
| Release | Security sign-off, SBOM complete | Hold deployment |
| Deploy | No critical image vulns, hardening baseline met | Rollback |

---

## Maturity Models

### OWASP SAMM (Software Assurance Maturity Model)

Five business functions, each with three security practices:

| Business Function | Security Practices |
|------------------|--------------------|
| **Governance** | Strategy & Metrics, Policy & Compliance, Education & Guidance |
| **Design** | Threat Assessment, Security Requirements, Security Architecture |
| **Implementation** | Secure Build, Secure Deployment, Defect Management |
| **Verification** | Architecture Assessment, Requirements-driven Testing, Security Testing |
| **Operations** | Incident Management, Environment Management, Operational Management |

Each practice scored 0–3 maturity level. Enables roadmap planning and benchmarking.

### BSIMM (Building Security In Maturity Model)
- Observation-based (what companies actually do vs. what they should do)
- 122 activities across 12 practices
- Useful for benchmarking against industry peers

### Microsoft SDL
- 12 practices from training to response
- Mandatory for all Microsoft products since 2004
- SDL for Agile adapts practices to sprint cycles

---

## Automotive SSDLC (ISO/SAE 21434 Alignment)

The automotive V-model integrates security at each level:

```
Requirements ──────────────────────────────── Validation
     │                                              ▲
     ▼                                              │
  Architecture ────────────────────────── Integration Testing
     │                                              ▲
     ▼                                              │
  Detailed Design ──────────────── Component Testing
     │                                              ▲
     ▼                                              │
  Implementation ─── Unit Testing ──────────────────┘

Security activities map to EACH level:
- Requirements:   TARA, security goals, cybersecurity concept
- Architecture:   Secure design, HSM integration, network segmentation
- Detailed Design: Crypto protocols, access control, secure boot chain
- Implementation:  CERT C, MISRA, SAST, SCA
- Unit Testing:    Security unit tests, negative tests
- Integration:     Protocol fuzzing, interface testing
- Validation:      Penetration testing, attack simulation
```

### Cybersecurity Case (ISO/SAE 21434)
The work product that demonstrates adequate cybersecurity:
- Cybersecurity plan
- TARA results
- Cybersecurity goals and requirements
- Verification and validation evidence
- Residual risk assessment and acceptance

---

## SBOM (Software Bill of Materials)

### Why SBOM Matters
- Identifies all components (open-source, commercial, proprietary)
- Enables rapid response when new CVEs affect dependencies
- Required by regulations (US Executive Order 14028, UN R155)
- Supports supply chain security

### Formats
| Format | Standard Body | Use Case |
|--------|--------------|----------|
| **CycloneDX** | OWASP | Lightweight, security-focused |
| **SPDX** | Linux Foundation | Comprehensive, license-focused |
| **SWID** | ISO/IEC 19770-2 | Software identification tags |

### SBOM in CI/CD
```bash
# Generate CycloneDX SBOM from Python project
cyclonedx-py requirements requirements.txt -o sbom.json

# Generate from container image
syft alpine:latest -o cyclonedx-json > sbom.json

# Scan SBOM against vulnerability database
grype sbom:sbom.json
```

---

## Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Defect Density** | Security bugs per 1000 LOC | Trending down |
| **Mean Time to Fix** | Average time from discovery to patch | < 7 days (critical) |
| **Security Gate Pass Rate** | % of builds passing security gates | > 85% |
| **Vulnerability Escape Rate** | % of vulns found in production vs. earlier | < 10% |
| **SBOM Coverage** | % of products with current SBOM | 100% |
| **Training Coverage** | % of developers with security training | > 90% |
| **Threat Model Coverage** | % of components with current threat model | > 80% |

---

## References

- OWASP SAMM: https://owaspsamm.org/
- BSIMM: https://www.bsimm.com/
- Microsoft SDL: https://www.microsoft.com/en-us/securityengineering/sdl
- NIST SSDF (Secure Software Development Framework): https://csrc.nist.gov/Projects/ssdf
- ISO/SAE 21434: Road Vehicles — Cybersecurity Engineering
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- CycloneDX: https://cyclonedx.org/
