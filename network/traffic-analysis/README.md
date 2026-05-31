# Traffic Analysis & Network Forensics

## Wireshark Essentials

### Critical Display Filters
```
# Protocol-specific
tcp.port == 443                    # HTTPS traffic
http.request.method == "POST"      # HTTP POST requests
dns.qry.name contains "evil"      # DNS queries matching pattern
tls.handshake.type == 1           # TLS Client Hello
smb2.cmd == 5                     # SMB2 Create (file access)

# Anomaly hunting
tcp.analysis.retransmission       # Retransmissions (network issues)
tcp.analysis.zero_window          # Flow control issues
tcp.flags.syn == 1 && tcp.flags.ack == 0  # SYN packets (scans)
dns.flags.response == 1 && dns.flags.rcode != 0  # DNS errors

# Security-focused
http.request.uri contains "cmd"   # Possible command injection
http.response.code == 500         # Server errors (exploitation?)
icmp.type == 8 && data.len > 64  # Large ICMP (possible tunneling)
tcp.dstport == 4444              # Common reverse shell port
```

### Capture Filters (BPF Syntax)
```bash
# Capture only specific traffic (reduces file size)
tcpdump -i eth0 -w capture.pcap 'port 80 or port 443'
tcpdump -i eth0 -w capture.pcap 'host 10.10.10.5 and port 445'
tcpdump -i eth0 -w capture.pcap 'icmp'
tcpdump -i eth0 -w capture.pcap 'tcp[tcpflags] & tcp-syn != 0'
```

### Extract Artifacts from PCAP
```bash
# Extract files transferred over HTTP
tshark -r capture.pcap --export-objects http,exported_files/

# Extract files from SMB
tshark -r capture.pcap --export-objects smb,exported_smb/

# Extract TLS certificates
tshark -r capture.pcap -Y "tls.handshake.certificate" \
  -T fields -e tls.handshake.certificate

# DNS query list
tshark -r capture.pcap -Y "dns.flags.response == 0" \
  -T fields -e dns.qry.name | sort -u

# HTTP credentials (Basic auth)
tshark -r capture.pcap -Y "http.authorization" \
  -T fields -e http.authorization

# Extract all URLs
tshark -r capture.pcap -Y "http.request" \
  -T fields -e http.host -e http.request.uri
```

## Protocol Analysis

### TLS/SSL Analysis
```bash
# JA3 fingerprinting (identify client applications by TLS fingerprint)
# JA3 = MD5(SSLVersion,Ciphers,Extensions,EllipticCurves,EllipticCurvePointFormats)

# Detect known malware C2 by JA3 hash
tshark -r capture.pcap -Y "tls.handshake.type == 1" \
  -T fields -e ip.src -e ja3.hash

# Known malicious JA3 hashes (example):
# Cobalt Strike: a0e9f5d64349fb13191bc781f81f42e1
# Metasploit:    5d65ea3fb1d4aa7d499be5adf45f4767

# JA3S (server fingerprint)
tshark -r capture.pcap -Y "tls.handshake.type == 2" \
  -T fields -e ip.src -e ja3s.hash

# Certificate analysis
openssl s_client -connect target:443 </dev/null 2>/dev/null | \
  openssl x509 -noout -text

# Check certificate transparency logs
# https://crt.sh/?q=%.target.com
```

### SMB/NTLM Analysis
```bash
# Extract NTLM hashes from network capture
# NTLMv2 challenge/response can be cracked with hashcat

tshark -r capture.pcap -Y "ntlmssp.auth" \
  -T fields -e ntlmssp.auth.username -e ntlmssp.auth.domain

# Format for hashcat (mode 5600):
# username::domain:challenge:NTProofStr:NTResponse(without first 16 bytes)
```

### Kerberos Analysis
```bash
# Extract Kerberos tickets from pcap
tshark -r capture.pcap -Y "kerberos.msg_type == 13" \
  -T fields -e kerberos.CNameString -e kerberos.realm

# AS-REP Roasting (pre-auth disabled accounts)
tshark -r capture.pcap -Y "kerberos.msg_type == 11 && kerberos.error_code == 0"
```

## Network Forensics Methodology

### 1. Evidence Collection
```bash
# Full packet capture (PCAP)
tcpdump -i eth0 -w evidence.pcap -s 0  # Full packets, no truncation

# NetFlow/IPFIX (metadata only — who talked to whom)
# Useful for: connection patterns, data volumes, timing

# DNS logs (passive DNS)
# Useful for: domain resolution history, tunneling detection
```

### 2. Timeline Analysis
```bash
# Extract connection timestamps
tshark -r evidence.pcap -T fields \
  -e frame.time -e ip.src -e ip.dst -e tcp.dstport \
  -Y "tcp.flags.syn == 1 && tcp.flags.ack == 0" > connections.csv

# Sort by time, identify:
# - Initial compromise timestamp
# - Lateral movement attempts
# - Data exfiltration windows
# - C2 beacon intervals
```

### 3. C2 (Command & Control) Detection
```
Indicators of C2 beaconing:
├── Regular time intervals between connections (jitter ±10%)
├── Consistent data sizes (heartbeat packets)
├── Connections to IP addresses (no DNS)
├── Self-signed or recently issued certificates
├── JA3 hashes matching known malware
├── DNS queries with high entropy subdomains
├── HTTP requests with encoded/encrypted POST bodies
└── Long-lived TCP connections with periodic small data bursts
```

### 4. Data Exfiltration Detection
```
Indicators:
├── Large outbound transfers (bytes_out >> bytes_in)
├── Transfers outside business hours
├── Connections to cloud storage (pastebin, mega, dropbox)
├── DNS TXT queries with Base64-like content
├── ICMP packets with large payloads
├── Encrypted traffic to unusual ports
└── Steganography (images with hidden data)
```

## Tools

| Tool | Purpose |
|------|---------|
| Wireshark | Interactive packet analysis |
| tshark | CLI packet analysis (scripting) |
| tcpdump | Packet capture |
| NetworkMiner | Artifact extraction, OS fingerprinting |
| Zeek | Protocol logging, scripting |
| Arkime (Moloch) | Large-scale PCAP storage + search |
| Rita | Beacon detection, DNS analysis |
| PCredz | Credential extraction from PCAP |
| Volatility (+ pcap) | Memory + network correlation |

## Detecting Common Attack Patterns

### Port Scan Detection
```bash
# Many SYN packets from single source, no established connections
tshark -r capture.pcap -Y "tcp.flags.syn == 1 && tcp.flags.ack == 0" \
  -T fields -e ip.src -e ip.dst -e tcp.dstport | \
  sort | uniq -c | sort -rn | head -20
```

### ARP Spoofing Detection
```bash
# Multiple MAC addresses claiming same IP
tshark -r capture.pcap -Y "arp.opcode == 2" \
  -T fields -e arp.src.proto_ipv4 -e arp.src.hw_mac | \
  sort | uniq -c | sort -rn
# If same IP has multiple MACs → spoofing!
```

### DNS Exfiltration Detection
```bash
# Long DNS queries (possible tunneling)
tshark -r capture.pcap -Y "dns.flags.response == 0" \
  -T fields -e dns.qry.name | awk '{print length, $0}' | \
  sort -rn | head -20

# High query volume to single domain
tshark -r capture.pcap -Y "dns.flags.response == 0" \
  -T fields -e dns.qry.name | \
  awk -F. '{print $(NF-1)"."$NF}' | sort | uniq -c | sort -rn
```
