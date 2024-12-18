Network Device Hardening
===
Based on: https://tryhackme.com/r/room/networkdevicehardening


## Common Threats and Attack Vectors of Network Devices
Below is a Markdown table based on the given information:

| Threat                       | Description                                                                                                                                                                      | Attack Vector                                                                                                                                                                                                                                                    |
|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Unauthorised access          | Gain unauthorised control of a network device, and then the complete network.                                                                                                     | - Password attacks (brute force, dictionary & hybrid)<br>- Exploit known vulnerabilities (e.g. RCE)<br>- Social Engineering/Phishing attacks to trick network administrators into disclosing sensitive information such as usernames and passwords of devices |
| Denial of Service (DoS)      | Disruption of critical devices and services to make them unavailable to genuine users.                                                                                           | - Flooding devices with fake requests<br>- Exploiting vulnerabilities in logical or resource handling<br>- Manipulating network packets                                                                                                                        |
| Man-in-the-Middle Attacks    | Intercept the network requests between two parties by masquerading as each other to steal sensitive information or alter/manipulate the requests.                                 | - ARP spoofing<br>- DNS spoofing<br>- Rogue access points                                                                                                                                                                  |
| Privilege escalation          | Gaining higher-level privileges or rights to perform restricted actions, e.g. accessing sensitive information or executing malicious code.                                        | - Weak passwords or use of the same passwords for user and admin accounts<br>- Exploiting vulnerabilities<br>- Misconfigurations                                                                                                                                |
| Bandwidth theft/ hotlinking  | Linking a bandwidth-intensive resource (image or video) from an external website to its original website, without permission. This can cause increased traffic to the original website. | - Scraping large volumes of data<br>- DoS attacks<br>- Malware attacks                                                                                                                                                     |


## Common Hardening Techniques
### General Techniques

Hardening techniques are meant to reduce the attack surface of a system or network by removing unnecessary functionality, limiting access, and implementing various security controls. Some standard methods are mentioned below:

**Updating & Patching:**
Ensuring the latest version of the Operating System and underlying applications of all devices and systems and installing regular security patches is the core hardening measure. Outdated OS and applications contain vulnerabilities that attackers can exploit.

**Disabling unnecessary services & ports:**
Turn off all unnecessary services and block all ports (physical and virtual) that are not needed for system functionality. This reduces the attack surface by minimizing the number of entry points an attacker can exploit.

**Principle of Least Privilege (POLP):**
Restrict users and processes to only the minimum necessary permissions required to perform their functions.

**Logs Monitoring:**
Implement a log monitoring system to detect unusual activity or security events.

**Backup regularly:**
Take routine backups of systems and configurations to facilitate recovery from a security incident or system failure.

**Enforcing Strong Passwords:**
Change default login passwords and use strong passwords that are at least ten characters long, containing a combination of lowercase letters, uppercase letters, special characters, and numbers. This protects against dictionary and brute-force attacks.

**Multi-Factor Authentication (MFA):**
MFA is an additional security layer requiring two or more types of identification before accessing the account or system. Typically, this involves something you know (like a password) and something you have (like a biometric factor).

### Importance of Secure Protocols

Secure protocols play a critical role in network device hardening by protecting against unauthorized access and data breaches. They ensure that sensitive data transmitted between devices is encrypted and cannot be intercepted by malicious actors. Moreover, secure protocols also help prevent man-in-the-middle attacks and other network-based exploits. By using secure protocols, network administrators can ensure that only authorized personnel can access sensitive information and perform system administration tasks.
Common secure protocols include **HTTPS**, **SSH**, **SSL/TLS**, and **IPsec**. You can learn more about secure network protocols in this room.

### Removal/Blocking of Insecure Protocols

In addition to using secure protocols, removing and blocking access to insecure protocols is equally essential as it decreases an attacker’s potential attack surface. Especially critical are protocols that transmit data in clear text without encryption, such as **FTP**, **HTTP**, **Telnet**, **SMTP**, and more. Even inherently secure protocols (e.g., **LDAP**, **RDP**, **SIPS**) can be exploited if configured incorrectly, so proper configuration and management are key.

### Implementation of Monitoring and Logging Controls

Logging in network devices is essential for detecting and investigating security incidents, identifying performance issues, and complying with regulatory requirements. It provides a record of events and activities on the device, which can be used for troubleshooting, forensic analysis, and auditing purposes. The following techniques are generally used for logging:

- **Syslog:** A protocol to standardize the transfer of log messages to a central server for storage and analysis.
- **SNMP:** Uses traps (notifications) sent by a network device to a management system when a predefined event occurs.
- **NetFlow:** A protocol used to collect and analyze network traffic data for monitoring and security analysis.
- **Packet Captures:** Capturing network traffic and storing it for analysis using a tool like Wireshark.



## Hardening Virtual Private Networks
- **Use strong encryption algorithm:** Configure the VPN gateway to use strong encryption to protect data in transit. The cipher directive in the config file can be used to select the encryption scheme. The possible options for cipher include AES, Blowfish, Camellia, and more. For example, AES-128-CBC mode means to use the AES encryption algorithm with a key size of 128-bit in Cipher Block Chaining (CBC) mode, as seen below. AES-256-CBC is typically considered one of the strongest cipher encryption nowadays.

- **Keep VPN gateway software up-to-date:** Ensure that the VPN gateway software is always updated with the latest security patches and updates. Every VPN software has a different method for it.


- **Implement strong authentication:** Use strong authentication mechanisms such as a combination of Transport Layer Security (TLS) and a secure hashing algorithm. We can use the auth directive to specify the exact algorithm in the OpenVPN configuration file to ensure that a secure hashing algorithm will be used for packet authentication. Some of the options for auth directive are SHA1, SHA128, SHA256, SHA512 and MD5. You can set the auth directive through the following command:

- **Change default settings:** Change the default usernames and passwords to something unique to reduce the risk of unauthorised access to the VPN gateway.

- **Enable Perfect Forward Secrecy (PFS):** Perfect Forward Secrecy (PFS) in OpenVPN generates unique session keys for each session to strengthen the security of the VPN connection. Because of this, even if a hacker successfully obtained a session key, they could not use it to decode more sessions. For each session, PFS generates a new set of encryption keys, preventing the possibility of remotely decrypting previously acquired material. As a result, it is far more challenging for an attacker to spoof the VPN connection and steal sensitive data. We can use the tls-crypt directive in the OpenVPN configuration file to enable PFS. The tls-crypt directive requires a key that can be generated using the command sudo openvpn --genkey --secret my.key and should be placed in the same directory on the server. Choosing the appropriate cipher and auth, like cipher AES-256-CBC and auth SHA 256, supports PFS if combined with tls-crypt



## Hardening Routers, Switches & Firewalls
- Setting up the device: While setting up any network device, it is necessary to fill in all relevant details like hostname, timezone, logging, and more. These features assist in conducting incident handling in case of a compromise. For example, logging must be enabled to log all the events with the default alert level Debug. Similarly, timezone and time synchronisation must be set accurately to properly correlate events with their occurrence time.

- Change default credentials: Usually, the admin web interface is protected through a username and password, and people tend to ignore changing the default. A threat actor can access the router's admin interface and compromise the whole network using default credentials.

- Enable secure network protocols:  For a network device to maintain the confidentiality, integrity, and availability of network traffic, secure protocols must be enabled. Secure protocols like HTTPS, SSH, and SSL/TLS offer encrypted authentication mechanisms and communications to stop unauthorised access and eavesdropping. By enabling secure protocols on a router, you can reduce the risk of data breaches, man-in-the-middle attacks, and other security threats.

- Disabling unnecessary scripts: Almost every network device executes some startup scripts to provide a better user experience to a user. For example, crontab is executed on startup to verify and execute any cron job. Threat actors try to gain persistent access on a network device by adding their malicious scripts on the startup.

- Securing Wi-Fi: If the router has Wi-Fi capabilities, securing the Wi-Fi by enabling strong encryption like WPA2/WPA3, disabling SSID broadcast, changing default passwords, and more.

- Manage traffic rules: Network devices allow you to create and implement traffic rules that accept/deny network traffic. For example, we notice that the data of users connected with our network device is being exfiltrated to a command and control server IP address. We can create a rule to block all traffic where the destination IP matches the attacker's command and control server

- Monitor traffic: As a network administrator, keeping track of network traffic, like uploads and downloads of data at different intervals, is essential. For example, you have excessive data uploaded from one of the email servers to an unknown IP address. Such alerts enable you to take remedial measures and stop data pilferage timely. Usually, network devices provide real-time graphs to monitor the traffic.

- Configuring port forwarding: A firewall's port forwarding capability enables inbound traffic from the internet or other sources to be routed to a particular device or service on the internal network. The firewall can send incoming traffic to the appropriate device or service on the internal network by establishing port forwarding rules while blocking any other incoming traffic that does not comply with the rules. This feature helps host applications that need outside access, granting remote control of internal devices. Port forwarding should be used carefully because it can expose internal devices and services to potential security issues if improperly secured and configured. Threat actors could add new rules here for creating connections to external command and control servers.

- Monitoring scheduled tasks: It is important to monitor scheduled tasks to confirm that the original scheduled tasks lists are not modified by a threat actor

- Update firmware: It is essential to update the firmware and installed packages on a regular basis to avoid any know/unknown attacks.

- Configuring port security: This includes limiting the number of MAC addresses registered on a switch port and taking particular action whenever unauthorised access is detected. Enabling port security enables an administrator that data is coming from a valid source and will be forwarded to a legitimate receiver.

- Preventing ARP spoofing: ARP spoofing is one of the most common vectors for launching man-in-the-middle attacks on the network. The threat can be mitigated by enabling static ARP tables and implementing MAC address filtering. You can learn more about mitigating ARP spoofing here.

- Preventing rogue DHCP servers: The attacker creates a spoofed DHCP server that can be later on used for assigning IPs to clients and launching MITM attacks. Mitigation measures to prevent such attacks include configuring static DHCP binding and ensuring no unknown devices are added to a network through network mapping tools. You can learn more about DHCP here.

- Enabling IPv6: Unlike IPv4, IPv6 has built-in support of IPsec that can be used to secure network communication and provide confidentiality, integrity, and authenticity. Moreover, this will help in protection against MITM, eavesdropping, and tampering of packets in transit.
