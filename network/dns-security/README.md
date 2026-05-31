# DNS Security

## DNS Attack Taxonomy

### 1. DNS Cache Poisoning (Kaminsky Attack)
Inject forged DNS responses into a resolver's cache, redirecting users to attacker-controlled servers.

```
Attacker                    Resolver                  Auth DNS
   │                           │                         │
   │ 1. Query: random.target.com                         │
   │──────────────────────────→│                         │
   │                           │──Query to auth DNS────→│
   │                           │                         │
   │ 2. Flood forged responses │                         │
   │   (spoofed source IP of   │                         │
   │    auth DNS, guessing TXID)│                        │
   │──────────────────────────→│                         │
   │                           │                         │
   │ If TXID matches before    │                         │
   │ real response arrives:    │                         │
   │   Cache poisoned! ✗       │                         │
   └───────────────────────────┘                         │
```

**Mitigations:**
- DNSSEC (cryptographic validation)
- Source port randomization (not just TXID)
- DNS-over-HTTPS (DoH) / DNS-over-TLS (DoT)
- Response Rate Limiting (RRL)

### 2. DNS Amplification DDoS
Abuse open resolvers to amplify traffic toward victim.

```bash
# Attack concept (DO NOT USE — educational only):
# Small query (~60 bytes) → Large response (~4000 bytes)
# Amplification factor: ~60x
# Attacker spoofs victim's IP as source

dig ANY isc.org @open-resolver   # ~4KB response for ~60B query
```

**Mitigations:**
- Block open resolvers (BCP38/BCP84)
- Response Rate Limiting on authoritative servers
- Ingress/egress filtering (prevent IP spoofing)

### 3. DNS Tunneling
Exfiltrate data or establish C2 channels by encoding data in DNS queries.

```bash
# Detection indicators:
# - Unusually long subdomain labels (>30 chars)
# - High volume of TXT/NULL/CNAME queries
# - Queries to recently registered domains
# - High entropy in subdomain strings

# Example tunneling tools:
# - iodine (IP-over-DNS)
# - dnscat2 (C2 over DNS)
# - DNSExfiltrator

# Detection query (Splunk/SIEM):
# index=dns query_length>50 | stats count by src_ip query
```

### 4. DNS Hijacking
Modify DNS records at registrar/resolver level to redirect traffic.

| Type | Vector | Impact |
|------|--------|--------|
| Registrar hijack | Compromised registrar account | Full domain takeover |
| Router DNS hijack | Compromised home/office router | Local network redirect |
| Rogue DNS server | DHCP poisoning | All DNS queries intercepted |
| BGP hijack of DNS | Route DNS prefix to attacker | Regional DNS takeover |

### 5. Subdomain Takeover
Claim an unclaimed resource pointed to by a CNAME record.

```bash
# Find dangling CNAMEs
dig CNAME app.target.com
# If returns: app.target.com CNAME app-target.herokuapp.com
# And that Heroku app is deleted → attacker can claim it!

# Tools:
# - subjack
# - can-i-take-over-xyz (GitHub knowledge base)
# - nuclei templates for subdomain takeover
```

## DNSSEC

### How It Works
```
Root Zone (signed with Root KSK)
  │
  └── .com (signed, DS record in root)
        │
        └── example.com (signed, DS record in .com)
              │
              ├── RRSIG (signature over A record)
              ├── DNSKEY (zone signing key)
              └── DS (hash of child's DNSKEY)
```

### Record Types
| Record | Purpose |
|--------|---------|
| RRSIG | Digital signature over an RRset |
| DNSKEY | Public key used to verify RRSIG |
| DS | Hash of child zone's DNSKEY (delegation) |
| NSEC/NSEC3 | Authenticated denial of existence |

### Validation with dig
```bash
# Check DNSSEC signatures
dig +dnssec example.com A
dig +sigchase example.com A

# Verify DS record chain
dig DS example.com @com-ns
dig DNSKEY example.com @ns1.example.com
```

## DNS Privacy

| Protocol | Port | Encryption | Standard |
|----------|------|-----------|----------|
| DNS (plain) | 53/UDP | None | RFC 1035 |
| DNS-over-TLS (DoT) | 853/TCP | TLS 1.3 | RFC 7858 |
| DNS-over-HTTPS (DoH) | 443/TCP | HTTPS | RFC 8484 |
| DNS-over-QUIC (DoQ) | 853/UDP | QUIC | RFC 9250 |
| Oblivious DoH (ODoH) | 443/TCP | HTTPS + proxy | RFC 9230 |

## DNS Hardening Checklist

- [ ] Enable DNSSEC signing on authoritative zones
- [ ] Deploy Response Rate Limiting (RRL)
- [ ] Disable recursion on authoritative servers
- [ ] Restrict zone transfers (AXFR) to secondaries only
- [ ] Monitor for DNS tunneling (query length, entropy)
- [ ] Use DoH/DoT for client privacy
- [ ] Implement RPZ (Response Policy Zones) for threat blocking
- [ ] Register common typo domains to prevent typosquatting
- [ ] Enable logging on resolvers for forensics
- [ ] Set appropriate TTLs (not too low = amplification, not too high = stale)
