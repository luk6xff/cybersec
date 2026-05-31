# CIA Triad & Security Properties

## The CIA Triad

The three fundamental properties of information security:

| Property | Definition | Threat | Control Examples |
|----------|-----------|--------|-----------------|
| **Confidentiality** | Only authorized entities can access data | Unauthorized disclosure, data breach | Encryption, access control, data classification |
| **Integrity** | Data cannot be altered without detection | Tampering, corruption, unauthorized modification | Hashing, digital signatures, checksums, version control |
| **Availability** | Systems and data are accessible when needed | DoS, hardware failure, ransomware | Redundancy, backups, DDoS protection, failover |

```
              Confidentiality
                   /\
                  /  \
                 /    \
                / CIA  \
               /  Triad \
              /──────────\
             /            \
            /              \
     Integrity ────────── Availability
```

---

## Extended Security Properties

### DAD Triad (Opposite/Threat Model)
| CIA Property | Threat (DAD) | Attack Example |
|-------------|-------------|----------------|
| Confidentiality | **Disclosure** | Data breach, sniffing, side-channel |
| Integrity | **Alteration** | MITM, SQL injection, firmware tampering |
| Availability | **Destruction/Denial** | DDoS, ransomware, hardware destruction |

### Additional Properties

| Property | Definition | Importance |
|----------|-----------|------------|
| **Authenticity** | Verify the claimed identity of entities/data | Prevents impersonation and forgery |
| **Non-repudiation** | Entity cannot deny having performed an action | Critical for legal, financial, audit |
| **Accountability** | Actions can be traced to responsible entity | Supports forensics and compliance |
| **Reliability** | System performs consistently as intended | Operational safety (automotive, medical) |

---

## Parkerian Hexad

Six security elements (Donn Parker, 1998):

| Element | Description | Beyond CIA? |
|---------|-------------|-------------|
| **Confidentiality** | Protection from unauthorized disclosure | CIA core |
| **Integrity** | Data is unaltered and accurate | CIA core |
| **Availability** | Accessible when needed | CIA core |
| **Possession/Control** | Physical control of data medium | Data on stolen USB (still encrypted) but you lost possession |
| **Authenticity** | Data is genuine and from claimed source | Forged document with valid content |
| **Utility** | Data is in usable form | Encrypted data without the key — available but not useful |

---

## Security Models

### Bell-LaPadula Model (Confidentiality)
Military/government classification model:
- **Simple Security Rule** (no read up): A subject cannot read data at a higher classification
- **Star Property** (no write down): A subject cannot write data to a lower classification
- Prevents information leaking from high to low classification

```
TOP SECRET  ──────── Can read TS, write TS
    ↑ no read up
SECRET      ──────── Can read S, write S or TS
    ↑ no read up         ↓ no write down blocked
CONFIDENTIAL ─────── Can read C, write C or above
    ↑ no read up
UNCLASSIFIED ─────── Can only read/write U
```

### Biba Model (Integrity)
Opposite of Bell-LaPadula — protects integrity:
- **Simple Integrity Rule** (no read down): Don't read lower-integrity data
- **Star Integrity Rule** (no write up): Don't write to higher-integrity level
- Prevents corruption flowing from low-integrity to high-integrity

### Clark-Wilson Model (Integrity, Commercial)
- **Constrained Data Items (CDIs)**: Data requiring integrity protection
- **Unconstrained Data Items (UDIs)**: Input data not yet validated
- **Transformation Procedures (TPs)**: Only authorized programs can modify CDIs
- **Integrity Verification Procedures (IVPs)**: Verify CDI consistency
- Enforces well-formed transactions and separation of duties

### Brewer-Nash Model (Chinese Wall)
- Prevents conflicts of interest in consulting/advisory contexts
- Once you access data from Company A, you cannot access competitor Company B's data
- Dynamic access control based on access history

---

## Applying CIA to Different Domains

### CIA in Automotive Cybersecurity

| Component | Confidentiality | Integrity | Availability |
|-----------|----------------|-----------|--------------|
| **ECU firmware** | Prevent reverse engineering (IP) | Critical — tampered firmware = safety risk | Must boot and function reliably |
| **CAN bus messages** | Some (battery SOC, user data) | **HIGHEST** — forged messages = safety | Bus must not be DoS'd |
| **OTA updates** | Protect pre-release firmware | **HIGHEST** — ensure authentic update | Update service must be accessible |
| **Diagnostic data** | PII (driver behavior) | Important for accurate diagnostics | Required for maintenance |
| **V2X messages** | Low (broadcast by design) | **HIGHEST** — false road hazard = accidents | Time-critical availability |
| **Cryptographic keys** | **HIGHEST** — compromise = full breach | Keys must not be corrupted | Keys must be available for boot/communication |

**Key insight for automotive:** Integrity and Availability often outweigh Confidentiality due to safety implications (ISO 26262).

### CIA in Cloud Services

| Scenario | Priority |
|----------|----------|
| Healthcare records | C > I > A (privacy-first) |
| Financial transactions | I > A > C (accurate and available) |
| Safety-critical systems | A > I > C (must be available, then correct) |
| Military/intelligence | C > I > A (protect secrets) |
| E-commerce | A > I > C (uptime drives revenue) |

---

## Implementation Patterns

### Confidentiality Controls
```
Data at rest  → AES-256 encryption, full disk encryption
Data in transit → TLS 1.3, IPsec, WireGuard
Data in use   → Secure enclaves (TEE), homomorphic encryption
Access        → RBAC/ABAC, MFA, least privilege
Classification → Label data, apply handling rules per level
```

### Integrity Controls
```
Data integrity     → SHA-256/SHA-3 hashes, HMAC
Message integrity  → Digital signatures (Ed25519, ECDSA)
System integrity   → Secure boot, code signing, TPM/HSM attestation
File integrity     → AIDE, Tripwire, dm-verity
Database integrity → Constraints, triggers, audit trails
Supply chain       → SBOM, reproducible builds, signed artifacts
```

### Availability Controls
```
Hardware      → Redundancy (RAID, dual power, N+1), geographic distribution
Network       → Load balancing, CDN, DDoS mitigation, redundant paths
Application   → Auto-scaling, health checks, circuit breakers, graceful degradation
Data          → Backups (3-2-1 rule), replication, point-in-time recovery
Process       → Disaster recovery plans, RTO/RPO targets, failover testing
```

---

## Key Metrics

| Property | Metric | Example Target |
|----------|--------|---------------|
| Confidentiality | Data breach incidents | 0 per year |
| Confidentiality | Unauthorized access attempts blocked | > 99.9% |
| Integrity | Data corruption events detected | 0 undetected |
| Integrity | File integrity monitoring alerts investigated | 100% within 1 hour |
| Availability | Uptime (SLA) | 99.99% (52 min downtime/year) |
| Availability | RTO (Recovery Time Objective) | < 4 hours |
| Availability | RPO (Recovery Point Objective) | < 1 hour |

---

## References

- NIST SP 800-33: Underlying Technical Models for IT Security
- ISO 27001: Information Security Management (CIA as foundation)
- Bell & LaPadula (1973): Secure Computer Systems: Mathematical Foundations
- Biba (1977): Integrity Considerations for Secure Computer Systems
- Clark & Wilson (1987): A Comparison of Commercial and Military Security Policies
- Parkerian Hexad: Donn Parker, "Fighting Computer Crime" (1998)
