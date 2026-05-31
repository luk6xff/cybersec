# Zero Trust Architecture

## Core Principles

**"Never trust, always verify"** — Every access request is treated as if it originates from an untrusted network, regardless of location.

### Traditional (Perimeter) vs Zero Trust

| Aspect | Perimeter Security | Zero Trust |
|--------|-------------------|------------|
| Trust model | Trust inside, verify outside | Verify everything |
| Network | Flat internal network | Micro-segmented |
| Access | VPN = full access | Per-resource, per-session |
| Identity | Network location = identity | Strong identity + context |
| Monitoring | Perimeter logs | Continuous verification |

## NIST SP 800-207 Zero Trust Architecture

### Core Components
1. **Policy Engine (PE)** — Makes access decisions
2. **Policy Administrator (PA)** — Establishes/terminates connections
3. **Policy Enforcement Point (PEP)** — Enforces decisions at resource boundary

### Key Tenets
1. All data sources and computing services are considered resources
2. All communication is secured regardless of network location
3. Access to individual resources is granted on a per-session basis
4. Access is determined by dynamic policy (identity, device state, behavior)
5. Enterprise monitors and measures integrity/security posture of all assets
6. Authentication and authorization are dynamic and strictly enforced
7. Enterprise collects information about assets, network, communications

## Zero Trust in Automotive / V2X

### Vehicle-to-Cloud Zero Trust
```
┌──────────┐     ┌─────────────┐     ┌──────────────────┐
│  Vehicle  │────→│   PEP       │────→│  Backend Service │
│  (TCU)    │     │  (API GW)   │     │  (OTA/Telemetry) │
└──────────┘     └──────┬──────┘     └──────────────────┘
                        │
                  ┌─────┴──────┐
                  │   Policy    │
                  │   Engine    │
                  │             │
                  │ • Device ID │
                  │ • Cert valid│
                  │ • Geo-fence │
                  │ • Anomaly   │
                  └────────────┘
```

### Intra-Vehicle Zero Trust
Extending zero trust to internal vehicle networks:
- **ECU identity**: Each ECU authenticated via certificate/SecOC
- **Micro-segmentation**: Ethernet VLANs + firewall rules per domain
- **Least privilege**: ECU can only access services it needs
- **Continuous verification**: IDPS monitors for anomalous behavior
- **No implicit trust**: Gateway verifies every cross-domain message

## Implementation Patterns

### 1. Software-Defined Perimeter (SDP)
- Single Packet Authorization (SPA) before connection
- Services invisible to unauthorized scanners
- Used in vehicle-to-cloud connectivity

### 2. Mutual TLS (mTLS)
- Both client and server present certificates
- No anonymous connections
- Applicable to ECU-to-backend and ECU-to-ECU (Ethernet)

### 3. Service Mesh
- Sidecar proxy handles authN/authZ
- Transparent to application code
- Relevant for SOA (Service-Oriented Architecture) vehicles

## Automotive Application Matrix

| Use Case | Zero Trust Control |
|----------|-------------------|
| OTA updates | mTLS + device attestation + firmware version check |
| Diagnostics (UDS) | Certificate-based access (0x29) + session timeout |
| V2X messages | IEEE 1609.2 PKI + pseudonym rotation + misbehavior detection |
| Telematics | API gateway + OAuth 2.0 + geo-fencing + rate limiting |
| In-vehicle Ethernet | MACsec + VLAN isolation + IDPS |
| CAN bus | SecOC + message allowlisting + timing anomaly detection |
