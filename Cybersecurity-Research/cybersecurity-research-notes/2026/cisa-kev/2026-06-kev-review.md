# June 2026 KEV Review

## Summary

This note reviews representative vulnerabilities added to CISA's Known Exploited Vulnerabilities catalog during June 2026. The goal is to translate KEV activity into practical SOC, vulnerability management, and incident response thinking.

Primary themes for this month: **edge appliance and network device risk; web application exploitation leading to code execution; identity and access control weakness**.

## Representative KEV Entries

| Date Added | CVE | Vendor | Product | Vulnerability | Ransomware Use |
| --- | --- | --- | --- | --- | --- |
| 2026-06-29 | CVE-2026-48558 | SimpleHelp  | SimpleHelp | SimpleHelp Authentication Bypass Vulnerability | Unknown |
| 2026-06-25 | CVE-2026-12569 | PTC | Windchill and FlexPLM | PTC Windchill and FlexPLM Improper Input Validation Vulnerability | Unknown |
| 2026-06-25 | CVE-2026-20230 | Cisco | Unified Communications Manager | Cisco Unified Communications Manager Server-Side Request Forgery (SSRF) Vulnerability | Unknown |
| 2026-06-23 | CVE-2025-67038 | Lantronix | EDS5000 | Lantronix EDS5000 Code Injection Vulnerability | Unknown |
| 2026-06-23 | CVE-2026-34910 | Ubiquiti | UniFi OS | Ubiquiti UniFi OS Improper Input Validation Vulnerability | Unknown |
| 2026-06-23 | CVE-2026-34909 | Ubiquiti | UniFi OS | Ubiquiti UniFi OS Path Traversal Vulnerability | Unknown |

## Analyst Takeaways

- CVE-2026-48558 / SimpleHelp  SimpleHelp: SimpleHelp contains an authentication bypass vulnerability in the OIDC authentication flow. When OIDC authentication is configured, identity tokens submitted during login are accepted without verifying their cryptographic signature. In a vulnerable configuration, a remote, unauthenticated attacker can submit a forged token containing arbitrary identity claims to obtain a fully authenticated technician session. In some configurations, this may also allow bypass of multi-factor authentication.
- CVE-2026-12569 / PTC Windchill and FlexPLM: PTC Windchill and FlexPLM contains an improper input validation vulnerability allowing an unauthenticated, remote attacker to execute arbitrary code by sending a malicious request to the network.
- CVE-2026-20230 / Cisco Unified Communications Manager: Cisco Unified Communications Manager (Unified CM) and Cisco Unified Communications Manager Session Management Edition (Unified CM SME) contain a server-side request forgery (SSRF) Vulnerability that could allow an unauthenticated, remote attacker to write files to the underlying operating system that could be used later to elevate to root.
- CVE-2025-67038 / Lantronix EDS5000: Lantronix EDS5000 contains a code injection vulnerability that could allow attackers to inject arbitrary OS commands into the username parameter. Injected commands are executed with root privileges.
- CVE-2026-34910 / Ubiquiti UniFi OS: Ubiquiti UniFi OS contains an improper input validation vulnerability which could allow a malicious actor with access to the network to conduct command injection.
- CVE-2026-34909 / Ubiquiti UniFi OS: Ubiquiti UniFi OS contains a path traversal vulnerability which could allow a malicious actor with access to the network to access files on the underlying system that could be manipulated to access an underlying account.

## Why This Month Matters

The KEV catalog is useful because it highlights vulnerabilities with known exploitation, not only theoretical risk. For security operations work, these entries should drive asset inventory checks, exposure review, patch prioritization, and targeted log searches.

A practical analyst should ask:

1. Do we run any affected products or related technologies?
2. Are affected systems internet-facing or reachable from untrusted networks?
3. Are patches or mitigations applied?
4. Do logs show exploitation attempts before remediation?
5. Are there signs of follow-on activity such as account misuse, file writes, new processes, or outbound connections?

## Evidence to Review

- Asset inventory and software version records
- Internet exposure and external attack surface records
- Web server, application, VPN, firewall, and endpoint logs
- Authentication logs for unusual user or administrator activity
- Vulnerability scan results and patch deployment records
- EDR alerts for suspicious process creation, file writes, or persistence
- DNS and proxy logs for unusual outbound destinations

## Detection Ideas

- Search for exploit-specific request patterns where public details are available.
- Look for successful exploitation indicators, not only blocked attempts.
- Correlate vulnerable asset exposure with suspicious authentication or process activity.
- Prioritize logs from internet-facing systems and administrative tools.
- Create watchlists for affected products until patching and validation are complete.

## Response and Remediation Notes

- Prioritize KEV-listed vulnerabilities ahead of ordinary vulnerability backlog items.
- Apply vendor patches or mitigations quickly.
- Restrict external access where possible until remediation is complete.
- Preserve logs before rebuilding or cleaning systems.
- Retest after remediation to confirm exposure is closed.
- Document exceptions with owner, business reason, compensating controls, and review date.

## Lessons Learned

Monthly KEV review helps connect vulnerability management with security operations. The useful habit is not just reading CVE names; it is checking whether the environment is exposed, whether exploitation evidence exists, and whether response actions were completed and verified.

## Sources

- CISA Known Exploited Vulnerabilities catalog: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- CISA KEV JSON feed: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json