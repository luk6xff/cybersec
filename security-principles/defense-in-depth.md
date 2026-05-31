# Defense in Depth

## Principle

No single security control is sufficient. Layer multiple, independent defensive mechanisms so that if one fails, others still protect the asset. Also known as **layered security** or **castle approach**.

---

## Layer Model

```
┌─────────────────────────────────────────────────────────────┐
│                      POLICIES & PROCEDURES                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                  PHYSICAL SECURITY                       │ │
│  │  ┌─────────────────────────────────────────────────────┐│ │
│  │  │                PERIMETER SECURITY                    ││ │
│  │  │  ┌─────────────────────────────────────────────────┐││ │
│  │  │  │              NETWORK SECURITY                   │││ │
│  │  │  │  ┌─────────────────────────────────────────────┐│││ │
│  │  │  │  │            HOST SECURITY                    ││││ │
│  │  │  │  │  ┌─────────────────────────────────────────┐││││ │
│  │  │  │  │  │         APPLICATION SECURITY            │││││ │
│  │  │  │  │  │  ┌─────────────────────────────────────┐│││││ │
│  │  │  │  │  │  │          DATA SECURITY              ││││││ │
│  │  │  │  │  │  └─────────────────────────────────────┘│││││ │
│  │  │  │  │  └─────────────────────────────────────────┘││││ │
│  │  │  │  └─────────────────────────────────────────────┘│││ │
│  │  │  └─────────────────────────────────────────────────┘││ │
│  │  └─────────────────────────────────────────────────────┘│ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Layers and Controls

### 1. Policies, Procedures & Awareness
| Control | Purpose |
|---------|---------|
| Security policies | Define acceptable behavior and standards |
| Security awareness training | Reduce human error and social engineering |
| Incident response plans | Ensure structured response to breaches |
| Background checks | Vet personnel before granting access |
| Acceptable use policies | Define boundaries for system usage |

### 2. Physical Security
| Control | Purpose |
|---------|---------|
| Facility access controls | Badge readers, biometrics, mantraps |
| Surveillance (CCTV) | Deter and record physical intrusion |
| Environmental controls | Fire suppression, UPS, HVAC monitoring |
| Hardware security | Tamper-evident seals, locked enclosures, cable locks |
| Secure disposal | Degaussing, shredding, certified destruction |

### 3. Perimeter Security
| Control | Purpose |
|---------|---------|
| Firewalls (network) | Filter traffic at network boundary |
| DMZ architecture | Isolate public-facing services |
| DDoS protection | Absorb volumetric attacks |
| Email gateway | Filter spam, phishing, malware |
| Web Application Firewall (WAF) | Protect web applications from OWASP Top 10 |
| VPN / Zero Trust Network Access | Secure remote access |

### 4. Network Security
| Control | Purpose |
|---------|---------|
| Network segmentation | Limit lateral movement |
| VLANs / micro-segmentation | Isolate workloads |
| IDS/IPS | Detect and block malicious traffic |
| Network Access Control (NAC) | Verify device before network access |
| DNS security (DNSSEC, DNS filtering) | Prevent DNS-based attacks |
| mTLS / IPsec | Encrypt internal communications |
| Network monitoring (NetFlow, PCAP) | Visibility into traffic patterns |

### 5. Host Security
| Control | Purpose |
|---------|---------|
| OS hardening (CIS Benchmarks) | Remove unnecessary services, secure configs |
| Endpoint Detection & Response (EDR) | Detect and respond to host-level threats |
| Host-based firewall | Restrict inbound/outbound per host |
| Patch management | Keep systems updated |
| Anti-malware | Detect known malicious software |
| Full disk encryption | Protect data if device is stolen |
| Secure boot | Verify firmware/OS integrity at startup |

### 6. Application Security
| Control | Purpose |
|---------|---------|
| Secure coding practices | Prevent vulnerabilities at source |
| Input validation | Block injection attacks |
| Authentication & authorization | Verify identity and enforce access control |
| Session management | Prevent session hijacking |
| API security | Rate limiting, auth, input validation |
| RASP (Runtime Application Self-Protection) | Detect attacks in running application |
| Code signing | Verify application integrity |

### 7. Data Security
| Control | Purpose |
|---------|---------|
| Encryption at rest | AES-256 for stored data |
| Encryption in transit | TLS 1.3 for network communications |
| Data Loss Prevention (DLP) | Prevent unauthorized exfiltration |
| Access controls (RBAC/ABAC) | Minimum necessary access to data |
| Backup and recovery | Protect against data loss/ransomware |
| Data masking/tokenization | Protect sensitive data in non-production |
| Key management (HSM) | Secure cryptographic key lifecycle |

---

## Security Control Categories

Controls are classified by their function:

| Category | Purpose | Examples |
|----------|---------|----------|
| **Preventive** | Stop attacks before they succeed | Firewall, access control, encryption, input validation |
| **Detective** | Identify attacks in progress or after | IDS, SIEM, log monitoring, integrity checking |
| **Corrective** | Fix damage after an incident | Backup restore, patch deployment, incident response |
| **Deterrent** | Discourage attack attempts | Warning banners, CCTV, legal notices |
| **Compensating** | Alternative when primary control isn't feasible | Network segmentation when patching isn't possible |
| **Recovery** | Restore normal operations | Disaster recovery, failover, backup restoration |

---

## Automotive Defense in Depth

```
┌─────────────────────────────────────────────────────────┐
│                 ORGANIZATIONAL LAYER                      │
│  ISO/SAE 21434 CSMS, Security policies, TARA            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │              EXTERNAL INTERFACE LAYER                 │ │
│  │  Firewall/Gateway, IDS, Certificate validation       │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │           NETWORK LAYER (In-Vehicle)            │ │ │
│  │  │  VLAN separation, SecOC, MACsec, CAN-FD auth   │ │ │
│  │  │  ┌─────────────────────────────────────────────┐│ │ │
│  │  │  │           ECU/HOST LAYER                    ││ │ │
│  │  │  │  Secure boot, TEE/HSM, runtime integrity   ││ │ │
│  │  │  │  ┌─────────────────────────────────────────┐││ │ │
│  │  │  │  │       APPLICATION/DATA LAYER           │││ │ │
│  │  │  │  │  Encrypted storage, access control,    │││ │ │
│  │  │  │  │  code signing, secure diagnostics      │││ │ │
│  │  │  │  └─────────────────────────────────────────┘││ │ │
│  │  │  └─────────────────────────────────────────────┘│ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Automotive Layer Details

| Layer | Controls |
|-------|----------|
| **Organizational** | CSMS (UN R155), security policies, supplier management, incident response |
| **External interfaces** | Vehicle gateway firewall, TLS/DTLS for telematics, V2X certificate validation |
| **In-vehicle network** | Domain separation, Ethernet switch ACLs, SecOC for CAN/CAN-FD, IDPS |
| **ECU** | Secure boot chain, HSM for crypto, memory protection (MPU/MMU), JTAG disabled |
| **Application/Data** | Code signing, encrypted calibration data, diagnostic authentication, key storage in HSM |

---

## Key Principles Supporting DiD

| Principle | Description |
|-----------|-------------|
| **Least Privilege** | Grant minimum access needed for the task |
| **Separation of Duties** | No single person/system controls entire process |
| **Fail Secure** | System defaults to secure state on failure |
| **Economy of Mechanism** | Keep security mechanisms simple (less attack surface) |
| **Complete Mediation** | Every access must be checked (no bypass) |
| **Open Design** | Security doesn't depend on secrecy of mechanism |
| **Defense of Choke Points** | Focus controls on narrow passages in data/access flow |
| **Diversity of Defense** | Use different vendor/technology at each layer |

---

## Common Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|--------------|
| Single firewall = "secure" | One layer, single point of failure |
| Trust internal network | Insider threats, lateral movement after breach |
| Security through obscurity | Discovery is when, not if |
| Encrypt everything, ignore access control | Authorized users can still abuse access |
| All eggs in one basket (single vendor) | Vendor vulnerability compromises all layers |
| Compliance checkbox security | Meets minimum, not real-world threats |

---

## Measuring Effectiveness

- **Red team exercises** — Test whether layered controls actually stop attacks
- **Purple team** — Collaborative testing between offense and defense
- **Breach simulation** — Automated tools (BAS) that emulate attack paths
- **Coverage mapping** — Map controls to MITRE ATT&CK techniques
- **Gap analysis** — Identify layers with insufficient controls

---

## References

- NIST SP 800-53: Security and Privacy Controls
- CIS Controls v8: https://www.cisecurity.org/controls
- MITRE ATT&CK: https://attack.mitre.org/
- ISO 27001/27002: Information Security Controls
- Saltzer & Schroeder: Protection of Information in Computer Systems (1975)
