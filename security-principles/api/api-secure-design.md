# API Secure Design Principles — Notes

## 🎯 Learning Outcomes

* Understand the impact of security on system design
* Apply the **6 API Secure Design Principles**

---

## 🤔 Why it matters

Security must be designed **before implementation**.

If added later:

* expensive rewrites
* hidden vulnerabilities
* fragile architecture

> Build secure → not secure later

---

## 🧠 Core Philosophy — Gall’s Law

> A complex system that works evolved from a simple system that worked.

Implication for APIs:

* Complex + secure = extremely hard
* Simple + secure = maintainable

**Simplicity is a security feature**

---

# 🔐 The 6 API Secure Design Principles

---

## 1) Keep Security Simple

### Goals

* Simple = understandable
* Understandable = fixable
* Fixable = secure

### Best Practices

* Use industry standards (OAuth2, JWT, TLS, mTLS)
* Avoid custom crypto / auth
* Secure by default
* Warn when security settings are weakened

### Rule

> Never invent your own security

---

## 2) Use API Versioning

Example:

```
/api/v1/users
/api/v2/users
```

### Benefits

* Faster iteration
* Introduce stronger security
* Backward compatibility
* Clean deprecation

### Important

Old versions must expire:

```
v1 → deprecated → removed
```

---

## 3) Enforce Least Privilege

Give users **only what they need**

### Techniques

* RBAC roles
* Separate read vs write API keys
* Scoped tokens

Example:

```
read_key → GET only
write_key → POST/PUT
admin → all
```

### Rule

> If access is not required → deny it

---

## 4) Minimize Data Collection

Collect only necessary data.

### Why

More data = more liability

### Practices

* Document why each field exists
* Record user consent
* Reject unnecessary input

---

## 5) Limit Data Exposure

Store and return minimal data.

### Risks

* Hidden fields in JSON
* Database correlation leaks
* PII reconstruction

### Practices

* Return only required fields
* Avoid sending internal objects directly
* Prevent accidental sensitive data leaks

---

## 6) Log Requests & Responses

Every request must be traceable.

### Use `request_id`

Unique per request:

```
request_id = crypto_hash(request_properties)
```

### Why

* Incident investigation
* Debugging
* Forensics
* Correlation across services

---

# 🧠 Summary Checklist

| Principle           | Purpose              |
| ------------------- | -------------------- |
| Keep it simple      | Reduce mistakes      |
| Version APIs        | Safe evolution       |
| Least privilege     | Prevent misuse       |
| Minimize collection | Reduce liability     |
| Limit exposure      | Prevent leaks        |
| Log everything      | Enable investigation |

---

## Golden Rule

> Secure architecture prevents vulnerabilities better than security patches.

---

## Key Takeaways

* Simple systems are safer systems
* Version APIs and deprecate old ones
* Grant minimal permissions
* Collect and expose minimal data
* Always log with a unique request_id
