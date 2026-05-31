# Automotive Cybersecurity — Reference Index

## Structure

```
automotive/
├── INDEX.md                                         — This file (navigation guide)
│
├── standards/                                       — FOUNDATIONS & COMPLIANCE
│   ├── automotive-cybersecurity.md                  — Standards overview (R155, 21434, ASPICE, TISAX)
│   ├── compliance-standards.md                      — R155 CSMS, 21434 lifecycle, R156, TISAX, supply chain
│   └── threat-modeling.md                           — TARA, STRIDE, PASTA, attack trees, feasibility ratings
│
├── communication/                                   — PROTOCOL & BUS SECURITY
│   ├── can-bus-security.md                          — CAN 2.0/FD attacks, SecOC on CAN, timing detection
│   ├── ethernet-security.md                         — MACsec, IPsec, SOME/IP, VLAN, DoIP, TSN security
│   ├── autosar-security.md                          — SecOC deep dive, CSM, KeyM, IdsM, freshness managers
│   └── v2x-security.md                             — IEEE 1609.2, SCMS PKI, pseudonym privacy, misbehavior
│
├── mechanisms/                                      — SECURITY MECHANISMS
│   ├── automotive-pki-key-management.md             — Vehicle PKI, HSM key storage, fleet diversification
│   ├── ota-security.md                              — Signing, anti-rollback, A/B update, Uptane, R156
│   ├── secure-diagnostics.md                        — UDS 0x27/0x29, DoIP, OBD-II hardening, role-based access
│   └── idps.md                                      — CAN/Ethernet IDS, ML detection, AUTOSAR IdsM, VSOC
│
├── attack-surfaces/                                 — ATTACK VECTORS & PENTESTING
│   ├── wireless-interfaces.md                       — Bluetooth, BLE, UWB, NFC, key fob relay, TPMS, Wi-Fi
│   ├── ev-charging.md                               — ISO 15118, OCPP, PLC attacks, billing fraud, grid threats
│   └── automotive-pentesting.md                     — Full attack methodology, tools, UDS exploitation, reporting
│
├── architecture/                                    — SYSTEM DESIGN & SAFETY
│   ├── sdv-security.md                              — Software-Defined Vehicle, hypervisor, containers, DevSecOps
│   └── functional-safety-security.md                — ISO 26262 + 21434 co-engineering, ASIL, safe states, timing
│
└── ../media/                                        — Diagrams referenced by documents
```

## Quick Navigation by Topic

### "I need to understand..."

| Topic | Start Here | Then Read |
|-------|-----------|-----------|
| R155 compliance | [compliance-standards.md](standards/compliance-standards.md) | [threat-modeling.md](standards/threat-modeling.md) |
| How SecOC works | [autosar-security.md](communication/autosar-security.md) | [can-bus-security.md](communication/can-bus-security.md) |
| Key management | [automotive-pki-key-management.md](mechanisms/automotive-pki-key-management.md) | [ota-security.md](mechanisms/ota-security.md) |
| Pentest a vehicle | [automotive-pentesting.md](attack-surfaces/automotive-pentesting.md) | [secure-diagnostics.md](mechanisms/secure-diagnostics.md) |
| OTA update security | [ota-security.md](mechanisms/ota-security.md) | [automotive-pki-key-management.md](mechanisms/automotive-pki-key-management.md) |
| EV charging threats | [ev-charging.md](attack-surfaces/ev-charging.md) | [compliance-standards.md](standards/compliance-standards.md) |
| Relay attacks (key fob) | [wireless-interfaces.md](attack-surfaces/wireless-interfaces.md) | [threat-modeling.md](standards/threat-modeling.md) |
| Safety vs security | [functional-safety-security.md](architecture/functional-safety-security.md) | [autosar-security.md](communication/autosar-security.md) |
| SDV / zonal arch | [sdv-security.md](architecture/sdv-security.md) | [ethernet-security.md](communication/ethernet-security.md) |
| Intrusion detection | [idps.md](mechanisms/idps.md) | [autosar-security.md](communication/autosar-security.md) |
| V2X / C-V2X | [v2x-security.md](communication/v2x-security.md) | [wireless-interfaces.md](attack-surfaces/wireless-interfaces.md) |
| Threat modeling | [threat-modeling.md](standards/threat-modeling.md) | [compliance-standards.md](standards/compliance-standards.md) |

### "I'm designing security for..."

| System | Key Files | Critical Requirements |
|--------|-----------|----------------------|
| Gateway ECU | communication/autosar-security, communication/can-bus-security, communication/ethernet-security | SecOC, firewall, IDS, DoIP gateway |
| Telematics (TCU) | attack-surfaces/wireless-interfaces, mechanisms/ota-security, mechanisms/idps | TLS, certificate management, OTA client |
| ADAS / AD | architecture/functional-safety-security, communication/ethernet-security | ASIL-D + security, sensor integrity |
| IVI / Head Unit | architecture/sdv-security, attack-surfaces/wireless-interfaces | Sandboxing, app security, BT/Wi-Fi hardening |
| Body Controller | communication/can-bus-security, attack-surfaces/wireless-interfaces, mechanisms/secure-diagnostics | Key fob auth, UWB, access control |
| EV Charger Interface | attack-surfaces/ev-charging | ISO 15118, Plug&Charge PKI |
| OTA System | mechanisms/ota-security, mechanisms/automotive-pki-key-management | Code signing, anti-rollback, Uptane |

## Standards Cross-Reference

| Standard | Covered In |
|----------|-----------|
| UNECE R155 | standards/compliance-standards.md |
| UNECE R156 | standards/compliance-standards.md, mechanisms/ota-security.md |
| ISO/SAE 21434 | standards/compliance-standards.md, standards/threat-modeling.md |
| ISO 26262 | architecture/functional-safety-security.md |
| ISO 15118 | attack-surfaces/ev-charging.md |
| ISO 14229 (UDS) | mechanisms/secure-diagnostics.md |
| ISO 13400 (DoIP) | mechanisms/secure-diagnostics.md, communication/ethernet-security.md |
| IEEE 1609.2 | communication/v2x-security.md |
| AUTOSAR SecOC | communication/autosar-security.md, communication/can-bus-security.md |
| AUTOSAR IdsM | mechanisms/idps.md, communication/autosar-security.md |
| AUTOSAR Adaptive | architecture/sdv-security.md, communication/autosar-security.md |
| CCC Digital Key | attack-surfaces/wireless-interfaces.md |
| OCPP 2.0.1 | attack-surfaces/ev-charging.md |
| TISAX / VDA ISA | standards/compliance-standards.md |
