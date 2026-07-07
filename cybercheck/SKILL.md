# /cybercheck

## Overview
The `cybercheck` skill is a comprehensive security auditing tool. Its primary job is to analyze a project's codebase, identify its category (web, mobile, database, API, etc.), create a secure virtual environment copy, write and run tailored security tests, and generate an in-depth vulnerability report in the main project directory.

## Instructions

When the user invokes `/cybercheck`, you must execute the following steps:

### 1. Project Discovery & Classification
Analyze the project's files, configuration, and dependencies to determine its category:
- **Web Application:** React, Vue, Angular, Next.js, Django, Ruby on Rails, etc.
- **Mobile Application:** Android (Java/Kotlin), iOS (Swift/Objective-C), Flutter, React Native.
- **Database / Storage:** SQL (PostgreSQL, MySQL), NoSQL (MongoDB, Redis), ORM configs.
- **API / Backend:** Node.js, Spring Boot, FastAPI, Go, GraphQL.
- **Desktop Application:** Electron, Tauri, C++, C#.
- **Infrastructure / Cloud:** Terraform, AWS CloudFormation, Docker, Kubernetes.

### 2. Sandbox Environment Preparation
- Create a virtual environment/sandbox copy of the project (e.g., inside a `.cybercheck_sandbox` directory or Docker container) to ensure testing does not modify or damage the main project files.
- **Important:** Ensure all auditing, dependency installations, and test executions occur **only** within this isolated sandbox.

### 3. Security Test Generation
Based on the identified project category, write specific security tests, scripts, and audit configurations. Ensure tests cover all applicable attack vectors:

#### A. Web Applications & APIs
- **Cross-Site Scripting (XSS):** Write tests injecting `<script>` payloads into all inputs, URL parameters, and headers to check for reflection and lack of sanitization.
- **SQL Injection (SQLi) & NoSQLi:** Write tests sending payloads like `' OR 1=1 --` to database queries, login forms, and endpoints.
- **Cross-Site Request Forgery (CSRF):** Write tests verifying the presence and validation of anti-CSRF tokens on state-changing requests.
- **DDoS / DoS Protection:** Audit rate-limiting middleware, payload size restrictions, and timeout configurations. Write scripts simulating high-frequency requests.
- **Authentication & Authorization:** Check for secure password hashing (e.g., bcrypt/Argon2), secure session cookies (`HttpOnly`, `Secure`, `SameSite`), and Insecure Direct Object References (IDOR).
- **Security Misconfigurations:** Verify security headers (CORS, CSP, HSTS, X-Frame-Options), disabled debug endpoints, and error handling verbosity.
- **Dependency Vulnerabilities:** Check `package.json`, `requirements.txt`, etc., against known CVE databases.

#### B. Mobile Applications
- **Insecure Data Storage:** Write tests checking if sensitive data (credentials, tokens) is stored in plain-text local databases (SQLite, SharedPreferences, NSUserDefaults).
- **Insecure Communication:** Audit TLS/SSL configurations, check for hardcoded certificate pinning, and verify lack of cleartext traffic.
- **Reverse Engineering & Tampering:** Check for code obfuscation (e.g., ProGuard/R8) and root/jailbreak detection mechanisms.
- **Deep Links / IPC:** Test exported activities, intents, and deep links for unauthorized access or data leakage.

#### C. Databases & Storage
- **Access Controls & Authentication:** Write scripts to audit user roles, overly permissive grants, and default or weak credentials.
- **Encryption:** Verify data-at-rest encryption configurations.
- **Network Exposure:** Check connection strings and configurations to ensure the database isn't bound to public interfaces (`0.0.0.0`) without proper firewalls.

#### D. Infrastructure / Docker
- **Container Security:** Check Dockerfiles for root user execution, exposed sensitive ports, and base image vulnerabilities.
- **Secrets Management:** Audit the codebase for hardcoded API keys, tokens, and passwords.

### 4. Execution & Analysis
Execute the generated tests within the sandbox environment. (If actual execution is restricted by the platform, simulate the execution by deeply analyzing the code paths against the generated test payloads).
- Log all failed tests.
- Identify the exact file, line number, and logic flaw responsible for each failure.

### 5. Reporting
After the audit is complete, generate a comprehensive markdown report in the **main** project directory named `CYBERCHECK_REPORT.md`. The report MUST include:

1. **Executive Summary:** A high-level overview of the project's security posture.
2. **Project Profile:** The identified categories and technologies used.
3. **Audit Methodology:** A list of the tests generated and executed in the sandbox.
4. **Vulnerabilities Found (Failed Cyberattacks):** A detailed breakdown of each test the project failed. For each failure include:
   - **Vulnerability Type:** (e.g., SQLi, XSS, Missing Rate Limiting)
   - **Severity:** (Critical, High, Medium, Low)
   - **Location:** File path and line number.
   - **Description:** Explanation of why the attack succeeded.
5. **Remediation Guide:** Actionable steps and code snippets to fix each identified vulnerability.

### 6. Cleanup
Remove the virtual environment/sandbox copy after the report has been successfully generated in the main directory.
