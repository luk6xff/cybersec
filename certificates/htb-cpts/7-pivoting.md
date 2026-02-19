# 7️⃣ Lateral Movement & Network Pivoting (Notes)

Goal: reach otherwise inaccessible networks/services, then enumerate them as if they were directly reachable.

## 1) Core concepts
- **Pivot host:** the compromised machine that has access to an internal network.
- **Route vs tunnel:**
  - *routing* makes your machine aware of internal subnets
  - *tunneling* forwards traffic through an established channel
- **Operational rule:** keep a stable control channel first (SSH/agent/beacon), *then* pivot.

## 2) Common techniques

### SSH port forwarding
- Local forwarding (expose an internal service on your box): `ssh -L local_port:internal_ip:internal_port user@pivot`
- Dynamic SOCKS proxy: `ssh -D 1080 user@pivot` (use with `proxychains`)

### Chisel (TCP tunneling)
- Useful when SSH is not available but outbound traffic is allowed.
- Pattern: run a server on attacker, client on pivot; forward ports or create SOCKS.

### Ligolo-ng (network pivot)
- Good for building “VPN-like” access through an agent + tunnel.
- Keep notes on:
  - which interface/subnet you’re trying to reach
  - routes you add/remove

## 3) Lateral movement checklist
- Enumerate from the pivot:
  - `ip a`, `ip r`, `arp -a`, DNS settings
- Identify internal targets:
  - AD/DCs, file servers, management interfaces
- Re-run the basics internally:
  - targeted port scan
  - service enumeration

## 4) Troubleshooting
- Can you reach the internal IP from the pivot at all?
- DNS vs IP: try both.
- Firewall direction: inbound to pivot vs outbound from pivot.
- Confirm the forwarded port is listening where you expect.

## 5) Evidence
- Document the tunnel setup commands and the reachable internal services.
