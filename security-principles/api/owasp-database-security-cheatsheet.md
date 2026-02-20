# OWASP Database Security Cheat Sheet — Notes

## 🎯 Learning Outcomes

* Identify common database threats
* Apply OWASP database security best practices
* Secure database connectivity, accounts, and configuration

---

## 🤔 Why it matters

Databases store:

* credentials
* personal data
* financial records
* business secrets

A database breach often = **total compromise of the system**

> If the database is lost, the application is lost.

---

# 🧨 Common Database Threats

| Threat              | Description                   | Impact                   |
| ------------------- | ----------------------------- | ------------------------ |
| SQL Injection       | Malicious queries executed    | Full data compromise     |
| Malware             | DB accessed via infected host | Data theft               |
| Insider Threat      | Legitimate user misuse        | Silent exfiltration      |
| Social Engineering  | Credential theft              | Unauthorized access      |
| Weak Authentication | Guessable/shared credentials  | Account takeover         |
| Data Leakage        | Sensitive data exposure       | Compliance violation     |
| DoS                 | DB resource exhaustion        | Service outage           |
| Data Tampering      | Unauthorized modification     | Corrupted business logic |

---

# 🔌 Secure Database Connectivity

Goal → Only authorized systems should reach the database.

## Network Exposure Rules

| Practice                       | Purpose                     |
| ------------------------------ | --------------------------- |
| Disable TCP access if possible | Local-only access           |
| Bind to localhost              | Prevent remote connections  |
| Firewall allowlist             | Only app servers connect    |
| Separate network/DMZ           | Isolate DB from public tier |

> The safest database is the one nobody can directly reach.

---

# 🔐 Core Security Recommendations

## 1) Use TLS Encryption

Encrypt database traffic in transit.

### Requirements

* Enforce encrypted connections only
* Use modern ciphers (AES-GCM, ChaCha20)
* Validate certificates
* Prevent MITM attacks

```
Client ↔ TLS ↔ Database
```

---

## 2) Strong Database Authentication

### Rules

* Strong unique passwords
* Rotate credentials
* One account per service
* Never shared accounts

Bad:

```
app, admin, analytics → same DB user
```

Good:

```
app_user
report_user
migration_user
```

---

## 3) Enforce Least Privilege

Every account gets only what it needs.

### DO

* restrict host access
* restrict database access
* restrict table access
* restrict query type

### DON’T

* use root/admin accounts
* grant global privileges
* allow cross-database links

Example:

```
app_user → SELECT, INSERT only
admin → maintenance only
```

---

# 🛡 Permission Management

## Principle: Least Privilege

| Action       | Risk if allowed      |
| ------------ | -------------------- |
| DROP TABLE   | Data destruction     |
| ALTER SCHEMA | Privilege escalation |
| CREATE USER  | Backdoor accounts    |
| EXECUTE OS   | Server compromise    |

Separate environments:

```
dev ≠ staging ≠ production
```

---

# 🧱 Harden Database Configuration

## Patch & Updates

* install security updates
* patch DB and OS

## Accounts

* remove default accounts
* disable test databases

## Runtime Security

* run DB under low-privileged OS user
* no root/system service

## Storage Safety

* transaction logs on separate disk
* protects integrity & recovery

## Backups

* scheduled backups
* offline/immutable copies
* tested restoration

> Backup not tested = backup does not exist

---

# 🧠 Additional Good Practices (Practical Extensions)

## Secrets Handling

Never store DB passwords in:

* source code
* config files
* containers

Use:

* secret managers
* environment injection
* vault systems

---

## Monitoring & Auditing

Log:

* login attempts
* privilege changes
* schema changes
* mass reads

Detect:

* unusual queries
* data exfiltration patterns

---

## Data Protection

* encrypt sensitive columns
* hash passwords (never reversible)
* tokenize sensitive identifiers

---

# 🧠 Summary Checklist

| Area          | Protection            |
| ------------- | --------------------- |
| Network       | restrict connectivity |
| Transport     | TLS encryption        |
| Identity      | unique DB accounts    |
| Authorization | least privilege       |
| Configuration | hardened DB           |
| Monitoring    | audit logs            |
| Data          | encryption & backups  |

---

## Golden Rule

> Application security fails fast — database security fails catastrophically.

---

## Key Takeaways

* Never use root DB accounts in applications
* Encrypt DB connections (TLS only)
* Limit permissions aggressively
* Harden DB configuration and remove defaults
* Monitor activity and maintain tested backups

