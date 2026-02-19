# OWASP REST Security Cheat Sheet — Notes

## 🎯 Learning Outcomes

* Understand OWASP best practices for securing REST APIs
* Explain and apply the practices in real API designs

---

## 🤔 Why it matters

REST APIs often handle **sensitive data** and power key business workflows. Securing them helps:

* prevent unauthorized access and data leaks
* maintain integrity and reliability
* support regulatory compliance
* build user trust

---

# ✅ OWASP REST Security Best Practices

## 1) Implement Access Control

* **Non-public APIs** must enforce access control **at every endpoint**
* Authorization decisions should be made **locally** at the service/endpoint (helps reduce latency and keeps policy enforcement close to the resource)
* **Centralize authentication** in an **Identity Provider (IdP)**

  * IdP issues **access tokens**
  * Services validate tokens + permissions before serving requests

**Rule:** Every endpoint must verify **authn + authz**, not just the gateway.

---

## 2) Restrict HTTP Methods

* Use an **allow-list** of permitted HTTP methods per endpoint
* If a method isn’t allowed, return:

  * **`405 Method Not Allowed`**
* Also ensure access control allows that method (e.g., RBAC)

**Goal:** Reduce attack surface (e.g., block `DELETE` if you don’t support it).

---

## 3) Use Appropriate Status Codes

* HTTP status codes communicate outcomes clearly and safely
* Avoid patterns like:

  * “always 200” for everything
  * “always 404” for any error

**Rule:** Always return the **semantically correct** status code for success/failure conditions.

---

## 4) Secure with TLS (HTTPS)

* Use **HTTPS/TLS** to protect data in transit:

  * confidentiality (encryption)
  * integrity (MACs)
  * server/client identity (certificates)
* TLS handshake negotiates:

  * encryption algorithm
  * key exchange
  * message authentication method

**Rule:** No TLS → assume traffic can be read/modified.

---

## 5) Perform Input Validation

Define and enforce constraints for every input:

* **expected inputs** (schema/contract)
* **length and range**
* **data type**
* **format**
* **sanitization** (remove dangerous characters/patterns)

Example: `POST /users`

* body must be JSON
* `username` is string
* max length = 20

**Rule:** Treat all incoming input as **untrusted**—validate + sanitize before use.

---

## 6) Authentication

Common models: basic auth, token-based auth.

Typical flow:

1. Client sends credentials in `Authorization` header
2. API validates credentials (DB lookup or signature verification)
3. API issues token/session for future calls
4. API checks token/session validity on each request (expiry matters)
5. If invalid/expired → return appropriate error and require re-auth

**Rule:** Tokens/sessions must be **stored securely** and **expire**.

---

## 7) Implement Authorization

Authorization happens after authentication:

* decide whether user can **read/create/update/delete** a resource

Common approaches:

* **RBAC** (Role-Based Access Control): simple roles → permissions
* **ABAC** (Attribute-Based Access Control): policies based on user/resource/context attributes (department, job title, etc.)

**Rule:** Enforce authorization at the **resource level**, not just at login.

---

## 8) Error Handling

Goals:

* consistency for clients
* reduce information leakage to attackers

Best practices:

* **Generic error responses** (don’t leak internals)
* Include **guidance** for resolution (docs/instructions)
* Put extra metadata in **response headers** when useful
* Never expose sensitive details (e.g., call stacks, “username exists”, etc.)

**Rule:** Errors should help the legit client—without helping the attacker.

---

## 9) Audit Logs

Audit logging is essential for detection and response.

Log:

* before/after security events (authn, authz, validation)
* validation and token errors (useful attack signals)
* sanitize log input to prevent **log injection**
* store logs securely

**Rule:** If it’s security-relevant, it should be auditable and searchable.

---

# 🧠 Key Takeaways

* Enforce access control **on every endpoint**
* Allow-list HTTP methods; return **405** for disallowed ones
* Use correct status codes (don’t overuse 200/404)
* Always use **TLS**
* Validate + sanitize all input
* Implement strong authn + authz (RBAC/ABAC)
* Use consistent, non-leaky error handling with helpful guidance
* Write audit logs around security events and sanitize logs to prevent injection
