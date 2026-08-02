# July 2025 KEV Review

## Summary

This note reviews representative vulnerabilities added to CISA's Known Exploited Vulnerabilities catalog during July 2025. The goal is to translate KEV activity into practical SOC, vulnerability management, and incident response thinking.

Primary themes for this month: **Microsoft enterprise platform exposure; edge appliance and network device risk; endpoint and browser exploitation; web application exploitation leading to code execution; developer tooling and application framework exposure**.

## Representative KEV Entries

| Date Added | CVE | Vendor | Product | Vulnerability | Ransomware Use |
| --- | --- | --- | --- | --- | --- |
| 2025-07-28 | CVE-2023-2533 | PaperCut | NG/MF | PaperCut NG/MF Cross-Site Request Forgery (CSRF) Vulnerability | Unknown |
| 2025-07-28 | CVE-2025-20337 | Cisco | Identity Services Engine | Cisco Identity Services Engine Injection Vulnerability | Unknown |
| 2025-07-28 | CVE-2025-20281 | Cisco | Identity Services Engine | Cisco Identity Services Engine Injection Vulnerability | Unknown |
| 2025-07-22 | CVE-2025-2775 | SysAid | SysAid On-Prem | SysAid On-Prem Improper Restriction of XML External Entity Reference Vulnerability | Unknown |
| 2025-07-22 | CVE-2025-2776 | SysAid | SysAid On-Prem | SysAid On-Prem Improper Restriction of XML External Entity Reference Vulnerability | Unknown |
| 2025-07-22 | CVE-2025-6558 | Google | Chromium | Google Chromium ANGLE and GPU Improper Input Validation Vulnerability | Unknown |

## Analyst Takeaways

- CVE-2023-2533 / PaperCut NG/MF: PaperCut NG/MF contains a cross-site request forgery (CSRF) vulnerability, which, under specific conditions, could potentially enable an attacker to alter security settings or execute arbitrary code. 
- CVE-2025-20337 / Cisco Identity Services Engine: Cisco Identity Services Engine contains an injection vulnerability in a specific API of Cisco ISE and Cisco ISE-PIC due to insufficient validation of user-supplied input allowing an attacker to exploit this vulnerability by submitting a crafted API request. Successful exploitation could allow an attacker to perform remote code execution and obtaining root privileges on an affected device.
- CVE-2025-20281 / Cisco Identity Services Engine: Cisco Identity Services Engine contains an injection vulnerability in a specific API of Cisco ISE and Cisco ISE-PIC due to insufficient validation of user-supplied input allowing an attacker to exploit this vulnerability by submitting a crafted API request. Successful exploitation could allow an attacker to perform remote code execution and obtaining root privileges on an affected device.
- CVE-2025-2775 / SysAid SysAid On-Prem: SysAid On-Prem contains an improper restriction of XML external entity reference vulnerability in the Checkin processing functionality, allowing for administrator account takeover and file read primitives.
- CVE-2025-2776 / SysAid SysAid On-Prem: SysAid On-Prem contains an improper restriction of XML external entity reference vulnerability in the Server URL processing functionality, allowing for administrator account takeover and file read primitives.
- CVE-2025-6558 / Google Chromium: Google Chromium contains an improper input validation vulnerability in ANGLE and GPU. This vulnerability could allow a remote attacker to potentially perform a sandbox escape via a crafted HTML page. This vulnerability could affect multiple web browsers that utilize Chromium, including, but not limited to, Google Chrome, Microsoft Edge, and Opera.

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