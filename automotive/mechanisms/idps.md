# Automotive IDPS — Intrusion Detection & Prevention System

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        VEHICLE IDPS ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │ CAN IDS  │  │ ETH IDS  │  │ Host IDS │  │ V2X IDS  │  ← Sensors   │
│  │ (per bus)│  │(per VLAN)│  │ (per ECU)│  │  (OBU)   │               │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘               │
│       │              │              │              │                      │
│       └──────────────┴──────┬───────┴──────────────┘                     │
│                             │                                            │
│                    ┌────────▼────────┐                                   │
│                    │  IDS Manager    │  ← Correlation, deduplication     │
│                    │  (IdsM/SecM)    │    Priority assignment             │
│                    └────────┬────────┘                                   │
│                             │                                            │
│              ┌──────────────┼──────────────┐                            │
│              ▼              ▼              ▼                             │
│     ┌──────────────┐ ┌──────────┐ ┌────────────┐                       │
│     │ Local Action │ │ Logging  │ │ Report to  │                        │
│     │ (block/rate  │ │ (secure  │ │ Backend    │  ← SOC/VSOC           │
│     │  limit)      │ │  store)  │ │ (SIEM)     │                        │
│     └──────────────┘ └──────────┘ └────────────┘                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Detection Methods

### 1. CAN Bus IDS

#### Content-Based Detection
```
Rule: Check message payload against allowed value ranges

Example — Engine RPM message (ID 0x0C0):
  Byte 0-1: RPM value (0-8000 valid)
  Byte 2:   Engine temp (0-130°C valid)

  Alert if: RPM > 8000 OR temp > 150 (physically impossible values)
  Alert if: Reserved bits are non-zero (indicates crafted frame)
```

#### Timing-Based Detection
```python
# Detect anomalous message timing on CAN bus
# CAN messages are periodic — deviation indicates injection

import can
import time

class CANTimingIDS:
    def __init__(self):
        self.msg_timing = {}  # {arb_id: [last_seen, expected_interval, tolerance]}

    def learn_baseline(self, bus, duration=60):
        """Learn normal timing for each CAN ID during baseline period."""
        timestamps = {}  # {arb_id: [timestamps]}
        end_time = time.time() + duration

        while time.time() < end_time:
            msg = bus.recv(timeout=1.0)
            if msg:
                if msg.arbitration_id not in timestamps:
                    timestamps[msg.arbitration_id] = []
                timestamps[msg.arbitration_id].append(msg.timestamp)

        for arb_id, ts_list in timestamps.items():
            if len(ts_list) > 10:
                intervals = [ts_list[i+1] - ts_list[i] for i in range(len(ts_list)-1)]
                avg_interval = sum(intervals) / len(intervals)
                std_dev = (sum((x - avg_interval)**2 for x in intervals) / len(intervals)) ** 0.5
                self.msg_timing[arb_id] = {
                    'interval': avg_interval,
                    'tolerance': max(std_dev * 3, 0.001)  # 3-sigma or 1ms minimum
                }

    def monitor(self, bus):
        """Monitor CAN bus for timing anomalies."""
        last_seen = {}

        while True:
            msg = bus.recv(timeout=1.0)
            if msg and msg.arbitration_id in self.msg_timing:
                arb_id = msg.arbitration_id
                expected = self.msg_timing[arb_id]

                if arb_id in last_seen:
                    actual_interval = msg.timestamp - last_seen[arb_id]

                    # Extra message injected (interval too short)
                    if actual_interval < expected['interval'] - expected['tolerance']:
                        self.alert(arb_id, 'INJECTION', actual_interval, expected['interval'])

                    # Message suppressed (interval too long)
                    elif actual_interval > expected['interval'] + expected['tolerance']:
                        self.alert(arb_id, 'SUPPRESSION', actual_interval, expected['interval'])

                last_seen[arb_id] = msg.timestamp

    def alert(self, arb_id, alert_type, actual, expected):
        print(f"[ALERT] {alert_type}: ID 0x{arb_id:03X} "
              f"interval={actual*1000:.1f}ms (expected={expected*1000:.1f}ms)")
```

#### Sequence-Based Detection
```
Known attack patterns to detect:

1. CAN Injection (theft):
   Signal: 10+ unlock commands within 100ms (normal: 1 per button press)

2. Bus-Off Attack:
   Signal: Dominant error frames targeting specific ECU's ID
   Detection: Error counter spikes + specific ID disappears

3. Diagnostic Abuse:
   Signal: 0x7DF (broadcast diagnostic) followed by multiple 0x7Ex responses
   Context: Vehicle is driving (diagnostics unusual while moving)

4. Replay Attack:
   Signal: Exact sequence of messages repeated (same data, correct IDs)
   Detection: Freshness counter / sequence number mismatch
```

### 2. Ethernet IDS

#### Deep Packet Inspection
```yaml
# Suricata-style rules for automotive Ethernet

# Detect SOME/IP service discovery flooding
alert someip any any -> any any (msg:"SOME/IP SD flood";
  someip_type:notification; threshold:type both, track by_src, count 100, seconds 1;
  sid:1000001;)

# Detect DoIP (Diagnostics over IP) unauthorized access
alert tcp any any -> any 13400 (msg:"DoIP routing activation from untrusted source";
  flow:to_server,established; content:"|00 05|"; offset:2; depth:2;
  sid:1000002;)

# Detect ARP spoofing (Ethernet MitM)
alert arp any any -> any any (msg:"ARP cache poisoning attempt";
  arp_opcode:2; threshold:type both, track by_src, count 10, seconds 5;
  sid:1000003;)

# Detect unauthorized VLAN access (VLAN hopping)
alert vlan any any -> any any (msg:"Double VLAN tag detected";
  content:"|81 00|"; offset:12; content:"|81 00|"; distance:2; within:4;
  sid:1000004;)
```

#### Protocol State Machine Monitoring
```
SOME/IP Service State Machine:
  Expected: FindService → OfferService → Subscribe → Notify
  Anomaly:  Direct method call without prior service discovery

DoIP State Machine:
  Expected: RoutingActivation → DiagRequest → DiagResponse
  Anomaly:  DiagRequest without successful RoutingActivation

UDS over DoIP:
  Expected: DiagSessionControl → SecurityAccess → Write/Flash
  Anomaly:  Direct write attempt without security unlock
```

### 3. Host-Based IDS (HIDS)

```
Monitor on each ECU / HPC:
├── Process integrity (unexpected processes, code injection)
├── File system changes (unauthorized writes to flash)
├── Memory anomalies (buffer overflow indicators)
├── Resource consumption (CPU/memory DoS)
├── System call patterns (abnormal syscall sequences)
├── Network connections (unexpected outbound connections)
└── Secure boot chain (boot measurement validation)
```

### 4. Machine Learning Detection

| Method | Detection Target | Pros | Cons |
|--------|-----------------|------|------|
| LSTM/RNN | Temporal patterns in CAN | Catches novel attacks | Training data needed, compute-heavy |
| Autoencoder | Anomaly in message payloads | Unsupervised, adaptive | High false positive rate |
| Random Forest | Known attack classification | Fast inference, interpretable | Misses zero-days |
| One-Class SVM | Novelty detection | Low false positives when tuned | Limited to simple features |
| CNN | Signal-level CAN analysis | Captures spatial patterns | Requires GPU or FPGA |

## AUTOSAR IdsM (Intrusion Detection System Manager)

### Architecture (AUTOSAR Classic Platform)
```
┌──────────────────────────────────────────────────────────┐
│ AUTOSAR BSW                                               │
│                                                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌───────────┐  │
│  │ SecOC   │  │  PduR    │  │  COM    │  │ Firewall  │  │
│  └────┬────┘  └────┬────┘  └────┬────┘  └─────┬─────┘  │
│       │             │            │              │         │
│       │  Security Event (SecEv)  │              │         │
│       ▼             ▼            ▼              ▼         │
│  ┌───────────────────────────────────────────────────┐   │
│  │              IdsM (IDS Manager)                    │   │
│  │  • Collect security events from all BSW modules   │   │
│  │  • Filter & qualify events (reduce noise)         │   │
│  │  • Assign severity & priority                     │   │
│  │  • Buffer events for transmission                 │   │
│  └───────────────────────────┬───────────────────────┘   │
│                              │                            │
│                              ▼                            │
│  ┌───────────────────────────────────────────────────┐   │
│  │              DEM (Diagnostic Event Manager)        │   │
│  │  • Store security DTCs                            │   │
│  │  • Report to diagnostic tester                    │   │
│  └───────────────────────────────────────────────────┘   │
│                                                           │
└──────────────────────────────────────────────────────────┘
        │
        ▼ (via PDU/Ethernet to TCU)
┌──────────────────┐
│  Backend SIEM    │  → Vehicle SOC (VSOC)
└──────────────────┘
```

### Security Events (IdsM)
```c
// Security Event Types defined in AUTOSAR:
typedef enum {
    IDSM_SEV_AUTH_FAILURE,        // SecOC MAC verification failed
    IDSM_SEV_CRYPTO_FAILURE,      // Key/cert operation failed
    IDSM_SEV_FIREWALL_BLOCKED,    // Packet dropped by firewall rule
    IDSM_SEV_TIMING_ANOMALY,      // Message timing violation
    IDSM_SEV_ACCESS_DENIED,       // Unauthorized diagnostic access
    IDSM_SEV_SECURE_BOOT_FAIL,    // Boot measurement mismatch
    IDSM_SEV_MEMORY_VIOLATION,    // MPU/MMU access violation
    IDSM_SEV_COUNTER_MISMATCH,    // Freshness counter desync
    IDSM_SEV_UNKNOWN_MESSAGE,     // Unrecognized CAN ID on bus
    IDSM_SEV_DOS_DETECTED         // Flood / resource exhaustion
} IdsM_SecurityEventType;
```

## Vehicle SOC (VSOC) Integration

### Data Flow: Vehicle → Backend
```
1. ECU detects anomaly → generates SecurityEvent
2. IdsM collects, filters (debouncing: don't report same event 1000x)
3. IdsM packages events → QueuedSecurityEvent
4. TCU transmits to backend (batch, low priority to save bandwidth)
5. Backend SIEM correlates across fleet
6. Analyst/automation decides response
```

### Fleet-Level Detection
```
Single vehicle alert: might be false positive
Same alert across 50 vehicles in same region: likely real attack

Fleet correlation enables:
- Detect distributed attacks (V2X misbehavior across multiple vehicles)
- Identify compromised OTA updates (same anomaly post-update fleet-wide)
- Geographic correlation (attacks near specific infrastructure)
- Model year correlation (vulnerability in specific HW revision)
```

### Response Actions

| Level | Action | Example |
|-------|--------|---------|
| 0 - Log | Record only | Unusual CAN timing (single event) |
| 1 - Alert | Notify VSOC | Multiple SecOC failures |
| 2 - Rate Limit | Throttle traffic | DoS attempt on bus |
| 3 - Block | Drop messages | Known malicious pattern |
| 4 - Isolate | Disable interface | Compromised TCU → disconnect from CAN |
| 5 - Safe State | Limp mode / pull over | Critical safety ECU compromise |

## Performance Constraints

| Parameter | Requirement | Rationale |
|-----------|-------------|-----------|
| Detection latency | <10ms (CAN), <50ms (Ethernet) | Must detect before damage |
| CPU overhead | <5% of ECU capacity | Don't impact primary function |
| RAM for rules | <64KB per sensor | Embedded MCU constraints |
| False positive rate | <0.01% | Avoid alert fatigue at VSOC |
| Message throughput | 10,000+ msg/sec (CAN FD) | Full bus load analysis |
| Boot time addition | <100ms | Vehicle start time budget |

## Deployment Considerations

### Rule Updates
```
Challenge: Update IDS signatures without full OTA ECU reflash

Solutions:
1. Separate rule partition (updateable via lightweight OTA)
2. Backend-pushed rule database (if ECU has connectivity)
3. ML model hot-swap (new model weights, same inference engine)
4. CAN ID allowlist update via diagnostic service (UDS)
```

### False Positive Management
```
Causes:
- Aftermarket accessories (non-standard CAN messages)
- Software updates changing message timing
- Extreme temperatures affecting clock accuracy
- Manufacturing variance in ECU timing
- New features added via OTA (new CAN IDs)

Mitigations:
- Learning mode after ECU flash / OTA update
- Configurable sensitivity per CAN ID
- Allowlist for aftermarket device IDs (via dealer)
- Adaptive baseline (slowly adjust to drift)
- Fleet-validated rules (only deploy if <0.01% FP rate on test fleet)
```

## Standards & Requirements

| Standard | IDPS Requirement |
|----------|-----------------|
| UNECE R155 (7.1) | "Detect and respond to cyber attacks" |
| ISO/SAE 21434 §9 | Cybersecurity monitoring throughout lifecycle |
| AUTOSAR | IdsM module specification |
| ISO 21111-7 | Vehicle SIEM data format |

## Commercial & Open Source

### Articles/Blogs
* [Argus Ethernet protection](https://argus-sec.com/products/ethernet-protection/)
* [Argus CAN protection](https://argus-sec.com/products/can-protection/)
* [Argus CAN protection technical blog](https://argus-sec.com/blog/blog-post/what-oems-can-do-to-prevent-can-injection-car-theft/)
* [Argus CAN IDS implementation](https://argus-sec.com/blog/cyber-security-blog/argus-can-ids-production-grade-integration-now-takes-only-one-month-with-new-argus-can-ids-api-and-generic-cpu-architecture-support/)

### Open Source Implementations
* [wolfsentry](https://github.com/wolfSSL/wolfsentry) — Embedded IDPS engine
* [Suricata](https://suricata.io/) — Network IDS (adaptable for automotive Ethernet)
* [Zeek](https://zeek.org/) — Network analysis framework
* [CAN-IDS (research)](https://github.com/topics/can-ids) — Various academic CAN IDS projects
