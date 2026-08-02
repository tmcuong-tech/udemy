# November 2025 KEV Review

## Summary

This note reviews representative vulnerabilities added to CISA's Known Exploited Vulnerabilities catalog during November 2025. The goal is to translate KEV activity into practical SOC, vulnerability management, and incident response thinking.

Primary themes for this month: **edge appliance and network device risk; endpoint and browser exploitation; web application exploitation leading to code execution; identity and access control weakness; developer tooling and application framework exposure**.

## Representative KEV Entries

| Date Added | CVE | Vendor | Product | Vulnerability | Ransomware Use |
| --- | --- | --- | --- | --- | --- |
| 2025-11-28 | CVE-2021-26829 | OpenPLC | ScadaBR | OpenPLC ScadaBR Cross-site Scripting Vulnerability | Unknown |
| 2025-11-21 | CVE-2025-61757 | Oracle | Fusion Middleware | Oracle Fusion Middleware Missing Authentication for Critical Function Vulnerability | Unknown |
| 2025-11-19 | CVE-2025-13223 | Google | Chromium V8 | Google Chromium V8 Type Confusion Vulnerability | Unknown |
| 2025-11-18 | CVE-2025-58034 | Fortinet | FortiWeb | Fortinet FortiWeb OS Command Injection Vulnerability | Unknown |
| 2025-11-14 | CVE-2025-64446 | Fortinet | FortiWeb | Fortinet FortiWeb Path Traversal Vulnerability | Unknown |
| 2025-11-12 | CVE-2025-12480 | Gladinet | Triofox | Gladinet Triofox Improper Access Control Vulnerability | Unknown |

## Analyst Takeaways

- CVE-2021-26829 / OpenPLC ScadaBR: OpenPLC ScadaBR contains a cross-site scripting vulnerability via system_settings.shtm.
- CVE-2025-61757 / Oracle Fusion Middleware: Oracle Fusion Middleware contains a missing authentication for critical function vulnerability, allowing unauthenticated remote attackers to take over Identity Manager.
- CVE-2025-13223 / Google Chromium V8: Google Chromium V8 contains a type confusion vulnerability that allows for heap corruption.
- CVE-2025-58034 / Fortinet FortiWeb: Fortinet FortiWeb contains an OS command Injection vulnerability that may allow an authenticated attacker to execute unauthorized code on the underlying system via crafted HTTP requests or CLI commands.
- CVE-2025-64446 / Fortinet FortiWeb: Fortinet FortiWeb contains a relative path traversal vulnerability that may allow an unauthenticated attacker to execute administrative commands on the system via crafted HTTP or HTTPS requests.
- CVE-2025-12480 / Gladinet Triofox: Gladinet Triofox contains an improper access control vulnerability that allows access to initial setup pages even after setup is complete.

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