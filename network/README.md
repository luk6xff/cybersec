# Network Security

## Structure

```
network/
├── network-device-hardening.md      — Router, switch, firewall hardening
├── network-security-protocols.md    — HTTPS, FTPS, DNSSEC, PGP
├── secure-network-architecture.md   — VLANs, security zones, segmentation
├── tls-mtls-overview.md             — TLS 1.2/1.3 handshake, mTLS
├── dns-security/                    — DNS attacks & defenses
│   └── README.md
├── wireless-security/               — 802.11, WPA3, attacks
│   └── README.md
├── ids-ips-evasion/                 — IDS/IPS concepts & bypass
│   └── README.md
├── traffic-analysis/                — Wireshark, protocol analysis, forensics
│   └── README.md
├── firewall-architecture/           — Types, rules, bypass techniques
│   └── README.md
└── ipv6-security/                   — IPv6 threats & mitigations
    └── README.md
```

## Quick Reference — Ports to Know

| Port | Service | Security Notes |
|------|---------|---------------|
| 21 | FTP | Cleartext creds — use SFTP/FTPS |
| 22 | SSH | Key-based auth, disable password login |
| 23 | Telnet | Cleartext — never use in production |
| 25 | SMTP | STARTTLS mandatory, SPF/DKIM/DMARC |
| 53 | DNS | DNSSEC, DoH/DoT for privacy |
| 80 | HTTP | Redirect to 443 |
| 88 | Kerberos | AD authentication |
| 110 | POP3 | Use POP3S (995) |
| 135 | MSRPC | Windows RPC — restrict access |
| 139/445 | SMB | Disable SMBv1, require signing |
| 389/636 | LDAP/S | Use LDAPS, disable anonymous bind |
| 443 | HTTPS | TLS 1.3, HSTS, certificate pinning |
| 993 | IMAPS | Encrypted email retrieval |
| 1433 | MSSQL | Never expose externally |
| 3306 | MySQL | Never expose externally |
| 3389 | RDP | NLA enabled, MFA, VPN only |
| 5432 | PostgreSQL | Never expose externally |
| 5985/5986 | WinRM | Restrict to admin networks |
| 8080 | HTTP-Alt | Common for proxies/dev servers |
