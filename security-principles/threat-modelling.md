# Threat Modelling


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


* Threats to Properties Diagram fro Microsoft.
| **Property**      | **Threat**            | **Definition**                                | **Example**                                                                                  |
|--------------------|-----------------------|------------------------------------------------|----------------------------------------------------------------------------------------------|
| Authentication     | Spoofing             | Impersonating something or someone else       | Pretending to be any of billg, microsoft.com, or ntdll.dll                                   |
| Integrity          | Tampering            | Modifying data or code                        | Modifying a DLL on disk or DVD, or a packet as it traverses the LAN                          |
| Non-repudiation    | Repudiation          | Claiming to have not performed an action      | "I didn’t send that email," "I didn’t modify that file," "I certainly didn’t visit that web site, dear!" |
| Confidentiality    | Information Disclosure | Exposing information to someone not authorized to see it | Allowing someone to read the Windows source code; publishing a list of customers to a web site |
| Availability       | Denial of Service    | Deny or degrade service to users              | Crashing Windows or a web site, sending a packet and absorbing seconds of CPU time, or routing packets into a black hole |
| Authorization      | Elevation of Privilege | Gain capabilities without proper authorization | Allowing a remote internet user to run commands is the classic example, but going from a limited user to admin is also EoP |

---



