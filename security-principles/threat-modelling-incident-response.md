# Threat Modelling & Incident Response


## Threat Modelling

Threat modelling is the process of reviewing, improving, and testing the security protocols in place within an organisation's information technology infrastructure and services.

A critical stage of the threat modelling process is identifying likely threats that an application or system may face, as well as the vulnerabilities they may have.

The threat modelling process is very similar to a workplace risk assessment. The principles return to:

- Preparation
- Identification
- Mitigations
- Review

It is, however, a complex process that requires constant review and discussion with a dedicated team. An effective threat model includes:

- Threat intelligence
- Asset identification
- Mitigation capabilities
- Risk assessment

To assist with this process, there are frameworks such as **STRIDE** (Spoofing identity, Tampering with data, Repudiation threats, Information disclosure, Denial of Service, and Elevation of privileges) and **PASTA** (Process for Attack Simulation and Threat Analysis) — infosec never tasted so good!

### STRIDE Framework

STRIDE, authored by two Microsoft security researchers in 1999, remains highly relevant. The six main principles of STRIDE are detailed below:

| Principle              | Description                                                                                                                                                                              |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Spoofing**           | This principle requires authentication of requests and users accessing a system. Spoofing involves a malicious party falsely identifying itself as another. Using access keys (e.g., API keys) or encryption signatures helps mitigate this threat. |
| **Tampering**          | Anti-tampering measures ensure data integrity. Data accessed must be kept integral and accurate. For example, shops use seals on food products to ensure integrity.                       |
| **Repudiation**        | This principle involves tracking user activity through logging services. Logs help determine if someone denies an action that took place.                                                |
| **Information Disclosure** | Applications or services that handle multiple users' information should be configured to only show data relevant to the owner.                                                        |
| **Denial of Service**  | Applications and services consume system resources. Measures must be in place so abuse does not bring down the entire system.                                                             |
| **Elevation of Privilege** | The worst-case scenario. A user escalates their privileges to a higher level, such as an administrator, allowing further exploitation or information disclosure.                      |

---

## Incident Response

A breach of security is known as an **incident**. Despite all rigorous threat models and secure system designs, incidents can occur. The actions taken to resolve and remediate the threat are known as **Incident Response (IR)**, a dedicated career path within cybersecurity.

Incidents are classified based on urgency and impact:

- **Urgency:** Determined by the type of attack.
- **Impact:** Determined by the affected system and its effect on business operations.

An incident is addressed by a **Computer Security Incident Response Team (CSIRT)**, a prearranged group of employees with technical knowledge of the systems and/or current incident.

### Six Phases of Incident Response

| Action        | Description                                                                                                                                    |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| Preparation    | Ensuring resources and plans are in place to deal with potential security incidents.                                                           |
| Identification | Confirming the threat and threat actor have been correctly identified.                                                                         |
| Containment    | Containing the threat to prevent it from affecting other systems or users.                                                                     |
| Eradication    | Removing the active threat from the environment.                                                                                               |
| Recovery       | Reviewing the impacted systems thoroughly and returning to normal business operations.                                                         |
| Lessons Learned | Understanding what can be improved to prevent future incidents. For example, if the cause was phishing, improve employee training on phishing recognition. |
