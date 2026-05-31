# Wireless Interface Security — Bluetooth, Key Fob, TPMS, UWB, NFC

## Attack Surface Map

```
┌──────────────────────────────────────────────────────────────────┐
│                  WIRELESS INTERFACE THREATS                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Range   Interface     Frequency      Primary Threat              │
│  ─────   ─────────     ─────────      ──────────────              │
│  ~100m   Bluetooth     2.4 GHz        MitM, tracking              │
│  ~100m   Wi-Fi         2.4/5 GHz      Rogue AP, code execution    │
│  ~50m    Key Fob (RKE) 315/433/868MHz Relay, replay, rolljam      │
│  ~10m    BLE           2.4 GHz        Relay, GATT exploit         │
│  ~10m    UWB           6-8 GHz        (Resistant to relay)        │
│  ~5m     NFC           13.56 MHz      Relay, clone                │
│  ~3m     TPMS          315/433 MHz    Spoofing, tracking          │
│  ~1m     Wireless Charging 85 kHz     MitM on charging session    │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## Key Fob / Remote Keyless Entry (RKE)

### Protocol Evolution

| Generation | Mechanism | Security Level |
|-----------|-----------|---------------|
| Gen 1 | Fixed code | Trivial replay |
| Gen 2 | Rolling code (KeeLoq) | Broken (algebraic attack) |
| Gen 3 | AES rolling code | Strong (current standard) |
| Gen 4 | Challenge-response (UWB) | Distance-bounding |

### Rolling Code (Keeloq) — How It Works
```
Key fob stores: Serial (fixed) + Rolling counter + Encryption key

Transmission:
┌──────────────────────────────────────────────────────┐
│ Fixed Part (32 bits)     │ Encrypted Part (32 bits)   │
│ Serial number            │ Enc(counter + buttons)     │
│ (identifies fob)         │ (KeeLoq cipher)            │
└──────────────────────────────────────────────────────┘

Car receives:
1. Match serial → identify which key fob
2. Decrypt rolling part → extract counter
3. Check counter > last_seen (anti-replay)
4. If valid AND counter in window → unlock
5. Increment last_seen counter

Window: typically accepts counter + 1 to counter + 256
  (allows for button presses out of range)
```

### Relay Attack (Passive Entry)

```
Passive Entry System (keyless go):
  Car constantly broadcasts LF challenge (125 kHz, ~2m range)
  Key fob responds with UHF reply (315/433 MHz, ~50m range)

  Normal: Driver near car → LF reaches fob → fob responds → unlock

Relay Attack:
  Attacker 1 (near car) ──[relay device]──→ Attacker 2 (near fob/owner)

  1. Attacker 1's device captures LF challenge from car
  2. Transmits over radio link to Attacker 2
  3. Attacker 2's device re-broadcasts LF near the fob (owner's pocket)
  4. Fob responds with UHF (thinks car is nearby)
  5. Attacker 2 captures UHF response, relays back to Attacker 1
  6. Attacker 1 re-broadcasts response near car
  7. Car unlocks! (and engine starts with Push-to-Start)

  Total latency added: ~10µs (below detection threshold for most cars)
  Cost: $20-100 for relay equipment
  Success rate: >95% on vulnerable vehicles
```

### Relay Attack Mitigations

| Mitigation | Method | Effectiveness |
|-----------|--------|--------------|
| UWB ranging | Measure time-of-flight (speed of light) | Very high (can't relay faster than light) |
| Motion sensor in fob | Fob must be moving to respond | Medium (defeats "fob on table" attack) |
| LF signal attenuation | Reduce LF range to <1m | Low (amplifiable) |
| User confirmation | Require button press | High (but removes "passive" convenience) |
| Faraday pouch | Block all RF from fob | High (user responsibility) |
| BLE distance estimation | RSSI-based ranging | Low (easily spoofed/amplified) |

### RollJam Attack
```
1. Attacker jams RKE frequency (blocks car from receiving)
2. Fob owner presses button → Attacker captures signal (Counter N)
3. Owner presses again → Attacker captures (Counter N+1), replays N to car
4. Car unlocks with N (owner thinks it worked on second press)
5. Attacker now holds valid unused code N+1 for later use!

Defense: Challenge-response (car sends unique challenge each time)
```

## Bluetooth / BLE Security

### Classic Bluetooth Attacks

| Attack | Method | Impact |
|--------|--------|--------|
| BlueSmack | L2CAP ping flood | DoS on IVI |
| BlueBorne | RCE via Bluetooth stack bugs (CVE-2017-0781) | Full compromise without pairing |
| KNOB | Negotiate 1-byte encryption key | MitM |
| BIAS | Spoof already-paired device | Impersonation |
| Bluesnarfing | Unauthorized data access (OBEX) | PII extraction |
| Car Whisperer | Default PIN on hands-free (0000/1234) | Audio interception |

### BLE (Bluetooth Low Energy) in Automotive

```
Uses:
- Digital car key (phone-as-key)
- Tire pressure monitoring (some systems)
- Diagnostic tools (aftermarket)
- Phone presence detection (passive entry)

BLE Phone Key Flow:
1. Phone approaches car → BLE advertisement detected
2. Car sends challenge (encrypted with shared key)
3. Phone signs challenge in Secure Element
4. Car verifies → unlock (+ start with additional verification)

Vulnerabilities:
- BLE relay attack (similar to RKE relay)
  Latency ~10ms (within BLE timeout)
  Mitigation: UWB for ranging

- GATT service enumeration
  Discover exposed characteristics → modify writable ones

- Pairing bypass (Just Works mode = no authentication)
  Use Numeric Comparison or OOB pairing for automotive!
```

### BLE Security Best Practices (Automotive)
```
1. Use LE Secure Connections (ECDH key exchange, not Legacy Pairing)
2. Enforce MITM protection (Numeric Comparison, not Just Works)
3. Implement UWB for distance verification (CCC Digital Key 3.0)
4. Store keys in Secure Element (phone-side) and HSM (car-side)
5. Rate-limit pairing attempts (prevent brute force)
6. Bond only in controlled environment (manufacturing or first owner setup)
7. Support key revocation (if phone lost/stolen)
```

## UWB (Ultra-Wideband) — Secure Ranging

### Why UWB Defeats Relay Attacks
```
UWB time-of-flight measurement:
  - Signal travels at speed of light (3×10⁸ m/s)
  - 1 nanosecond = 30cm distance
  - UWB measures with <10cm accuracy

  Relay attack adds latency:
  - Even at light speed, relay adds distance
  - Any relay device adds processing delay (>1ns)
  - UWB detects: measured distance ≠ expected distance

  Result: Relay attack becomes physically impossible to hide!
```

### CCC Digital Key (Car Connectivity Consortium)

```
CCC Digital Key Standard:
  Version 2.0: BLE-based (vulnerable to relay)
  Version 3.0: UWB ranging + BLE for data (relay-resistant)

Architecture:
  Phone: Secure Element → stores ECDSA key pair + UWB keys
  Car:   HSM/Secure MCU → stores paired device records

  Phase 1 (BLE): Mutual authentication + session key establishment
  Phase 2 (UWB): Secure ranging (distance measurement)
  Phase 3 (Action): Unlock/lock/start based on distance + authentication

  Distance zones:
    >30m:  Nothing (out of range)
    10-30m: Wake up system, prepare
    2-10m:  Unlock doors (approach detection)
    <1m:    Allow engine start (proximity confirmed)
```

## TPMS (Tire Pressure Monitoring System)

### Protocol Details
```
Frequency: 315 MHz (US) or 433.92 MHz (EU)
Modulation: ASK or FSK
Data: Sensor ID (32-bit) + Pressure + Temperature + Battery status
Encryption: NONE on most vehicles (plaintext broadcast!)
Range: ~3m (sensor to receiver), receivable at >50m with amplified antenna
```

### TPMS Attacks

| Attack | Description | Impact |
|--------|-------------|--------|
| Eavesdropping | Capture sensor IDs at distance | Vehicle tracking (unique IDs) |
| Spoofing | Broadcast fake pressure data | Trigger warnings, confuse driver |
| ID cloning | Record and replay sensor ID | Mask real sensor data |
| DoS | Continuous invalid data broadcast | Overwhelm receiver, disable TPMS |

### TPMS Security Implications
```
Tracking:
  - Each TPMS sensor has unique 32-bit ID
  - Broadcast continuously while driving
  - Receivable at 40m+ with directional antenna
  - Can track specific vehicle by monitoring roadside

  Mitigation:
  - Rotating IDs (not implemented in practice)
  - Encrypted payloads (emerging in premium vehicles)
  - Reduce transmission power (less range for eavesdropping)

Spoofing:
  - Trigger false low-pressure warning → driver stops
  - Suppress real low-pressure → unsafe driving condition

  Mitigation:
  - Plausibility check (compare with ABS wheel speed sensors)
  - Authentication (HMAC on sensor data — future standard)
```

## NFC Digital Key

```
NFC (13.56 MHz, ~5cm range):
  Used for: Backup key (when phone battery dead), valet mode

  Standard: CCC Digital Key + ISO 14443 / ISO 7816

  Security:
  ├── Mutual authentication (AES-128 or ECDSA)
  ├── Secure channel (encrypted NFC communication)
  ├── Key stored in phone's Secure Element (not in app memory!)
  ├── Anti-replay (session nonces)
  └── Relay possible but range is tiny (requires device within 5cm)

  NFC Relay Attack:
  - Requires attacker device within ~5cm of phone AND ~5cm of car reader
  - Much harder to execute than RKE relay
  - Mitigated by requiring screen unlock / biometric on phone
```

## Wi-Fi in Vehicles

### Attack Scenarios
```
1. Rogue AP (Evil Twin):
   - Clone vehicle's hotspot SSID
   - Passengers connect to attacker's AP
   - MitM all traffic

2. IVI Wi-Fi Stack Exploit:
   - Vulnerability in Wi-Fi chipset firmware (Broadcom, Qualcomm)
   - Send crafted management frames → code execution
   - Example: CVE-2017-9417 (Broadpwn) — RCE via Wi-Fi probe responses

3. WPA2 KRACK on Vehicle Hotspot:
   - Force key reinstallation on vehicle AP
   - Decrypt/inject traffic

4. Deauthentication:
   - Force disconnect Wi-Fi clients
   - DoS on connectivity features

5. OTA Update over Wi-Fi:
   - If vehicle downloads updates via Wi-Fi
   - Rogue AP could serve malicious content
   - Mitigation: TLS + certificate pinning + package signing
```

### Wi-Fi Hardening for Automotive
```
1. WPA3-Personal (SAE) or WPA3-Enterprise for vehicle hotspot
2. Disable WPS (Wi-Fi Protected Setup) — PIN brute forceable
3. Isolate Wi-Fi interface from vehicle internal networks (VLAN)
4. Disable management frame processing from untrusted sources
5. Regular firmware updates for Wi-Fi chipset
6. Client isolation (passengers can't see each other)
7. Captive portal with ToS for guest access
8. Rate limiting and traffic shaping
```

## Consolidated Security Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│               WIRELESS SECURITY REFERENCE ARCHITECTURE            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Interface Layer:                                                 │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐             │
│  │ BLE │ │ UWB │ │ NFC │ │Wi-Fi│ │ RKE │ │TPMS │             │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘             │
│     │        │        │        │        │        │               │
│  ┌──┴────────┴────────┴────────┴────────┴────────┴──┐           │
│  │           Wireless Security Gateway               │           │
│  │  • Protocol validation      • Rate limiting       │           │
│  │  • Authentication verify    • Anomaly detection   │           │
│  │  • Encryption termination   • Logging             │           │
│  └──────────────────────┬───────────────────────────┘           │
│                          │                                        │
│  ┌───────────────────────┴───────────────────────────┐          │
│  │                Body Domain Controller               │          │
│  │  • Access control logic    • Key management        │          │
│  │  • UWB distance decision   • Anti-theft state      │          │
│  │  • Multi-factor auth       • Secure logging        │          │
│  └────────────────────────────────────────────────────┘          │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```
