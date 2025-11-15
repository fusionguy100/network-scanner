def generate_recommendations(open_ports):
    issues = []

    if 23 in open_ports:
        issues.append("Telnet detected (port 23) — disable and use SSH instead.")

    if 445 in open_ports and 139 in open_ports:
        issues.append("SMBv1 may be enabled — high ransomware risk.")

    if 3389 in open_ports:
        issues.append("RDP open — ensure MFA and firewall restrictions.")

    if not issues:
        issues.append("No major findings.")

    return issues
