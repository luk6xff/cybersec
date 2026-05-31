# Software Bill of Materials (SBOM)

## Definition
An SBOM is a formal, machine-readable inventory of all software components, libraries, and dependencies that make up a piece of software — analogous to an ingredient list for food.

## Why SBOM Matters for Automotive

- **UNECE R155** requires tracking of software components for vulnerability management
- **ISO/SAE 21434** mandates monitoring of cybersecurity-relevant components post-production
- **Executive Order 14028** (US) requires SBOM for government suppliers
- **EU Cyber Resilience Act** mandates SBOM for all connected products

## SBOM Formats

| Format | Maintainer | Strengths |
|--------|-----------|-----------|
| **SPDX** | Linux Foundation | ISO standard (ISO/IEC 5962), license focus |
| **CycloneDX** | OWASP | Vulnerability + dependency focus, lightweight |
| **SWID** | ISO/NIST | Software identification tags, installed SW |

## Automotive SBOM Challenges

1. **Multi-tier supply chain**: OEM → Tier 1 → Tier 2 → OSS; each layer has its own SBOM
2. **Binary analysis**: Many ECU components delivered as binaries without source
3. **AUTOSAR classic**: Static configuration, less dynamic dependencies
4. **Linux-based ECUs**: Hundreds of OSS packages (Yocto/buildroot)
5. **Long lifecycle**: Must track vulnerabilities for 15+ years post-production

## SBOM Lifecycle in Automotive

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│   Build     │────→│   Delivery   │────→│  Production   │
│   System    │     │   to OEM     │     │  Monitoring   │
│             │     │              │     │               │
│ Generate    │     │ Merge SBOMs  │     │ CVE scanning  │
│ SBOM at CI  │     │ from Tier1/2 │     │ against SBOM  │
└─────────────┘     └──────────────┘     └───────────────┘
                                                │
                                         ┌──────▼──────┐
                                         │  Incident   │
                                         │  Response   │
                                         │             │
                                         │ Identify    │
                                         │ affected    │
                                         │ vehicles    │
                                         └─────────────┘
```

## Tools

| Tool | Purpose | Type |
|------|---------|------|
| Syft (Anchore) | Generate SBOM from container/binary | Open source |
| Trivy | Vulnerability scanning with SBOM | Open source |
| FOSSA | License compliance + SBOM | Commercial |
| Black Duck | Binary analysis + SBOM | Commercial |
| sw360 | SBOM management (Eclipse) | Open source |
| Yocto `create-spdx` | Generate SPDX from Yocto build | Built-in |

## Integration with Vulnerability Management

```
SBOM + NVD/CVE Database → Affected component list
                        → Risk assessment per vehicle model
                        → OTA patch prioritization
                        → Regulatory reporting (R155)
```

## Minimum SBOM Data Fields

| Field | Example | Purpose |
|-------|---------|---------|
| Component name | openssl | Identification |
| Version | 3.0.12 | Vulnerability matching |
| Supplier | OpenSSL Project | Responsibility |
| Hash/Checksum | SHA-256:a1b2... | Integrity verification |
| License | Apache-2.0 | Compliance |
| Relationship | depends-on, contains | Dependency graph |
| CPE/PURL | pkg:deb/openssl@3.0.12 | Machine-readable ID |
