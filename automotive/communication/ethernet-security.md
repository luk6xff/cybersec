# Automotive Ethernet Security

## Overview
Modern vehicles are transitioning from CAN-dominated networks to Ethernet-based architectures (particularly for ADAS, infotainment, and backbone communication). This introduces both IP-based threats and IP-based security solutions.

## Automotive Ethernet Standards

| Standard | Speed | Use Case |
|----------|-------|----------|
| 100BASE-T1 (BroadR-Reach) | 100 Mbps | Legacy sensors, body domain |
| 1000BASE-T1 | 1 Gbps | ADAS cameras, backbone |
| 2.5/5/10GBASE-T1 | 2.5-10 Gbps | Zonal architecture, compute |
| TSN (802.1) | Various | Time-critical control messages |

## Network Architecture

### Traditional (Domain-based)
```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│Powertrain│   │  ADAS   │   │  Body   │   │  Infot. │
│ Domain   │   │ Domain  │   │ Domain  │   │ Domain  │
│Controller│   │Controller│   │Controller│   │  HU    │
└────┬─────┘   └────┬────┘   └────┬────┘   └────┬────┘
     │              │              │              │
     └──────────────┴──────┬───────┴──────────────┘
                           │
                    ┌──────┴──────┐
                    │  Central    │
                    │  Gateway    │
                    │  (Firewall) │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │    TCU      │
                    │ (Telematics)│
                    └─────────────┘
```

### Modern (Zonal / SOA)
```
┌──────────────────────────────────────────────────┐
│              Ethernet Backbone (TSN)               │
├──────────┬───────────┬───────────┬───────────────┤
│ Zone ECU │  Zone ECU │  Zone ECU │  Central      │
│  Front   │   Rear    │   Left    │  Compute      │
│          │           │           │  (HPC)        │
│ CAN/LIN  │  CAN/LIN  │  CAN/LIN  │  ADAS/Info   │
│ sensors  │  sensors  │  sensors  │  + Gateway    │
└──────────┴───────────┴───────────┴───────────────┘
```

## Security Controls

### Layer 2: MACsec (IEEE 802.1AE)

MACsec provides hop-by-hop encryption and integrity at the Ethernet frame level.

```
┌──────────────────────────────────────────────────────────┐
│                  MACsec Frame Format                       │
├────────┬──────────┬────────────────┬────────┬────────────┤
│ DA/SA  │ SecTAG   │   Payload      │  ICV   │    FCS     │
│(12B)   │(8-16B)   │(encrypted data)│ (16B)  │   (4B)     │
│        │PN+SCI   │                │ AES-GCM│            │
└────────┴──────────┴────────────────┴────────┴────────────┘
```

| Property | Value |
|----------|-------|
| Algorithm | AES-128-GCM or AES-256-GCM |
| Integrity | GCM authentication tag (ICV) |
| Replay protection | Packet Number (PN) in SecTAG |
| Key management | MKA protocol (802.1X-2020) |
| Latency overhead | ~1-5 μs (hardware offload) |

**Automotive considerations**:
- Point-to-point only (not broadcast like CAN)
- Requires MACsec-capable PHYs/switches
- Key distribution via 802.1X or pre-shared CAK

### Layer 3: IPsec

| Mode | Protection | Use Case |
|------|-----------|----------|
| Transport | Payload only | ECU-to-ECU within vehicle |
| Tunnel | Full IP packet | Vehicle-to-cloud VPN |

### Layer 4: TLS/DTLS

| Protocol | Transport | Use Case |
|----------|-----------|----------|
| TLS 1.3 | TCP | OTA updates, diagnostics |
| DTLS 1.3 | UDP | SOME/IP-SD, real-time services |

### Application: SOME/IP Security

SOME/IP (Scalable service-Oriented MiddlewarE over IP) is the automotive service discovery and RPC protocol.

Security additions:
- **SOME/IP-TP with DTLS**: Encrypt service communication
- **Service authentication**: Only authorized ECUs can subscribe
- **Access control lists**: Per-service, per-client authorization

## Firewall and IDPS on Ethernet

### Automotive Ethernet Firewall Rules

```
┌──────────────────────────────────────────────┐
│            Ethernet Switch / Gateway          │
├──────────────────────────────────────────────┤
│  Rule 1: ADAS_Zone → Infotainment: DENY     │
│  Rule 2: TCU → ADAS_Zone: DENY              │
│  Rule 3: Infotainment → TCU: rate_limit(1M) │
│  Rule 4: OBD_Port → All: DENY (except diag) │
│  Rule 5: Any → Central_Compute: mTLS only   │
│  Rule 6: Default: LOG + DENY                │
└──────────────────────────────────────────────┘
```

### Deep Packet Inspection (DPI) for Automotive Protocols
- SOME/IP message ID validation
- DoIP (Diagnostics over IP) session monitoring
- UDS payload anomaly detection over Ethernet
- ARP spoofing detection

## VLAN Segmentation

| VLAN | Domain | Security Level |
|------|--------|---------------|
| 10 | ADAS/Safety | Highest — isolated, MACsec |
| 20 | Powertrain | High — critical CAN-ETH bridge |
| 30 | Body/Comfort | Medium |
| 40 | Infotainment | Low — internet-facing |
| 50 | Diagnostics | Restricted — only during service |
| 99 | Management | Switch config, IDPS reporting |

## Time-Sensitive Networking (TSN) Security

TSN (IEEE 802.1 family) provides deterministic real-time guarantees. Security concerns:

| TSN Feature | Security Concern | Mitigation |
|-------------|-----------------|------------|
| 802.1Qbv (Time-Aware Shaper) | Schedule manipulation → DoS | Authenticated config |
| 802.1CB (Frame Replication) | Replay through redundant paths | MACsec on all paths |
| 802.1AS (Time Sync / gPTP) | Time spoofing → schedule disruption | 802.1AS-Rev authentication |
| 802.1Qci (Per-Stream Filtering) | Bypass filtering rules | Defense in depth |

## Attack Vectors

| Attack | Vector | Impact | Detection |
|--------|--------|--------|-----------|
| ARP spoofing | Ethernet LAN | MITM, traffic redirection | Static ARP, IDPS |
| VLAN hopping | 802.1Q double-tagging | Cross-domain access | Trunk port security |
| DoS flooding | High-rate traffic | ECU resource exhaustion | Rate limiting, QoS |
| SOME/IP injection | Forge service messages | False sensor data | Service authentication |
| DoIP exploitation | Diagnostic protocol abuse | Unauthorized access | Session monitoring |
| TSN time attack | Manipulate gPTP | Desynchronize safety | Authenticated sync |

## References
- IEEE 802.1AE (MACsec)
- IEEE 802.1X-2020 (Port-Based Network Access Control)
- AUTOSAR Ethernet Security
- OPEN Alliance TC8 (Automotive Ethernet)
- IEEE 802.1 TSN Task Group
