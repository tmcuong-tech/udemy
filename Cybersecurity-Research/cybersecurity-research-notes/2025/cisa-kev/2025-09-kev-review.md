# September 2025 KEV Review

## Summary

This note reviews representative vulnerabilities added to CISA's Known Exploited Vulnerabilities catalog during September 2025. The goal is to translate KEV activity into practical SOC, vulnerability management, and incident response thinking.

Primary themes for this month: **edge appliance and network device risk; endpoint and browser exploitation; web application exploitation leading to code execution**.

## Representative KEV Entries

| Date Added | CVE | Vendor | Product | Vulnerability | Ransomware Use |
| --- | --- | --- | --- | --- | --- |
| 2025-09-29 | CVE-2025-32463 | Sudo | Sudo | Sudo Inclusion of Functionality from Untrusted Control Sphere Vulnerability | Unknown |
| 2025-09-29 | CVE-2025-59689 | Libraesva | Email Security Gateway | Libraesva Email Security Gateway Command Injection Vulnerability | Unknown |
| 2025-09-29 | CVE-2025-10035 | Fortra | GoAnywhere MFT | Fortra GoAnywhere MFT Deserialization of Untrusted Data Vulnerability | Known |
| 2025-09-29 | CVE-2025-20352 | Cisco | IOS and IOS XE | Cisco IOS and IOS XE Software SNMP Denial of Service and Remote Code Execution Vulnerability | Unknown |
| 2025-09-29 | CVE-2021-21311 | Adminer | Adminer | Adminer Server-Side Request Forgery Vulnerability | Unknown |
| 2025-09-25 | CVE-2025-20362 | Cisco | Secure Firewall Adaptive Security Appliance and Secure Firewall Threat Defense | Cisco Secure Firewall Adaptive Security (ASA) Appliance and Secure Firewall Threat Defense (FTD) Missing Authorization Vulnerability | Unknown |

## Analyst Takeaways

- CVE-2025-32463 / Sudo Sudo: Sudo contains an inclusion of functionality from untrusted control sphere vulnerability. This vulnerability could allow local attacker to leverage sudo’s -R (--chroot) option to run arbitrary commands as root, even if they are not listed in the sudoers file.
- CVE-2025-59689 / Libraesva Email Security Gateway: Libraesva Email Security Gateway (ESG) contains a command injection vulnerability which allows command injection via a compressed e-mail attachment.
- CVE-2025-10035 / Fortra GoAnywhere MFT: Fortra GoAnywhere MFT contains a deserialization of untrusted data vulnerability allows an actor with a validly forged license response signature to deserialize an arbitrary actor-controlled object, possibly leading to command injection.
- CVE-2025-20352 / Cisco IOS and IOS XE: Cisco IOS and IOS XE contains a stack-based buffer overflow vulnerability in the Simple Network Management Protocol (SNMP) subsystem that could allow for denial of service or remote code execution. A successful exploit could allow a low-privileged attacker to cause the affected system to reload, resulting in a DoS condition, or allow a high-privileged attacker to execute arbitrary code as the root user and obtain full control of the affected system.
- CVE-2021-21311 / Adminer Adminer: Adminer contains a server-side request forgery vulnerability that, when exploited, allows a remote attacker to obtain potentially sensitive information.
- CVE-2025-20362 / Cisco Secure Firewall Adaptive Security Appliance and Secure Firewall Threat Defense: Cisco Secure Firewall Adaptive Security (ASA) Appliance and Secure Firewall Threat Defense (FTD) Software VPN Web Server contain a missing authorization vulnerability. This vulnerability could be chained with CVE-2025-20333.

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