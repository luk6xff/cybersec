# IR and IM - Incident Response and Incident Management


## Introduction

In the realm of cybersecurity, effectively identifying and managing cyber incidents is paramount to safeguarding an organization's digital assets. This technical note delves into the concept of a **Cyber Incident**, the role of the **Security Operations Centre (SOC)**, and the frameworks of **Incident Response** and **Incident Management**. Additionally, it explores the hierarchical **Levels of Incident Response and Management**, providing a comprehensive overview essential for cybersecurity professionals.

## Key Technical Terms

- **Cyber Incident**
- **Security Operations Centre (SOC)**
- **Incident Response**
- **Incident Management**
- **Digital Forensics**
- **Security Information and Event Management (SIEM)**
- **Endpoint Detection and Response (EDR)**
- **Anti Virus (AV)**
- **Intrusion Prevention Systems (IPS)**
- **Computer Emergency Readiness Team (CERT)**
- **Computer Security Incident Response Team (CSIRT)**
- **Crisis Management Team (CMT)**
- **Triaging**
- **Phishing Emails**
- **Malware**
- **Anomalous Activity**
- **Playbooks**
- **Containment, Eradication, and Recovery**

## What is a Cyber Incident?

A **Cyber Incident** refers to any event that compromises the security of an organization's information systems. Unlike routine security alerts, a cyber incident signifies a potential or actual breach that requires immediate attention to mitigate risks and prevent further damage. The pathway to identifying a cyber incident typically begins with the **Security Operations Centre (SOC)**, where continuous monitoring and analysis of security events occur.

## Role of the Security Operations Centre (SOC)

The **SOC** serves as the frontline defense in an organization's cybersecurity framework. Comprising a team of analysts, the SOC continuously monitors the organization's digital estate for security events. Key functions of the SOC include:

- **Event Monitoring:** Tracking activities across the organization's network and systems.
- **Alert Generation:** Identifying anomalies or unexpected events that may indicate security threats.
- **Alert Investigation:** Assessing the validity of alerts to filter out false positives.
- **Triage Process:** Evaluating the severity of legitimate alerts to determine the necessity of escalating to a cyber incident.

### Filtering Mechanism

The SOC acts as a **filter**, ensuring that only significant events escalate to cyber incidents. For instance, **Intrusion Prevention Systems (IPS)** like spam filters automatically block numerous **phishing emails** daily. Even if some malicious content slips through, tools like **Anti Virus (AV)** and **Endpoint Detection and Response (EDR)** software can neutralize threats, prompting the SOC to update security measures without escalating to an incident.

## Incident Response and Management

Once an alert is deemed severe enough by the SOC, **Incident Response** and **Incident Management** protocols are activated. While often combined under the umbrella term **Incident Response**, these two components have distinct roles:

### Incident Response

**Incident Response** focuses on the technical aspects of addressing a cyber incident. Its primary objective is to answer the question:

**"What happened?"**

Key activities include:

- **Alert Analysis:** Reviewing information from tools like **SIEM**, **EDR**, and **AV** to understand the nature of the incident.
- **Digital Forensics:** Conducting in-depth investigations to gather additional data, such as recovering hard disks, volatile memory, and system logs from compromised hosts.
- **Scope Determination:** Assessing the extent of the incident to inform subsequent management actions.

### Incident Management

**Incident Management** addresses the procedural and organizational aspects of handling a cyber incident. It seeks to answer:

**"How do we respond to what happened?"**

Core responsibilities include:

- **Triaging:** Continuously assessing the incident's severity as new information emerges.
- **Stakeholder Engagement:** Involving relevant parties, including **Subject Matter Experts (SMEs)**.
- **Action Guidance:** Utilizing **playbooks** to steer containment, eradication, and recovery efforts.
- **Communication:** Managing internal and external communications during the incident.
- **Documentation:** Recording actions taken and their impacts for future reference and improvement.
- **Incident Closure:** Finalizing the incident and integrating lessons learned into security protocols.

## Levels of Incident Response and Management

Cyber incidents vary in severity, necessitating a tiered response approach. This hierarchy ensures that incidents are handled proportionately, involving appropriate resources and stakeholders. The following levels outline a structured response mechanism:

### Level 1: SOC Incident

- **Characteristics:** Low severity, often isolated events.
- **Response:** Single analyst updates security measures, such as mail filtering rules, to block threats.
- **Example:** An analyst identifies and blocks a phishing email from a single sender.

### Level 2: CERT Incident

- **Characteristics:** Moderate severity, multiple related events.
- **Response:** Multiple SOC analysts collaborate to investigate the incident's scope.
- **Example:** Several users receive the same phishing email, prompting a **Computer Emergency Readiness Team (CERT)** to assess potential malware distribution.

### Level 3: CSIRT Incident

- **Characteristics:** High severity, widespread impact.
- **Response:** The entire SOC and forensic teams engage to contain and eradicate the threat.
- **Example:** Detection of malware spread across multiple hosts, necessitating a **Computer Security Incident Response Team (CSIRT)** to implement containment and recovery strategies.

### Level 4: CMT Incident

- **Characteristics:** Critical severity, full-scale crisis.
- **Response:** Activation of the **Crisis Management Team (CMT)**, including executive stakeholders and external entities like regulators or law enforcement.
- **Example:** A sophisticated cyberattack compromises critical infrastructure, requiring comprehensive measures such as taking the organization offline to prevent further damage.

## Example Scenario: Phishing Email Incident

Consider a scenario where a user reports receiving a phishing email. The incident response unfolds as follows:

1. **Level 1:** The SOC analyst investigates the email, identifies it as an isolated phishing attempt, and updates the spam filter to block the sender.
2. **Level 2:** If multiple users receive the phishing email, a CERT incident is invoked to assess whether any users interacted with the email or if malware is present.
3. **Level 3:** Discovery of malware spread leads to a CSIRT incident, mobilizing the entire SOC and forensic teams to contain and eradicate the threat.
4. **Level 4:** If the malware affects critical systems or escalates to a broader cyber crisis, the CMT is activated to manage the extensive impact.



## Roles in Incident Response and Management

| **Role**                      | **Description**                                                                                                                                                                                                                                        | **Key Responsibilities**                                                                                                                                                                                                                                                   | **Tools & Skills**                                                                                                     |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| **SOC Analyst**               | Monitors and manages security events and alerts within the Security Operations Centre (SOC). They are often the first responders to potential security incidents.                                                                                         | - Monitor security alerts and events<br>- Investigate anomalies<br>- Perform initial triage of incidents<br>- Escalate incidents based on severity                                                                                                                           | - Security Information and Event Management (SIEM) tools<br>- Knowledge of network protocols<br>- Analytical skills  |
| **SOC Lead / SOC Manager**    | Oversees the SOC team, manages workflow, and decides when to escalate alerts to incidents. They ensure efficient task distribution and incident escalation procedures are followed.                                                                        | - Manage and coordinate SOC activities<br>- Escalate alerts to incidents<br>- Ensure team adherence to protocols<br>- Provide technical guidance during investigations                                                                                                            | - Leadership and management skills<br>- In-depth knowledge of cybersecurity tools and practices                     |
| **Forensic Analyst**          | Conducts detailed investigations to understand the nature and extent of security incidents by examining digital evidence.                                                                                                                                 | - Perform digital forensics on compromised systems<br>- Analyze memory dumps and hard drives<br>- Collect and preserve evidence<br>- Document findings                                                                                                                           | - Forensic tools (e.g., EnCase, FTK)<br>- Understanding of file systems and data recovery<br>- Attention to detail      |
| **Malware Analyst**           | Specializes in dissecting and understanding malicious software to determine its behavior and impact.                                                                                                                                                     | - Analyze malware samples<br>- Debug and decompile malicious code<br>- Identify Indicators of Compromise (IoCs)<br>- Develop signatures for detection                                                                                                                           | - Reverse engineering skills<br>- Knowledge of programming languages (e.g., C++, Python)<br>- Malware analysis tools |
| **Threat Hunter**             | Proactively searches for hidden threats within the network that evade existing security measures.                                                                                                                                                        | - Identify and investigate potential threats<br>- Develop new detection rules<br>- Analyze logs and network traffic<br>- Collaborate with SOC to improve detection capabilities                                                                                                   | - Advanced knowledge of network security<br>- Proficiency with SIEM and EDR tools<br>- Analytical and investigative skills |
| **First Responder**           | The initial point of contact when a security incident is detected, often from non-SOC teams. They take preliminary actions to contain the incident and preserve evidence.                                                                              | - Identify and report incidents<br>- Perform initial containment<br>- Preserve evidence for further analysis<br>- Communicate incident details to SOC                                                                                                                                 | - Basic understanding of cybersecurity principles<br>- Communication skills<br>- Familiarity with incident reporting tools |
| **Security Engineer**         | Designs, implements, and maintains security infrastructure. They provide technical expertise during incidents related to their specific systems or applications.                                                                                         | - Develop and maintain security architectures<br>- Implement security controls<br>- Assist in incident investigations<br>- Ensure SOC receives necessary logs and data                                                                                                           | - Knowledge of security technologies (e.g., firewalls, IDS/IPS)<br>- Scripting and automation skills<br>- System administration expertise |
| **Information Security Officer (ISO)** | Manages and oversees the security posture of a specific division or the entire organization. Acts as a bridge between technical teams and management, ensuring security policies are enforced and incidents are managed effectively.                      | - Develop and enforce security policies<br>- Coordinate with Incident Response teams<br>- Act as liaison between technical and managerial staff<br>- Oversee compliance with security standards                                                                                       | - Leadership and strategic planning<br>- Knowledge of regulatory requirements<br>- Strong communication skills       |
| **Incident Manager**          | Leads the management aspect of incident response, ensuring that all procedures are followed and that the incident is documented and resolved efficiently.                                                                                                | - Coordinate incident response efforts<br>- Document incident timelines and actions<br>- Ensure adherence to incident response plans<br>- Facilitate communication among stakeholders                                                                                                 | - Project management skills<br>- Excellent organizational abilities<br>- Familiarity with incident management frameworks |
| **Project Owner**             | Leads the development and deployment of security solutions. Acts as a subject matter expert during incidents related to their projects, ensuring that solutions are updated and incidents are addressed promptly.                                           | - Oversee security projects<br>- Provide expertise during incidents<br>- Ensure timely updates and patches<br>- Collaborate with Incident Response teams to implement fixes                                                                                                          | - Project management expertise<br>- In-depth knowledge of specific applications or systems<br>- Agile methodologies  |
| **Subject Matter Expert (SME)** | Provides specialized knowledge related to specific technologies or systems involved in an incident. They assist the incident response team by offering insights that aid in understanding and mitigating the incident.                                      | - Offer expertise on specific systems or technologies<br>- Assist in incident analysis and remediation<br>- Provide guidance on best practices and security measures                                                                                                                 | - Deep technical knowledge in specific areas (e.g., Active Directory, cloud services)<br>- Problem-solving skills        |
| **Crisis Manager**            | Leads the Crisis Management Team (CMT) during critical incidents, coordinating responses across various departments and ensuring that the organization navigates the crisis effectively.                                                                   | - Oversee crisis response strategies<br>- Coordinate with executive and external stakeholders<br>- Make high-level decisions to mitigate crisis impact<br>- Ensure continuity of business operations during crises                                                                      | - Executive leadership skills<br>- Strategic decision-making<br>- Experience in crisis management                       |
| **Executive**                 | Senior leadership members who are involved in managing severe incidents. They provide strategic direction, allocate resources, and communicate with external entities such as regulators or law enforcement.                                               | - Make strategic decisions during incidents<br>- Allocate resources for incident response<br>- Communicate with stakeholders and external parties<br>- Oversee overall incident management and recovery efforts                                                                          | - Leadership and communication skills<br>- Understanding of business operations and risk management<br>- Decision-making abilities |

## Detailed Role Insights

### SOC Analyst
SOC Analysts are the backbone of the Security Operations Centre. They continuously monitor security systems, analyze alerts, and determine the legitimacy of potential threats. Their ability to quickly assess and respond to incidents helps prevent minor issues from escalating into significant breaches.

### SOC Lead / SOC Manager
The SOC Lead not only manages the SOC team but also ensures that the team operates efficiently. They make critical decisions about incident escalation and ensure that analysts have the necessary resources and support to perform their duties effectively.

### Forensic Analyst
Forensic Analysts play a crucial role in understanding the full impact of an incident. By examining digital evidence, they can trace the steps of an attacker, identify compromised systems, and provide detailed reports that inform remediation efforts.

### Malware Analyst
Specializing in malicious software, Malware Analysts dissect malware to understand its functionality and propagation methods. Their work is essential for developing effective detection signatures and preventing future infections.

### Threat Hunter
Threat Hunters take a proactive approach by searching for threats that have evaded initial security defenses. Their efforts often lead to the discovery of sophisticated attacks that automated systems might miss.

### First Responder
First Responders ensure that the initial stages of incident handling are managed properly. Their actions are critical in containing incidents early and preserving vital evidence for further investigation.

### Security Engineer
Security Engineers build and maintain the security infrastructure that protects an organization’s assets. During incidents, they provide the technical expertise needed to address vulnerabilities and strengthen defenses.

### Information Security Officer (ISO)
ISOs ensure that security policies are effectively implemented across the organization. They play a key role in bridging the gap between technical teams and management, ensuring that security strategies align with business objectives.

### Incident Manager
Incident Managers oversee the entire incident response process, ensuring that all actions are documented and that the response follows established protocols. Their organizational skills are vital for managing complex incidents efficiently.

### Project Owner
Project Owners ensure that security measures are integrated into development projects. During incidents, they provide necessary insights to quickly address and resolve security issues related to their projects.

### Subject Matter Expert (SME)
SMEs provide in-depth knowledge about specific systems or technologies. Their expertise is invaluable during incidents that involve specialized areas, allowing the response team to address issues more effectively.

### Crisis Manager
Crisis Managers lead the response to critical incidents, coordinating efforts across the organization and with external stakeholders. Their leadership ensures that the organization can navigate severe incidents with minimal disruption.

### Executive
Executives provide the strategic direction and resources necessary during significant incidents. Their involvement ensures that the organization’s response aligns with business goals and complies with regulatory requirements.

## Conclusion

A successful Incident Response and Management strategy relies on the collaboration of diverse roles, each bringing specialized skills and expertise. From the initial monitoring by SOC Analysts to the strategic oversight of Executives and Crisis Managers, each role plays a pivotal part in detecting, analyzing, and mitigating cyber incidents. Understanding these roles and fostering effective communication among them enhances an organization’s ability to respond to and recover from security incidents efficiently.



## Incident Management Based on the NIST Framework

Incident management is crucial for effectively addressing security events and mitigating their impact. While organizations may adapt the process to suit their specific needs, the foundational structure is often derived from the **NIST Incident Management Framework**. This framework comprises four primary phases:

---

### 1. **Preparation**
Preparation is the cornerstone of effective incident response. Since incidents often occur under stressful conditions where every moment counts, thorough preparation minimizes errors and accelerates response times. Key preparation activities include:

- **Stakeholder Identification:** Document key stakeholders and establish call trees for efficient communication during incidents.
- **Playbook Creation:** Develop and maintain playbooks for known incident types, providing step-by-step guidance.
- **Simulations and Exercises:** Conduct tabletop exercises and cyber war games to train teams and refine processes.
- **Threat Hunting:** Continuously perform threat hunting to identify emerging attacker techniques and improve alerting rules.

---

### 2. **Detection and Analysis**
The detection and analysis phase is critical to understanding the nature and scope of the incident. Some organizations introduce a triage step within this phase to classify the severity of alerts and incidents.

Key activities include:

- **Alert Review:** Monitor alerts on tools like antivirus (AV), endpoint detection and response (EDR), and security information and event management (SIEM) systems.
- **Forensic Investigation:** Examine system and network artifacts to gather evidence and assess the incident's impact.
- **Malware Analysis:** Analyze discovered malware to understand its behavior and create detection signatures.

---

### 3. **Containment, Eradication, and Recovery**
This phase focuses on managing and resolving the incident. The activities are structured sequentially to ensure effective handling:

- **Containment:** Implement measures to halt the incident's progression (e.g., isolating affected systems).
- **Eradication:** Remove the threat actor and any associated malicious activity from the environment.
- **Recovery:** Restore affected systems and processes, enabling the organization to resume business as usual (BAU).

The sequential nature of these steps is critical. Premature eradication or recovery without containment risks allowing the threat actor to maintain or regain access. For example, changing passwords (eradication) without blocking the threat actor's access (containment) could enable them to reacquire credentials.

**Cyclic Nature of Phases:** Detection, analysis, containment, and eradication often involve iterative cycles as new insights emerge. Actions are taken progressively while continuing the investigation, ensuring timely mitigation without waiting for full incident scope clarity.

---

### 4. **Post-Incident Activity**
The final phase involves learning and improving from the incident response process. Activities include:

- **Review and Analysis:** Evaluate the incident timeline and response effectiveness.
- **Lessons Learned:** Document insights to enhance preparation and refine processes.
- **Process Updates:** Update playbooks, detection rules, and training protocols based on the incident.

This phase ensures continuous improvement, better equipping the organization for future incidents.

### Or Six Phases of Incident Response

| Action        | Description                                                                                                                                    |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| Preparation    | Ensuring resources and plans are in place to deal with potential security incidents.                                                           |
| Identification | Confirming the threat and threat actor have been correctly identified.                                                                         |
| Containment    | Containing the threat to prevent it from affecting other systems or users.                                                                     |
| Eradication    | Removing the active threat from the environment.                                                                                               |
| Recovery       | Reviewing the impacted systems thoroughly and returning to normal business operations.                                                         |
| Lessons Learned | Understanding what can be improved to prevent future incidents. For example, if the cause was phishing, improve employee training on phishing recognition. |


### Summary
A breach of security is known as an **incident**. Despite all rigorous threat models and secure system designs, incidents can occur. The actions taken to resolve and remediate the threat are known as **Incident Response (IR)**, a dedicated career path within cybersecurity.

Incidents are classified based on urgency and impact:

- **Urgency:** Determined by the type of attack.
- **Impact:** Determined by the affected system and its effect on business operations.

An incident is addressed by a **Computer Security Incident Response Team (CSIRT)**, a prearranged group of employees with technical knowledge of the systems and/or current incident.

The NIST Incident Management Framework provides a structured approach to managing security incidents. By emphasizing preparation, clear detection and analysis, sequential response actions, and post-incident learning, organizations can effectively minimize damage and improve resilience against future threats.







## Common Pitfalls in Incident Management

While a robust incident response and management strategy is essential, organizations often encounter challenges that undermine their efforts. These common pitfalls can delay response times, exacerbate the impact, and increase organizational risk. Understanding and addressing these pitfalls is critical for improving overall incident management.

---

### 1. **Insufficient Hardening**
This pitfall often arises even before an incident occurs due to prioritizing speed and profitability over security.

- **Hardening Overview:** Hardening involves configuring systems to align with security best practices after deployment. When skipped, systems remain vulnerable, increasing the likelihood of incidents.
- **Impact:** Skipping hardening results in more frequent incidents, any of which could cause significant damage if successful.
- **Solution:**
  - Adopt the **Shift Left** principle by integrating hardening during the development phase.
  - Ensure post-deployment hardening is mandatory for all solutions.

---

### 2. **Insufficient Logging**
Effective incident detection hinges on comprehensive logging, yet many organizations neglect this critical aspect.

- **Issues:**
  - Limited logging creates a "flying blind" scenario where incidents may go unnoticed.
  - Cost constraints, such as SIEM ingestion fees or network charges for remote devices, often result in reduced logging.
  - Local logs may have short retention periods or could be tampered with by threat actors.
- **Impact:** Insufficient logging delays detection, obscures incident scope, and complicates investigations.
- **Solution:**
  - Prioritize critical log sources and optimize retention policies.
  - Implement cost-effective methods for collecting remote logs.
  - Regularly test logging configurations to ensure critical events are captured.

---

### 3. **Insufficient and Over-Alerting**
Both insufficient and excessive alerts can hinder effective incident response.

- **Insufficient Alerts:** Key threats may go unnoticed due to gaps in alert rules.
- **Over-Alerting:** Excessive false positives can desensitize teams, leading to critical alerts being ignored ("cry wolf" effect).
- **Impact:** Ineffective alert management slows detection and response, increasing the risk of undetected threats.
- **Solution:**
  - Perform **threat hunting** to refine alert rules and identify meaningful patterns.
  - Optimize the signal-to-noise ratio of alerts to balance coverage and relevance.

---

### 4. **Insufficient Determination of Incident Scope**
Understanding the scope of an incident is vital to effective response but is often underestimated or overestimated.

- **Underestimation:** Leads to incomplete eradication of the threat actor.
- **Overestimation:** Results in unnecessary disruptions to business operations.
- **Impact:** Both scenarios can prolong the incident or cause excessive downtime.
- **Solution:**
  - Continuously train and prepare teams to improve scope assessment.
  - Employ iterative processes during response to refine understanding over time.

---

### 5. **Insufficient Accountability**
Lack of clear accountability during incident response often leads to inaction.

- **Issues:** Teams may discuss actions but fail to execute them due to unclear responsibilities.
- **Impact:** Delayed actions allow the incident to escalate, increasing damage.
- **Solution:**
  - Assign specific individuals to each action during the incident.
  - Maintain detailed notes to track responsibilities and outcomes.
  - Empower an **incident manager** to oversee accountability and progress.

---

### 6. **Insufficient Backups**
Backups are often the last line of defense during catastrophic incidents, yet they are frequently inadequate.

- **Issues:**
  - Lack of comprehensive backup processes and policies.
  - Inadequate isolation of backups, such as High Availability Disaster Recovery (HADR) setups that replicate ransomware.
- **Impact:** Without secure backups, recovery from incidents like ransomware attacks becomes impossible.
- **Solution:**
  - Ensure offline and remote backups are maintained alongside HADR setups.
  - Regularly test backups to confirm integrity and accessibility.
  - Establish clear policies for creating, updating, and securing backups.




## References

1. **NIST Special Publication 800-61 Rev. 2**: *Computer Security Incident Handling Guide*. National Institute of Standards and Technology.
2. **ISO/IEC 27035**: *Information Security Incident Management*. International Organization for Standardization.
3. **Lockheed Martin Cyber Kill Chain®**: Understanding the Stages of a Cyber Attack.
4. **MITRE ATT&CK Framework**: Comprehensive Matrix of Adversary Tactics, Techniques, and Procedures.
5. **SANS Institute**: Incident Response and Digital Forensics Resources.

