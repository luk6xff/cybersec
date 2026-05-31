# Zero Trust Architecture

## Core Principle

**"Never trust, always verify"** — No entity (user, device, application, network flow) is inherently trusted regardless of network location.

Traditional security: Castle-and-moat (trust everything inside the perimeter)
Zero Trust: Every access request is fully authenticated, authorized, and encrypted regardless of origin.

---

## Zero Trust Tenets (NIST SP 800-207)

1. **All data sources and computing services are considered resources**
2. **All communication is secured regardless of network location** — Internal traffic is not inherently more trustworthy
3. **Access to individual resources is granted on a per-session basis** — Trust is not blanket or persistent
4. **Access is determined by dynamic policy** — Behavioral, environmental, and contextual attributes
5. **The enterprise monitors and measures integrity/security of all assets** — No device is inherently trusted
6. **Authentication and authorization are strictly enforced before access** — Dynamic, continuous
7. **The enterprise collects maximum information for security improvement** — Telemetry-driven decisions

---

## Architecture Components

```
┌──────────────────────────────────────────────────────────────────┐
│                         CONTROL PLANE                              │
│  ┌─────────────┐   ┌─────────────────┐   ┌──────────────────┐   │
│  │   Policy     │   │  Policy Engine   │   │ Trust Algorithm  │   │
│  │   Admin      │   │  (Decision Point)│   │  (Risk Scoring)  │   │
│  │   Point      │   │                  │   │                  │   │
│  └─────────────┘   └────────┬─────────┘   └──────────────────┘   │
│                              │                                     │
└──────────────────────────────┼─────────────────────────────────────┘
                               │ Allow/Deny
┌──────────────────────────────┼─────────────────────────────────────┐
│                         DATA PLANE                                  │
│                              ▼                                      │
│  ┌──────────┐    ┌────────────────┐    ┌────────────────────────┐ │
│  │  Subject │───→│ Policy Enforce- │───→│      Resource          │ │
│  │  (User/  │    │ ment Point (PEP)│    │  (App/Data/Service)    │ │
│  │  Device) │    │                 │    │                        │ │
│  └──────────┘    └────────────────┘    └────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Role |
|-----------|------|
| **Policy Engine (PE)** | Makes access decisions based on policy and trust algorithm |
| **Policy Administrator (PA)** | Establishes/shuts down communication paths via PEP |
| **Policy Enforcement Point (PEP)** | Enables, monitors, and terminates connections |
| **Trust Algorithm** | Computes risk score from multiple inputs |

### Trust Algorithm Inputs
- User identity and authentication strength (MFA, biometrics)
- Device health (patched, compliant, managed, cert valid)
- Request context (time, location, network, behavior patterns)
- Resource sensitivity classification
- Threat intelligence feeds
- Historical access patterns

---

## Five Pillars of Zero Trust

| Pillar | Description | Implementation |
|--------|-------------|----------------|
| **Identity** | Verify every user/service identity | MFA, SSO, certificate-based auth, passwordless |
| **Device** | Validate device health and compliance | EDR, device certificates, posture assessment |
| **Network** | Micro-segment and encrypt all traffic | Micro-segmentation, mTLS, encrypted overlay networks |
| **Application** | Secure app access and runtime | API gateway, RBAC/ABAC, runtime protection |
| **Data** | Classify and protect data everywhere | Encryption at rest/transit, DLP, rights management |

---

## Implementation Approaches

### Micro-Segmentation
Divide the network into small, isolated zones:
```
Traditional:  [Internet] → [Firewall] → [Flat Internal Network — everything talks to everything]

Zero Trust:   [Internet] → [PEP] → [Segment A]
                                  → [Segment B]   (A cannot talk to B without explicit policy)
                                  → [Segment C]
```

Each workload/service has its own segment with explicit allow-list policies.

### Software-Defined Perimeter (SDP)
- Resources are invisible until authenticated and authorized
- "Dark cloud" — no exposed ports, no DNS records for attackers to find
- Connection only established after verification

### Identity-Centric Access
```
User → Authenticate (MFA) → Identity Provider → Policy Engine evaluates:
  - User role/group
  - Device compliance
  - Location/time risk
  - Resource sensitivity
  - Behavior baseline
→ Grant access with minimum privilege, time-limited session
→ Continuously re-evaluate during session
```

---

## Zero Trust for Automotive / IoT

Traditional vehicle networks assumed physical isolation = trust. Modern connected vehicles break this assumption.

### Applying ZT to Vehicle Architecture

| Vehicle Domain | Zero Trust Application |
|---------------|----------------------|
| **In-vehicle network** | Authenticate every ECU message (SecOC/MACsec), no implicit bus trust |
| **V2X communication** | Verify every external message (PKI-based, certificate validation) |
| **OTA updates** | Mutual authentication, signed packages, rollback protection |
| **Diagnostics** | Session-based auth (ISO 14229 security access), per-service authorization |
| **Telematics/Cloud** | mTLS, device certificates, short-lived tokens, API gateway |
| **User access** | Multi-factor for companion apps, role-based vehicle functions |

### Automotive ZT Principles
1. Every ECU authenticates messages it sends (SecOC with freshness)
2. No ECU trusts another ECU's messages without verification
3. External interfaces (OBD-II, Wi-Fi, Bluetooth, cellular) are untrusted zones
4. Cloud-to-vehicle communication requires mutual authentication
5. Diagnostic access requires proof of authorization (certificates, challenge-response)
6. Firmware updates are cryptographically verified before installation

---

## Comparison: Perimeter vs Zero Trust

| Aspect | Perimeter Security | Zero Trust |
|--------|-------------------|------------|
| Trust model | Trust inside, verify outside | Verify everything, trust nothing |
| Lateral movement | Easy once inside | Contained by micro-segmentation |
| Remote access | VPN (full network access) | Per-application access only |
| Insider threats | Poorly addressed | Treated same as external threats |
| Breach impact | Full network compromise | Limited blast radius |
| Visibility | Edge-focused | Full internal visibility |

---

## Implementation Roadmap

```
Phase 1: Foundation (Months 1-3)
├── Asset inventory (users, devices, apps, data)
├── Identity consolidation (single IdP, MFA enforcement)
├── Network visibility (flow logging, traffic analysis)
└── Data classification

Phase 2: Core Controls (Months 4-8)
├── Micro-segmentation of critical assets
├── Device compliance enforcement
├── Least-privilege access policies
├── Encrypted internal communications (mTLS)
└── API gateway for application access

Phase 3: Advanced (Months 9-12+)
├── Continuous adaptive trust scoring
├── Behavioral analytics (UEBA)
├── Automated policy enforcement
├── Software-defined perimeter
└── Full telemetry-driven security operations
```

---

## Challenges

- **Legacy systems** — May not support modern authentication or encryption
- **Complexity** — Requires comprehensive inventory and policy management
- **Performance** — Additional authentication/encryption overhead
- **Culture** — Shifts responsibility from network team to all engineers
- **IoT/OT** — Resource-constrained devices may not support full ZT stack

---

## References

- NIST SP 800-207: Zero Trust Architecture
- CISA Zero Trust Maturity Model: https://www.cisa.gov/zero-trust-maturity-model
- DoD Zero Trust Reference Architecture
- Forrester: Zero Trust eXtended (ZTX) Framework
- Google BeyondCorp: https://cloud.google.com/beyondcorp
