# API Security Best Practices — Notes

## 🎯 Learning Outcomes

* Implement secure input validation
* Use correct HTTP semantics
* Protect APIs in transit
* Prevent abuse and detect attacks

---

## 🤔 Why it matters

Good design prevents vulnerabilities.
Good practices prevent exploitation.

> Design = architecture safety
> Best practices = operational safety

---

# 🧱 PART 1 — Request Validation & Handling

---

## 1) Restrict HTTP Methods

Create a **safe-list** of allowed methods.

Example:

```
Allowed: GET, POST
Blocked: DELETE, PUT, PATCH
```

Return:

```
405 Method Not Allowed
```

### Rule

> If you don’t need the method → block it

---

## 2) Validate Input

Never trust user input.

Validate:

* type
* length
* format
* range

Example rule:

```
length < 400 bytes
range 1–512
type boolean
```

Reject invalid input immediately.

### Best Practices

* Use strong typing
* Use allow-lists (not blocklists)

---

## 3) Validate Content Types

Allow only expected `Content-Type`.

Example safe-list:

```
application/json
image/jpeg
```

Reject with:

```
406 Not Acceptable
415 Unsupported Media Type
```

---

## 4) Use Libraries, Parsers & Logging

Do NOT write validation manually.

Use:

* validation libraries
* secure JSON/XML parsers

Log:

* validation failures
* abnormal input patterns

Why?
→ detects probing attacks

---

## 5) Send Safe Response Content Types

Check `Accept` header:

```
Accept: application/json
```

Reject unsupported formats.

Always return matching header:

```
Content-Type: application/json
```

Avoid JavaScript responses → header injection risk

---

## 6) Use Correct HTTP Status Codes

Do NOT always return `200` or `404`.

Examples:

| Code | Meaning             |
| ---- | ------------------- |
| 400  | Bad request         |
| 401  | Unauthorized        |
| 403  | Forbidden           |
| 405  | Method not allowed  |
| 415  | Unsupported media   |
| 429  | Too many requests   |
| 503  | Service unavailable |

### Rule

> HTTP codes communicate security state

---

## 7) Protect Management Endpoints

Never expose admin APIs publicly.

If unavoidable:

* firewall / ACL
* MFA required

Prefer:

```
private control network
```

---

# 🧱 PART 2 — Monitoring & Vulnerability Handling

---

## 8) Error Handling & Auditing

### Error Responses

Return generic messages:

```
Invalid credentials
```

NOT:

```
SQL error in auth_user table line 182
```

---

### Logging

Log before & after:

* authentication
* authorization
* token validation

Sanitize logs → prevent log injection

---

## 9) Detect Vulnerabilities (Dependencies)

Scan third-party libraries:

| Tool             | Language       |
| ---------------- | -------------- |
| Retire.js        | JavaScript     |
| Bundle-audit     | Ruby           |
| Safety           | Python         |
| Dependency-Check | Multi-language |

---

# 🧱 PART 3 — Transport Security

---

## 10) Enforce HTTPS & TLS

Rules:

```
Never allow HTTP
Use latest TLS version
```

---

## 11) Protect Sensitive Data in Requests

Never put secrets in URLs.

### Correct

POST/PUT → body or headers
GET → headers only

### Why

Proxies and logs store URLs.

Bad:

```
/api?apiKey=ABC123
```

Good:

```
Authorization: Bearer ABC123
```

---

## 12) Use Security Headers

Important headers:

```
Content-Type: application/json
X-Content-Type-Options: nosniff
X-Frame-Options: deny
Access-Control-Allow-Origin: trusted-domain
```

Purpose:

* prevent XSS
* prevent clickjacking
* control CORS access

---

# 🧱 PART 4 — Abuse Prevention

---

## 13) Quotas, Rate Limiting & Throttling

Prevent resource starvation.

Example:

```
60 requests/minute per user
```

Options:

* reject extra requests
* queue (throttle)

---

## 14) Filtering

Restrict who can call API:

* IP allowlist
* geo filtering
* block anonymous proxies

---

# 🧠 Summary Checklist

| Area       | Protection              |
| ---------- | ----------------------- |
| Input      | Validate everything     |
| Transport  | HTTPS + TLS             |
| Identity   | Secure headers & tokens |
| Monitoring | Logging & auditing      |
| Abuse      | Rate limiting           |
| Exposure   | Filtering               |

---

## Golden Rule

> Every API request is hostile until proven safe.

---

## Key Takeaways

* Never expose internal errors
* Always validate input & content type
* Enforce HTTPS + modern TLS
* Never put secrets in URLs
* Apply rate limiting and filtering
* Log everything security-related
