# Software-Defined Vehicle (SDV) Security

## What is an SDV?
A Software-Defined Vehicle decouples hardware from software, enabling vehicle features and behavior to be updated, added, or modified throughout the vehicle's lifetime via software updates.

## Architecture Shift

### Legacy vs SDV Architecture

| Aspect | Legacy | SDV |
|--------|--------|-----|
| ECU count | 70-150 ECUs | 3-5 HPCs + zone controllers |
| Software | Distributed, fixed | Centralized, updatable |
| Communication | CAN signal-based | Service-oriented (SOME/IP, DDS) |
| OS | AUTOSAR Classic / bare-metal | Linux, QNX, Hypervisor |
| Updates | Dealer visit | Continuous OTA |
| Features | Fixed at production | Dynamically activated |

### SDV Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Cloud Platform                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   OTA    │  │ Vehicle  │  │  Fleet   │  │  Feature │   │
│  │  Server  │  │ Digital  │  │  Security│  │  Store   │   │
│  │          │  │  Twin    │  │  SOC     │  │          │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼──────────────┼──────────────┼──────────────┼────────┘
        │              │              │              │
        └──────────────┴──────┬───────┴──────────────┘
                              │ (mTLS / Zero Trust)
                       ┌──────▼──────┐
                       │ Connectivity│
                       │ Gateway     │
                       │ (TCU + FW)  │
                       └──────┬──────┘
                              │
┌─────────────────────────────┼─────────────────────────────┐
│              Vehicle Compute Platform                       │
│  ┌───────────────────────────────────────────────────┐    │
│  │         High-Performance Computer (HPC)            │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────────────┐   │    │
│  │  │Hypervisor│  │ ADAS VM │  │ Infotainment VM │   │    │
│  │  │(Type 1)  │  │ (QNX)   │  │ (Linux/Android) │   │    │
│  │  │          │  │ ASIL-D  │  │ QM              │   │    │
│  │  └─────────┘  └─────────┘  └─────────────────┘   │    │
│  └───────────────────────────────────────────────────┘    │
│                              │                             │
│  ┌──────────┐  ┌──────────┐  │  ┌──────────┐             │
│  │Zone ECU  │  │Zone ECU  │  │  │Zone ECU  │             │
│  │(Front)   │  │(Rear)    │  │  │(Left)    │             │
│  │CAN/LIN   │  │CAN/LIN   │  │  │CAN/LIN   │             │
│  │actuators │  │sensors   │  │  │sensors   │             │
│  └──────────┘  └──────────┘  │  └──────────┘             │
└──────────────────────────────┴────────────────────────────┘
```

## New Attack Surfaces in SDV

| Attack Surface | Threat | Impact |
|---------------|--------|--------|
| App store / feature activation | Malicious app, license bypass | Vehicle control, revenue loss |
| Container orchestration | Container escape, privilege escalation | Cross-domain access |
| Hypervisor | VM escape from infotainment to ADAS | Safety compromise |
| API gateway | Authentication bypass, injection | Unauthorized vehicle access |
| Digital twin | Data poisoning, model manipulation | Incorrect fleet decisions |
| OTA pipeline | Supply chain attack, CI/CD compromise | Fleet-wide malware |
| Service mesh | Service impersonation | Data theft, command injection |

## SDV Security Controls

### 1. Hypervisor Security
```
┌─────────────────────────────────────────────┐
│          Hardware (SoC with TrustZone)       │
├─────────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐    │
│  │    Type-1 Hypervisor                 │    │
│  │  • Memory isolation (MMU/IOMMU)      │    │
│  │  • CPU partitioning                  │    │
│  │  • Device passthrough control        │    │
│  │  • Inter-VM communication policy     │    │
│  └─────────────────────────────────────┘    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Safety VM │  │  IVI VM  │  │ Network  │  │
│  │ (QNX/RTOS)│  │ (Linux)  │  │  VM      │  │
│  │ ASIL-D   │  │   QM     │  │(Gateway) │  │
│  │ No network│  │ Internet │  │ Firewall │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────┘
```

### 2. Container Security for Automotive
- **Image signing**: All container images signed (Notary/cosign)
- **Runtime policy**: No privileged containers, read-only rootfs
- **Network policy**: Strict pod-to-pod communication rules
- **Resource limits**: CPU/memory quotas prevent DoS
- **Vulnerability scanning**: Pre-deployment CVE check

### 3. Feature-on-Demand (FoD) Security
```
Threat: Customer bypasses payment to activate features
       (heated seats, performance boost, autonomous driving)

Controls:
1. License token signed by backend (ECDSA)
2. Token bound to VIN + ECU hardware ID
3. Expiry timestamp + monotonic counter
4. Verification in secure execution environment (TEE)
5. Periodic online re-validation
```

### 4. API Security (Vehicle SOA)
```
Service access control:

  Infotainment App → API Gateway → Policy Engine → Vehicle Service
                         │
                  Checks:
                  • App signed by OEM?
                  • Permission granted for this API?
                  • Rate limit OK?
                  • Safety state allows this action?
                  • User consent obtained?
```

## DevSecOps for Automotive

### CI/CD Security Pipeline
```
┌──────┐  ┌──────┐  ┌────────┐  ┌──────┐  ┌────────┐  ┌──────┐
│Source│→│Build │→│  SAST  │→│ DAST │→│  Sign  │→│Deploy │
│ Code │  │      │  │Coverity│  │Fuzzing│  │(HSM)  │  │ OTA  │
│      │  │      │  │CodeQL  │  │AFL++ │  │       │  │      │
└──────┘  └──────┘  └────────┘  └──────┘  └────────┘  └──────┘
    │         │          │          │          │          │
    │    SBOM gen    Vuln scan   Pen test  Integrity   Staged
    │    License     MISRA/CERT  API fuzz  Chain of    rollout
    │    check       compliance           trust       (canary)
```

### Security Testing Automation
- **SAST**: Coverity, CodeQL, Polyspace (MISRA compliance)
- **DAST**: AFL++, libFuzzer, Defensics (protocol fuzzing)
- **SCA**: Black Duck, Snyk (dependency vulnerabilities)
- **Container scanning**: Trivy, Grype
- **Infrastructure**: Terraform security scanning

## References
- AUTOSAR Adaptive Platform
- SOAFEE (Scalable Open Architecture for Embedded Edge)
- Eclipse SDV Working Group
- ISO/SAE 21434 applied to SDV
- COVESA (Connected Vehicle Systems Alliance)
