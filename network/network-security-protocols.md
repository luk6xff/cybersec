# Netwok Security Protocols

## Application Layer

### Core Concepts
- **Protocols operate at specific OSI or TCP/IP layers** and follow the functionality defined at that layer.
- **TCP and UDP-based protocols use specific network ports**. Understanding port assignments is crucial for firewall configurations, intrusion detection, and monitoring.

### HTTPS (HTTP Secure)
- **Purpose:** Encrypts HTTP communications using SSL/TLS.
- **Port:** Default TCP port 443.
- **Security Benefit:** Protects against eavesdropping and data tampering.
- **Key Mechanism:** Combines asymmetric (public key) and symmetric encryption to ensure confidentiality and integrity.

### FTPS (FTP Secure)
- **Purpose:** Secure extension of FTP for file transfers.
- **Ports:**
  - FTP/Explicit FTPS: 21
  - Implicit FTPS: 990
  - FTP data port (active mode): 20
- **Modes:**
  - **Active Mode:** Server initiates the data connection to the client.
  - **Passive Mode:** Client initiates both control and data connections, suitable when the client is behind a firewall.
- **Data Types:** ASCII, Binary (Image), EBCDIC, and Local.
- **Security Benefit:** Protects login credentials and data transfers from being intercepted in cleartext.

### SMTPS (SMTP Secure)
- **Purpose:** Secure extension of SMTP for sending emails.
- **Ports:** 465 or 587 for SMTPS.
- **Encryption:** Uses TLS/SSL (STARTTLS command) to encrypt emails.
- **Benefit:** Prevents sniffing of login details and email content, and reduces spam/phishing by verifying authenticity of sender domains.

### POP3S (POP3 Secure)
- **Purpose:** Secure version of POP3 for retrieving emails from the server to the client.
- **Port:** 995 for POP3S (vs. 110 for POP3).
- **Encryption:** Uses TLS/SSL (STARTTLS command) to encrypt both login credentials and email data in transit.
- **Benefit:** Prevents attackers from intercepting usernames, passwords, and email content.

```markdown
## Key Points for a Cybersecurity Engineer (Updated with OpenPGP Examples)

### DNSSEC
- **Purpose:** Ensures DNS responses are authentic and haven’t been tampered with.
- **Mechanism:**
  - DNS zone owners sign all DNS records with a private key.
  - Public keys are published so clients can verify the authenticity of the DNS records.
- **Benefits:**
  - **Authenticity:** Confirms the DNS record is from the correct owner.
  - **Integrity:** Guarantees records haven’t been altered in transit.

### OpenPGP (GnuPG)
- **Purpose:** Provides end-to-end encryption and signing for emails, files, and other data transfers.
- **Encryption Model:** Uses asymmetric cryptography (public/private keys).
- **Key Benefits:**
  - **Confidentiality:** Only intended recipients (who have the corresponding private key) can read the content.
  - **Integrity & Authenticity:** Digital signatures ensure messages are not altered and confirm the sender’s identity.

#### Practical Usage with GnuPG (gpg)

**1. Installing GnuPG**
On most Linux distributions:
```bash
sudo apt-get update && sudo apt-get install gnupg -y
```

**2. Generating a Key Pair**
GnuPG will guide you through selecting a key type, key size, and setting an expiry:
```bash
gpg --gen-key
```
- You’ll be prompted for your name, email, and a passphrase.
- After completion, this command creates a key pair (a private key and a public key) stored in `~/.gnupg/`.

**3. Listing Your Keys**
To see a list of your public keys:
```bash
gpg --list-keys
```
To list your secret (private) keys:
```bash
gpg --list-secret-keys
```

**4. Exporting Your Public Key**
You’ll need to share your public key with anyone who needs to send you encrypted data:
```bash
gpg --armor --export your_email@example.com > public_key.asc
```
- This creates an ASCII-armored public key file named `public_key.asc`.

**5. Importing Someone’s Public Key**
When you receive someone else’s public key, import it:
```bash
gpg --import their_public_key.asc
```

**6. Encrypting a File for a Specific Recipient**
Use the `-r` option with the recipient’s email (associated with their public key):
```bash
gpg --encrypt --sign --armor -r recipient@example.com file_to_encrypt.txt
```
- `--encrypt` encrypts the file using the recipient’s public key.
- `--sign` signs the file with your private key, ensuring authenticity.
- `--armor` outputs ASCII text instead of binary.
- The result is `file_to_encrypt.txt.asc`, which you can safely send to the recipient.

**7. Decrypting a File You Received**
To decrypt a file you have received and for which you have the private key:
```bash
gpg --decrypt file_to_decrypt.txt.asc > decrypted_file.txt
```
- If the file was also signed, GnuPG will automatically verify the signature and inform you if it’s valid.

**8. Verifying a Signed File**
If you receive a signed file (not necessarily encrypted), you can verify its authenticity:
```bash
gpg --verify signed_file.asc
```

With these steps, you have the basic tooling to create keys, encrypt/decrypt data, sign files, and verify signatures using GnuPG in a Bash environment.

### SSH
- **Purpose:** A secure protocol for remote system administration, shell access, and file transfers.
- **Security Improvements Over Telnet:**
  - **Encryption:** Prevents eavesdropping on credentials and commands.
  - **Integrity:** Ensures commands and data are not altered in transit.
- **Key Features:**
  - Uses asymmetric keys for authentication (optional, but recommended).
  - Protects against man-in-the-middle attacks by verifying server host keys.

