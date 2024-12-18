# CIA Triad


* **Confidentiality** ensures that only the intended persons or recipients can access the data.

* **Integrity** aims to ensure that the data cannot be altered; moreover, we can detect any alteration if it occurs.

* **Availability** aims to ensure that the system or service is available when needed.




```markdown
## Let’s Consider the CIA Security Triad in the Case of Online Shopping

**Confidentiality:**
During online shopping, you expect your credit card number to be disclosed only to the entity that processes the payment. If you doubt that your credit card information will be disclosed to an untrusted party, you will most likely refrain from continuing with the transaction. Moreover, if a data breach results in the disclosure of personally identifiable information, including credit cards, the company will incur huge losses on multiple levels.

**Integrity:**
After filling out your order, if an intruder can alter the shipping address you have submitted, the package will be sent to someone else. Without data integrity, you might be very reluctant to place your order with this seller.

**Availability:**
To place your online order, you will either browse the store’s website or use its official app. If the service is unavailable, you won’t be able to browse the products or place an order. If you continue to face such technical issues, you might eventually give up and start looking for a different online store.

---

## CIA in the Context of Patient Records and Related Systems

**Confidentiality:**
According to various laws in modern countries, healthcare providers must ensure and maintain the confidentiality of medical records. Consequently, healthcare providers can be held legally accountable if they illegally disclose their patients’ medical records.

**Integrity:**
If a patient record is accidentally or maliciously altered, it can lead to the wrong treatment being administered, which, in turn, can lead to a life-threatening situation. Hence, the system would be useless and potentially harmful without ensuring the integrity of medical records.

**Availability:**
When a patient visits a clinic to follow up on their medical condition, the system must be available. An unavailable system would mean that the medical practitioner cannot access the patient’s records and consequently won’t know if any current symptoms are related to the patient’s medical history. This situation makes the medical diagnosis more challenging and error-prone.

---

## Beyond the CIA Security Triad: Authenticity and Nonrepudiation

**Authenticity:**
"Authentic" means not fraudulent or counterfeit. Authenticity is about ensuring that the document, file, or data is from the claimed source.

**Nonrepudiation:**
"Repudiate" means refusing to acknowledge the validity of something. Nonrepudiation ensures that the original source cannot deny that they are the source of a particular document, file, or data. This characteristic is indispensable in various domains, such as shopping, patient diagnosis, and banking.

These two requirements are closely related. The need to distinguish authentic files or orders from fake ones is indispensable. Moreover, ensuring that the other party cannot deny being the source is vital for many systems to be usable.

In online shopping, depending on your business, you might tolerate attempting to deliver a t-shirt with cash-on-delivery and later learn that the recipient never placed such an order. However, no company can tolerate shipping 1000 cars only to discover that the order is fake.

In the example of a shopping order, you want to confirm that the said customer indeed placed this order — that’s authenticity. Moreover, you want to ensure they cannot deny placing this order — that’s nonrepudiation.

As a company, if you receive a shipment order of 1000 cars, you need to ensure the authenticity of this order; moreover, the source should not be able to deny placing such an order. Without authenticity and nonrepudiation, business cannot be conducted.

---

## Parkerian Hexad

In 1998, Donn Parker proposed the Parkerian Hexad, a set of six security elements. They are:

- Availability
- Utility
- Integrity
- Authenticity
- Confidentiality
- Possession


**Utility:**
Utility focuses on the usefulness of the information. For instance, a user might have lost the decryption key to access a laptop with encrypted storage. Although the user still has the laptop with its disk(s) intact, they cannot access them. In other words, although the information is still available, it is in a form that is not useful, i.e., of no utility.

**Possession:**
This security element requires that we protect the information from unauthorized taking, copying, or controlling. For instance, an adversary might take a backup drive, meaning we lose possession of the information as long as they have the drive. Alternatively, the adversary might succeed in encrypting our data using ransomware; this also leads to the loss of possession of the data.
```
