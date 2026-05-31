# IPv6 Security

## Why IPv6 Matters for Security

- IPv6 is often enabled by default but not monitored
- Many security tools and firewalls are IPv4-focused
- Dual-stack networks have twice the attack surface
- IPv6 introduces new protocols (NDP, SLAAC) with new attack vectors

## IPv6 vs IPv4 Security Differences

| Feature | IPv4 | IPv6 |
|---------|------|------|
| Address discovery | ARP | NDP (ICMPv6) |
| Auto-configuration | DHCP | SLAAC + DHCPv6 |
| Broadcast | Yes | No (multicast instead) |
| IPsec | Optional | Designed-in (still optional in practice) |
| Network scanning | Feasible (/24 = 254 hosts) | Impractical (/64 = 2^64 hosts) |
| NAT | Common | Not needed (end-to-end) |
| Fragment handling | Router + host | Host only |

## IPv6 Attack Vectors

### 1. Router Advertisement (RA) Spoofing
```
Attacker sends rogue Router Advertisements:
→ Victim configures attacker as default gateway
→ Man-in-the-middle achieved

Defense: RA Guard (switch feature), SEND (Secure NDP)
```

### 2. NDP Spoofing (IPv6 equivalent of ARP spoofing)
```bash
# Tool: parasite6, fake_router6 (THC-IPv6 toolkit)
# Attacker responds to Neighbor Solicitations with own MAC
# Redirects traffic through attacker

# Detection: Monitor for duplicate NA (Neighbor Advertisement) responses
# Mitigation: ND Inspection, SEND, static neighbor entries for critical hosts
```

### 3. SLAAC Attack
```
SLAAC (Stateless Address Autoconfiguration):
1. Host sends Router Solicitation
2. Router replies with prefix + gateway
3. Host auto-generates address (prefix + interface ID)

Attack: Rogue RA gives attacker-controlled prefix/gateway
→ All traffic routes through attacker
→ DNS can also be poisoned via RA options (RDNSS)
```

### 4. IPv6 Tunnel Exploitation
```bash
# 6to4, Teredo, ISATAP tunnels often bypass IPv4 firewalls
# IPv6 traffic encapsulated in IPv4 — invisible to IPv4-only IDS

# Detection: Block protocol 41 (6in4) at perimeter unless needed
# Block UDP 3544 (Teredo) unless explicitly required
```

### 5. Extension Header Abuse
```
IPv6 allows chained extension headers:
  Hop-by-Hop → Routing → Fragment → Auth → ESP → Destination

Attacks:
- Hide payload behind many extension headers (IDS evasion)
- Routing header type 0 (deprecated) allows source routing
- Fragment header for evasion (reassembly attacks)

Mitigation: Drop packets with excessive/unusual extension headers
```

## IPv6 Reconnaissance

```bash
# Unlike IPv4, you can't scan a /64 (18 quintillion addresses)
# Instead, use:

# 1. Multicast — ping all-nodes address
ping6 -c 2 ff02::1%eth0        # All link-local nodes respond

# 2. DNS enumeration — same as IPv4
dig AAAA target.com

# 3. IPv6 address patterns (many are predictable):
#    - EUI-64 (embeds MAC address)
#    - Low addresses (::1, ::2, etc.)
#    - Privacy extensions (random, temporary)

# 4. Passive discovery — monitor NDP traffic
# 5. Search engine/CT logs for AAAA records
```

## IPv6 Hardening

- [ ] Apply same firewall rules to IPv6 as IPv4 (don't leave IPv6 unfiltered!)
- [ ] Enable RA Guard on switches
- [ ] Disable IPv6 on interfaces where not needed
- [ ] Block IPv6 tunnel protocols at perimeter (6to4, Teredo, ISATAP)
- [ ] Use privacy extensions (RFC 4941) to prevent tracking
- [ ] Monitor ICMPv6 for anomalous behavior
- [ ] Implement DHCPv6 guard (prevent rogue DHCP servers)
- [ ] Filter unnecessary extension headers
- [ ] Include IPv6 addresses in SIEM/IDS monitoring
- [ ] Test security controls with IPv6-specific tools (THC-IPv6 toolkit)
