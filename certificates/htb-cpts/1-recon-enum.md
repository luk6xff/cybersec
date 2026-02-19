# 1️⃣ Reconnaissance & Enumeration (Checklist)

Goal: build a reliable picture of the target surface area, then enumerate only what’s real.

## 0) Before touching the target
- Confirm scope, allowed attack types, and any out-of-scope ranges.
- Set up a notes structure per host: `IP/FQDN → open ports → services → creds → findings → proof`.
- Start a log/command transcript early (tmux logging helps).

## 1) Host discovery & target list
- Identify live hosts and *confirm reachability* (ICMP may be blocked).
- Maintain a single source of truth: `targets.txt` and `alive.txt`.

**Common patterns**
- ICMP blocked? Use TCP ping-style discovery (e.g., probing 80/443/445/3389) and confirm via ARP/ND when local.

## 2) Port scanning strategy
Use a two-phase approach:
1. **Fast, broad scan** to discover ports.
2. **Focused service scan** with version detection + safe scripts.

Tips:
- Prefer `-oA` output and keep scans named per host.
- Avoid `-A` unless you need it (noisy, can be slow).

## 3) Service fingerprinting & “what next”
Once you have ports, decide the next enumeration step per service.

### Web (HTTP/HTTPS)
- Identify stack: server header, technologies, redirects, WAF hints.
- Enumerate:
  - virtual hosts (Host header), subpaths, parameters, auth boundaries
  - file upload points
  - admin panels and API docs (Swagger/OpenAPI)
- Capture:
  - screenshots of key pages
  - response headers and cookies

### SMB (445)
- Shares, null sessions, domain/host role, signing, SMB versions.
- If creds exist: list shares, read access, local admin, lateral potential.

### DNS (53)
- Attempt zone transfer (rare, but quick to check).
- Enumerate records: MX, TXT, SRV, internal naming conventions.

### FTP (21)
- Anonymous access?
- Writable directories?
- Banner and TLS configuration.

### RDP/WinRM/SSH
- Validate which accounts can log in.
- Prioritize stable shells over fragile command exec.

## 4) “Enumeration checklist” per host
For each host, ensure you’ve answered:
- What is it (OS/role)?
- What services are *actually reachable*?
- What’s the easiest auth boundary to break?
- What data is exposed without auth?
- What’s the pivot value (subnets, trust, credentials, tokens)?

## 5) Evidence & reporting hygiene
- Save outputs (`nmap`, screenshots, configs) under a per-host folder.
- Record the exact command that produced each finding.

## Quick links
- Nmap commands: see the [Nmap section](README.md#nmap)
- Service enumeration commands: see [Footprinting Services](README.md#footprinting-services)
