# CAN Bus Security Deep Dive

## CAN Protocol Weaknesses

| Weakness | Description | Exploitability |
|----------|-------------|---------------|
| No authentication | Any node can send any ID | Trivial injection |
| No encryption | All traffic readable by all nodes | Passive eavesdropping |
| No sender identification | CAN ID ≠ sender identity | Spoofing |
| Priority-based arbitration | Lower ID = higher priority | DoS via ID 0x000 |
| Broadcast medium | All nodes see all messages | No confidentiality |
| Error handling | Bus-off attack possible | Targeted node isolation |

## Attack Taxonomy

### 1. Injection Attacks
```
Attacker (via OBD-II, compromised ECU, or physical access):
  → Send CAN frame with legitimate ID but malicious data
  → Example: Inject Steering Angle message (ID 0x0025)
  → Vehicle actuators respond to injected commands
```

### 2. Replay Attacks
```
1. Record legitimate message sequence (e.g., door unlock)
2. Replay recorded frames at later time
3. Without freshness (counter/timestamp), receiver cannot distinguish replay
```

### 3. Bus-Off Attack
```
CAN error handling:
  Transmit Error Counter (TEC) increments on transmission errors
  TEC > 255 → Node enters Bus-Off state (disconnected!)

Attack:
  Attacker sends dominant bit during victim's recessive bit
  → Victim detects bit-stuffing error
  → Victim increments TEC
  → Repeated → victim enters Bus-Off
  → Safety-critical ECU silenced!
```

### 4. Diagnostic Abuse
```
UDS via CAN:
  0x27 (Security Access) → Brute force seed/key
  0x2E (Write Data) → Modify calibration
  0x31 (Routine Control) → Activate actuators
  0x34/0x36/0x37 → Upload malicious firmware
```

## CAN Security Controls

### SecOC (Secure Onboard Communication)

#### CAN 2.0 (8 bytes payload)
```
Classic CAN frame: 8 bytes total
┌────────────────────────────┐
│ Data (4B) │ FV (1B) │MAC(3B)│  ← Very limited space!
└────────────────────────────┘

Challenges:
- Only 3 bytes (24 bits) for MAC → 2^24 ≈ 16M attempts to forge
- Only 1 byte for freshness value → wraps quickly
- Must sacrifice data bytes for security overhead
```

#### CAN FD (64 bytes payload)
```
CAN FD frame: up to 64 bytes
┌──────────────────────────────────────────────────────┐
│ Data (variable) │ Freshness (4-8B) │ MAC (6-8B)     │
└──────────────────────────────────────────────────────┘

Much better:
- 48-64 bit MAC → practical forgery resistance
- Full freshness counter → strong replay protection
- More data capacity preserved
```

### Message Allowlisting (Gateway Firewall)
```
Gateway configuration:
  CAN_Bus_1 (Powertrain) → CAN_Bus_2 (Body):
    ALLOW: [0x100, 0x101, 0x102]  (engine status to dashboard)
    DENY:  [0x000-0x0FF]          (no low-priority IDs cross)
    DENY:  ALL others             (default deny)

  OBD-II Port → CAN_Bus_1 (Powertrain):
    ALLOW: [0x7DF, 0x7E0-0x7E7]  (standard diagnostic IDs only)
    RATE:  max 100 msgs/sec       (prevent flooding)
    DENY:  ALL others
```

### Timing-Based Anomaly Detection
```python
# Simplified IDPS timing check (conceptual)
class CANTimingMonitor:
    def __init__(self):
        self.expected_intervals = {
            0x100: 10,    # Engine RPM: every 10ms
            0x200: 20,    # Wheel speed: every 20ms
            0x300: 100,   # Temperature: every 100ms
        }
        self.last_seen = {}

    def check_message(self, can_id, timestamp):
        if can_id in self.last_seen:
            interval = timestamp - self.last_seen[can_id]
            expected = self.expected_intervals.get(can_id, None)

            if expected and interval < expected * 0.5:
                # Message arriving too fast → possible injection!
                raise Alert(f"Timing anomaly: ID 0x{can_id:03X} "
                           f"interval={interval}ms (expected {expected}ms)")

        self.last_seen[can_id] = timestamp
```

## CAN FD Security Advantages

| Feature | CAN 2.0 | CAN FD |
|---------|---------|--------|
| Max payload | 8 bytes | 64 bytes |
| Bitrate (data phase) | 1 Mbps | 2-8 Mbps |
| SecOC overhead budget | ~3-4 bytes | ~16+ bytes |
| MAC strength | 24 bits (weak) | 64+ bits (strong) |
| Freshness value space | 4-8 bits | 32+ bits |

## Practical Tools for CAN Security Testing

| Tool | Purpose |
|------|---------|
| `can-utils` (Linux) | Send/receive CAN frames, candump, cansend |
| `SavvyCAN` | GUI CAN analysis, DBC support |
| `CANalyzer` / `CANoe` (Vector) | Professional CAN analysis |
| `python-can` | Python library for CAN |
| `scapy` | CAN frame crafting |
| `caringcaribou` | Automotive security testing framework |
| `UDSim` | UDS ECU simulator |

### Example: CAN Injection with python-can
```python
import can

# Connect to CAN interface
bus = can.interface.Bus(channel='vcan0', interface='socketcan')

# Inject a spoofed message (speed = 0 to disable speed-dependent door lock)
spoofed_msg = can.Message(
    arbitration_id=0x0B4,  # Example: vehicle speed message
    data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    is_extended_id=False
)

# Send at expected interval to overpower legitimate message
import time
for _ in range(1000):
    bus.send(spoofed_msg)
    time.sleep(0.01)  # 10ms interval (match original)
```

## Defense Layers (Defense in Depth)

```
Layer 1: Physical → Isolate diagnostic port, add gateway
Layer 2: Network → Message allowlisting, rate limiting at gateway
Layer 3: Authentication → SecOC (CMAC on safety messages)
Layer 4: Detection → IDPS (timing, frequency, content anomalies)
Layer 5: Response → Log event, alert backend, safe state
```

## References
- AUTOSAR SecOC SWS
- SAE J1939 Security (heavy vehicles)
- CAN in Automation (CiA) 601 series
- ISO 11898 (CAN protocol)
- Charlie Miller & Chris Valasek CAN research
