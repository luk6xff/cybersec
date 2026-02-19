# API Authentication & Authorization — Notes

## 🎯 Learning Outcomes

* Apply best practices for authentication and authorization in APIs
* Choose the best authentication method
* Choose the appropriate authorization model

---

## 🤔 Why it matters

* **Authentication → WHO can access**
* **Authorization → WHAT they can do**

A secure API must implement **both**, otherwise endpoints become vulnerable.

---

# 🔐 Authentication

We cover three common approaches:

1. API Keys
2. X.509 Client Certificates
3. JSON Web Tokens (JWT)

---

## 1) API Keys

### Concept

A client receives a secret key and sends it in every request (usually header).

Like a house key:

> Whoever has it = becomes you.

### When to use

* Simple service-to-service APIs
* Backend platforms able to securely store secrets

---

### Risks

If leaked → attacker gains full access to your API.

---

### Requirements / Best Practices

* Require key for **every request**
* Use **MFA for sensitive operations**
* Rate limit → `429 Too Many Requests`
* Allow multiple keys per client
* Support expiration
* Support revocation
* Do NOT rely on keys alone for high-value operations

---

### Storage

#### Server side

Never store plaintext keys.

Store:

```
hash = PBKDF2(api_key)
```

On request:

```
hash(incoming_key) == stored_hash
```

#### Client side secure storage options

* Hardware Security Module (HSM)
* Virtual HSM
* AWS KMS
* Azure Key Vault
* HashiCorp Vault

Never store in:

* config files
* source code
* git repositories

---

## 2) X.509 Client Certificates (mTLS)

### Concept

Client authenticates using a cryptographic certificate.

Server validates:

* Expiration
* Revocation
* Match with trusted CA

### When to use

* High-value clients
* B2B integrations
* Strong identity assurance
* Small number of consumers

### Advantage

Strongest identity proof — possession of private key required.

---

## 3) JSON Web Token (JWT)

### Concept

User logs in → server creates token → client reuses token.

```
username/password → server → JWT → client
client → JWT → API (every request)
```

JWT connects authentication AND authorization.

---

### Structure

```
HEADER
PAYLOAD
SIGNATURE
```

Example:

```json
Header:
{ "typ": "JWT", "alg": "HS256" }

Payload:
{ "iss": "chris", "exp": 1596318193 }

Signature:
HMACSHA256(base64(header)+"."+base64(payload), secret)
```

Signature prevents modification.

---

### When to use

* OAuth 2.0 / identity providers
* Stateless sessions
* Scalable architectures

---

### JWT Validation Rules

Reject if:

* `alg = none`
* Signature invalid
* Expired
* Not yet valid
* On revocation list

Verify standard claims:

| Claim | Meaning           |
| ----- | ----------------- |
| `iss` | Trusted issuer    |
| `aud` | Intended audience |
| `exp` | Expiration time   |
| `nbf` | Not valid before  |

Use a **revocation list (blocklist)** for compromised tokens.

---

# 🔑 Authorization

Authorization must exist **per endpoint**.

Example endpoints:

```
/api/v1/login
/api/v1/me
/api/v1/{user-id}/media
/api/v1/comment
```

---

## RBAC — Role Based Access Control

Users have roles:

* NonAuthenticatedUser
* AuthenticatedUser
* Admin

Access decision:

```
ROLE → allowed endpoints
```

Example:

| Role  | Access        |
| ----- | ------------- |
| Guest | login only    |
| User  | own resources |
| Admin | all           |

✔ Simple
✔ Easy to reason about
❌ Rigid

---

## ABAC — Attribute Based Access Control

Decisions based on attributes:

Possible attributes:

* IP address
* Country (GeoIP)
* API key validity
* User agent
* VPN usage
* Request sensitivity
* Time of day
* Rate limit

Example policy:

```
Allow IF
API_KEY valid
AND IP in 192.168.0.0/24
AND Country = Nauru
AND time 09:00–17:00
```

✔ Extremely flexible
✔ Context aware
❌ More complex

---

# 🧠 Key Takeaways

### Authentication

| Method       | Best Use Case                |
| ------------ | ---------------------------- |
| API Keys     | Simple service integrations  |
| Client Certs | High-trust clients           |
| JWT          | Scalable web / OAuth systems |

---

### Security Rules

* Hash API keys (PBKDF2)
* Validate JWT strictly
* Use revocation mechanisms
* Never trust client input

---

### Authorization

Implement per endpoint using:

* **RBAC** → simple role policies
* **ABAC** → contextual policies

---

## Golden Rule

> Authentication proves identity.
> Authorization enforces permissions.
> You need both — always.
