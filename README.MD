# JCE Scanner - Joomla JCE RCE Exploit (CVE-2026-48907)

## Vulnerability Details

**CVE-2026-48907** - Unauthenticated arbitrary file upload in Joomla JCE (Joomla Content Editor) profile import functionality.

### Affected Versions
- JCE 1.0.0 through 2.9.99.4
- All Joomla versions using vulnerable JCE

### CVSS Score
10.0 (Critical)

### Root Cause
The vulnerability exploits a chain of three weaknesses in the `profiles.import` endpoint:

1. **Missing Authorization (CWE-284)**: The profile import endpoint does not verify if the user is authenticated as an administrator. The only protection is a CSRF token, which can be easily extracted from the public page.

2. **Ineffective File Validation (CWE-434)**: The upload function does not validate file extensions. This allows uploading files with dangerous extensions like `shell.xml.php`, which the server interprets as PHP.

3. **Disabled Security**: The JCE code calls the Joomla upload function with the `$allow_unsafe = true` parameter, disabling the dangerous extension blacklist and allowing PHP files to be uploaded directly to the `/tmp/` directory.

### Impact
- Unauthenticated RCE
- Full site compromise
- Admin account creation
- Website defacement
- Data exfiltration
- Server compromise
- Backdoor installation

### Exploitation Chain
The attack can be executed in 3 HTTP requests without credentials:

1. Extract CSRF token from public page
2. Upload malicious JCE profile to disable upload validations
3. Upload PHP webshell via profile import
4. Access webshell to execute system commands

---

## Exploit

### Features
- Multi-threaded mass scanning (20 threads default)
- Automatic Joomla version detection
- JCE version detection and vulnerability check (CVE-2026-48907)
- CSRF token extraction
- Payload upload via `profiles.import`
- R57 webshell deployment
- RCE confirmation with `id` command
- JSON report generation
- Color-coded terminal output

Example Output:

[1/100] https://example.com
   RCE: https://example.com/tmp/r57.php
   TXT: https://example.com/tmp/poc.txt
