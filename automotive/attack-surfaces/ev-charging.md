# EV Charging Security

## Overview

Electric Vehicle (EV) charging infrastructure introduces a complex attack surface spanning power electronics, communications protocols, cloud backends, and billing systems.

```
┌──────────┐     PLC / Wi-Fi / LTE     ┌──────────────┐     TLS/REST     ┌───────────┐
│  Vehicle │ ←──────────────────────→  │  Charger     │ ←──────────────→ │  Backend  │
│  (EV)    │    ISO 15118 / CHAdeMO    │  (EVSE)      │    OCPP 1.6/2.0 │  (CSMS)   │
└──────────┘                            └──────────────┘                   └───────────┘
     │                                        │                                  │
     │ Contract cert (Plug&Charge)            │ EVSE cert                        │ Root CA
     │ Session keys (TLS)                     │ Firmware signed                  │ Billing
     │ Charging profile                       │ Local auth (RFID)               │ Roaming
```

## ISO 15118 (Plug & Charge)

### Protocol Stack
```
Application Layer   → Service Discovery, Charging Parameters, Payment
                      V2G Messages (EXI encoded XML)
Session Layer       → V2GTP (V2G Transfer Protocol, TCP port 15118)
Transport Layer     → TLS 1.2/1.3 (mutual authentication)
Network Layer       → IPv6 (link-local, SLAAC)
Data Link Layer     → HomePlug Green PHY (PLC) / Wi-Fi (15118-20)
Physical Layer      → Control Pilot (CP) line / Power Line
```

### ISO 15118-2 vs 15118-20

| Feature | ISO 15118-2 | ISO 15118-20 |
|---------|-------------|--------------|
| Encoding | EXI (XML) | EXI (XML) |
| Transport | TCP/TLS | TCP/TLS 1.3 |
| Auth | Contract cert (X.509) | Contract cert + ACDP |
| Charging | AC, DC | AC, DC, WPT (wireless), ACDP, BPT |
| PKI | Full chain validation | Full chain + OCSP stapling |
| Communication | PLC only | PLC + Wi-Fi + LTE |
| Bidirectional | Not supported | V2G/V2H supported |

### Plug & Charge (PnC) Authentication Flow
```
1. EV connects CP → EVSE signals availability
2. SLAC (Signal Level Attenuation Characterization) on PLC
3. IPv6 link-local established
4. SDP (SECC Discovery Protocol) → Find EVSE services
5. TLS 1.2 handshake:
   - EVSE presents EVSE cert (server auth)
   - EV presents Contract cert (client auth — Plug&Charge!)
   - Mutual TLS established
6. V2G session: ServiceDiscovery → ChargeParameterDiscovery →
   PaymentDetails → Authorization → PowerDelivery → Charging
7. Session ends: MeteringReceipt → SessionStop
```

### PKI Structure (VDE PKI / Hubject)
```
V2G Root CA
├── Sub-CA 1 (OEM) → Provisioning Certificates (EV identity)
├── Sub-CA 2 (MO)  → Contract Certificates (payment identity)
├── Sub-CA 3 (CPO) → EVSE Certificates (charger identity)
└── CPS Server      → Certificate Provisioning Service

Key relationships:
- OEM Root → issues Provisioning Cert → installed at manufacturing
- Mobility Operator → issues Contract Cert → installed OTA via CPS
- Charge Point Operator → issues EVSE Leaf Cert → in each charger
```

## OCPP (Open Charge Point Protocol)

### OCPP Versions & Security
| Version | Transport | Security |
|---------|-----------|----------|
| 1.5 | SOAP/HTTP | None (cleartext!) |
| 1.6-J | WebSocket/JSON | TLS optional (often missing) |
| 2.0.1 | WebSocket/JSON | TLS mandatory, client certs |

### OCPP 2.0.1 Security Profiles
```
Profile 1: Unsecured (HTTP/WS) — NOT recommended
Profile 2: TLS with Basic Auth (server cert + password)
Profile 3: TLS with Client Certificates (mutual TLS — preferred)
```

### Common OCPP Vulnerabilities
| Vulnerability | Impact | Example |
|--------------|--------|---------|
| No TLS (OCPP 1.6) | MitM, credential theft | Intercept ChargePointId + password |
| Weak authentication | Unauthorized charging | Default/shared passwords |
| Missing authorization on messages | Free charging, DoS | Send RemoteStartTransaction |
| Firmware update over HTTP | Malicious firmware | MitM FirmwareUpdate message |
| Missing message integrity | Transaction manipulation | Modify MeterValues, billing fraud |
| Information disclosure | Privacy breach | Expose RFID UIDs, vehicle IDs |

## Attack Vectors

### 1. PLC (Power Line Communication) Attacks
```bash
# HomePlug Green PHY operates on pilot line
# Attacker can inject/sniff via charging cable or nearby outlet

# SLAC manipulation → MitM between EV and EVSE
# Tools: QCA7000-based adapters, open-plc-utils

# Attack: ARP spoofing on PLC network
# Impact: Intercept V2GTP messages, steal session data

# Attack: Rogue EVSE
# Emulate charger → harvest contract certificates from EVs
```

### 2. TLS Downgrade/Bypass
```
- Missing certificate validation (accept any cert)
- Self-signed certificates accepted
- Expired certificates not checked
- Missing CRL/OCSP checks
- TLS 1.0/1.1 supported (POODLE, BEAST)
- Weak cipher suites (RC4, DES)
```

### 3. Billing Fraud
```
- Modify MeterValues in transit (OCPP without integrity)
- Clone RFID cards (Mifare Classic — broken crypto)
- Replay valid authorization tokens
- Exploit free-vend mode on misconfigured chargers
- Session hijacking (start/stop another user's session)
```

### 4. Charger Compromise
```
- Default credentials on management interface
- Exposed debug ports (UART, JTAG) on charger controller
- Vulnerable web interface (SQLi, RCE)
- Unsigned firmware updates
- Physical access to internal network
- Supply chain attack on charger components
```

### 5. Grid Attacks (via compromised chargers)
```
- Coordinated load manipulation → frequency instability
- Demand-side attack: simultaneously switch all chargers ON/OFF
- V2G abuse: drain vehicle batteries, inject dirty power
- DDoS on grid management systems via OCPP backend
```

## Security Requirements

### For EVSE (Chargers)
- [ ] TLS 1.2+ with mutual authentication (OCPP Security Profile 3)
- [ ] Signed and verified firmware updates
- [ ] Secure boot chain on charger controller
- [ ] RFID card encryption (DESFire EV2/EV3, not Mifare Classic)
- [ ] Rate limiting on authentication attempts
- [ ] Physical tamper detection and lockout
- [ ] Isolated network zones (payment vs. management vs. grid)
- [ ] Event logging with integrity protection (send to SIEM)

### For EV (Vehicle Side)
- [ ] Validate EVSE certificate chain (don't accept self-signed)
- [ ] Protect Contract Certificate private key in HSM/TPM
- [ ] Support certificate revocation checking
- [ ] Secure storage of charging history/billing data
- [ ] Prevent extraction of Provisioning Certificate

### For Backend (CSMS)
- [ ] Enforce OCPP 2.0.1 Security Profile 3
- [ ] Monitor for anomalous charging patterns
- [ ] Implement charger certificate lifecycle management
- [ ] Secure CPS (Certificate Provisioning Service) endpoints
- [ ] Billing system integrity validation

## Standards & Regulations

| Standard | Scope |
|----------|-------|
| ISO 15118 (-2, -20) | V2G communication, Plug&Charge |
| IEC 61851 | EV charging equipment safety |
| OCPP 2.0.1 | Charger-to-backend communication |
| ISO 27001 | Information security for charging operators |
| NIST 800-82 | ICS security (grid-connected chargers) |
| EN 303 645 | IoT security baseline (consumer chargers) |
| UNECE R155 | Cybersecurity for vehicles (includes charging) |

## Tools & References

### Code
- [EcoG - ISO 15118 Implementation](https://github.com/EcoG-io/iso15118)
- [SwitchEV - ISO 15118 (Josev)](https://github.com/SwitchEV/iso15118)
- [open-plc-utils](https://github.com/qca/open-plc-utils) — HomePlug Green PHY tools
- [V2GInjector](https://github.com/FlUxIuS/V2Gdecoder) — V2G traffic analysis

### Talks & Research
- [Hacking EV Charging Stations Via The Charging Cable](https://www.youtube.com/watch?v=JoviRCoRN6c) - [Slides](https://elaad.nl/en/hacking-ev-charging-stations-via-the-charging-cable/)
- [Plug&Charge Security Analysis (2023)](https://www.usenix.org/conference/usenixsecurity23) — PKI implementation flaws
- [ENCS - Security testing EV charging infrastructure](https://encs.eu/)
- [Sandia National Labs - EV Charging Cybersecurity](https://www.sandia.gov/)
