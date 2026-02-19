# API Attacks — Threat Landscape Notes

## 🎯 Learning Outcomes

* Recognize common API attack types
* Understand consequences of successful attacks

---

## 🤔 Why it matters

APIs are attractive targets because they:

* expose **structured data**
* allow **automation**
* lack UI protections (no CAPTCHA, human friction)

Many attacks exist in web apps —
but APIs amplify them through scale.

---

# 🧨 API Attack Categories

---

## 1) Data Breach Attacks (Scraping)

### Concept

Attacker repeatedly calls a public endpoint:

```
GET /transactions
GET /transactions?page=2
GET /transactions?page=3
...
```

They collect massive datasets into their own database.

---

### Goal

Harvest sensitive information about users or business operations.

---

### Consequences

* Millions of records leaked
* Reconnaissance for further attacks
* Privacy violations
* Regulatory penalties

---

## 2) Parameter Tampering

### Concept

Attacker modifies request parameters while they pass through the client.

Example:

```
price=999 → price=0
```

Occurs often when:

* client performs redirect to payment gateway
* two APIs trust client input

---

### Goal

Change business logic

---

### Consequences

* Free purchases
* Financial fraud
* Data corruption

---

## 3) Identity Attacks

### A) Credential Stuffing

Attacker reuses leaked credentials:

```
email/password from breach → API login attempts
```

Eventually succeeds.

---

### B) Broken Authorization

Attacker authenticates correctly but accesses other users' data:

```
/company/acme → /company/other-company
```

---

### Consequences

* Account takeover
* Data exposure
* Cross-tenant compromise

---

## 4) Machine-in-the-Middle (MITM)

### Concept

Attacker proxies traffic between user and API.

Steals:

```
session_id / token / cookies
```

Then impersonates the victim.

---

### Consequences

* Full account hijack
* Undetectable activity as victim

---

## 5) Functionality & Resource Abuse

Attacker misuses legitimate features.

### Examples

| Feature      | Abuse                  |
| ------------ | ---------------------- |
| Email API    | Spam relay             |
| Location API | Track users            |
| File upload  | Host malicious content |

---

### Consequences

* Privacy violations
* Blacklisting
* Reputation damage

---

## 6) Compute Farming

### Concept

Attacker triggers expensive operations repeatedly.

```
/generate-report
/render-video
/ai-processing
```

Cloud resources consumed:

* CPU
* RAM
* Storage

---

### Consequences

💸 Massive infrastructure bill

(Attacker profits, you pay)

---

## 7) DDoS Attacks

### Types

| Type       | Description           |
| ---------- | --------------------- |
| TCP Flood  | Network saturation    |
| HTTP Flood | Repeated API requests |

---

### Why APIs are vulnerable

* Long-lived connections
* Expensive requests
* Hard to distinguish bots
* No CAPTCHA (machine-to-machine)

---

### Consequences

* Service outage
* Legitimate users blocked
* SLA violations

---

# 🧠 Key Takeaways

| Attack              | Result                    |
| ------------------- | ------------------------- |
| Data scraping       | Massive data leak         |
| Parameter tampering | Fraud / free purchases    |
| Identity attacks    | Account takeover          |
| MITM                | Session hijacking         |
| Functionality abuse | Spam / tracking / hosting |
| Compute farming     | Financial loss            |
| DDoS                | Service unavailable       |

---

## Golden Rule

> APIs amplify attacks because they are fast, scriptable, and data-rich.

Security must assume:
**attackers automate everything**

---
