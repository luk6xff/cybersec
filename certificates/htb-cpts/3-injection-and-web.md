# 3️⃣ Injection-Based + Web Attacks (Quicknotes)

Keep a repeatable workflow: map the app → identify trust boundaries → test inputs safely → confirm impact → capture proof.

## Web attacks (common CPTS patterns)

### HTTP verb tampering
What to test:
- endpoints that behave differently on `GET` vs `POST` vs `PUT`/`DELETE`
- misconfigured proxies/WAFs that allow forbidden methods

Checks:
- `OPTIONS` response for allowed methods
- try “method override” headers only when the stack supports it

Evidence to capture:
- request/response pair showing an auth bypass or unauthorized action.

### IDOR (Insecure Direct Object References)
What to test:
- predictable IDs in URLs/JSON bodies (e.g., `/api/users/123`)
- actions that should be scoped to the current user

Workflow:
- confirm authorization logic (not just “it works”)
- test horizontal + vertical access

Defensive note:
- authorization must be server-side on every access; don’t rely on UI controls.

### XXE (XML External Entity)
Preconditions:
- server parses XML with external entity resolution enabled

Workflow:
- verify the parser is reachable (content-type, endpoints)
- attempt a low-impact entity expansion / out-of-band confirmation in a lab-safe way

Defensive note:
- disable external entities / use safe parsers.

## Injection (command / SQL / XSS)

### Command injection
Where it hides:
- “ping”, “traceroute”, “pdf generation”, “image convert”, “backup” features

Workflow:
- start with benign timing/echo tests
- confirm command boundary and escaping rules
- upgrade to file read or minimal execution proof (within scope)

See deeper notes: [command-injection.md](../../pentesting/web-hacking/command-injection.md)

### SQL injection
Workflow:
- identify parameterized vs concatenated queries (behavioral clues)
- confirm with safe boolean tests and error clues
- move to enumeration only after confirmation

Tooling:
- `sqlmap` is great once you’ve isolated the injection point and can replay reliably.

See deeper notes: [sql-injection.md](../../pentesting/web-hacking/sql-injection.md)

### XSS
Types to consider:
- reflected, stored, DOM-based

Workflow:
- confirm context (HTML, attribute, JS string, URL)
- craft payload appropriate to context
- demonstrate impact (session/token exposure, action as user) *ethically/in-scope*

See deeper notes: [xss.md](../../pentesting/web-hacking/xss.md)

## Minimal web checklist per host
- endpoints discovered (incl. hidden vhosts)
- auth mechanisms + session cookies
- roles and authorization checks
- uploads + file handling
- API surface (OpenAPI/Swagger/Postman collections)
- input vectors (query, body, headers, JSON/XML)
