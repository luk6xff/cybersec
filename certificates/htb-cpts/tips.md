# CPTS Tips (Workflow + Reporting)

These are practical habits to reduce mistakes during long engagements/exams.

## 1) Timeboxing
- 10–15 min: enumerate + map attack surface.
- 20–40 min: pursue your best initial access hypothesis.
- If stuck: switch vectors (new host, new service, or pivot from creds).

## 2) Host note template
For each host create a mini record:
- `IP/FQDN` + role guess
- Open ports + versions
- Vuln hypotheses (with confidence)
- Creds found (source + validity)
- Proof of access (command output / screenshot)
- Next actions

## 3) Evidence-first mindset
- Screenshot the *moment* you gain access.
- Keep raw outputs (scan files, HTTP requests, configs).
- Record commands exactly; small differences matter later.

## 4) Common failure modes to avoid
- Scanning too broadly for too long (no follow-through).
- Not testing vhosts and alternate domains.
- Ignoring “boring” wins: password reuse, exposed configs, readable shares.
- Breaking your shell and losing the foothold.

## 5) Reporting checklist
- Executive summary: what was achieved and risk.
- Findings:
  - clear title + severity rationale
  - reproduction steps (minimal but complete)
  - impact
  - remediation guidance
- Appendix:
  - commands, tool versions, timestamps
