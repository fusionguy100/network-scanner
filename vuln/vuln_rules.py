def analyze_banner(port, banner):
    issues = []

    if banner is None:
        return issues

    lower = banner.lower()

    # --- HTTP Vulnerabilities ---
    if port == 80 or port == 8080:
        if "apache" in lower and "2.2" in lower:
            issues.append("Apache 2.2 detected — End of Life, multiple CVEs.")

        if "apache" in lower and "2.4.49" in lower:
            issues.append("Apache 2.4.49 vulnerable to CVE-2021-41773 (path traversal).")

    # --- SSH Vulnerabilities ---
    if port == 22:
        if "openssh" in lower:
            if "7.2" in lower:
                issues.append("OpenSSH 7.2 vulnerable to CVE-2016-6515.")

            if "5." in lower:
                issues.append("Very old OpenSSH version detected — security risk.")

    # --- SMBv1 Detection ---
    if port == 445:
        if "smb" in lower or "windows" in lower:
            issues.append("SMBv1 detected — extremely vulnerable (WannaCry).")

    # --- FTP Vulnerabilities ---
    if port == 21 and "vsftpd 2.3.4" in lower:
        issues.append("vsftpd 2.3.4 backdoor vulnerability (CVE-2011-2523).")

    # --- Generic Indicators ---
    if "deprecated" in lower:
        issues.append("Service banner contains deprecated component warning.")

    return issues
