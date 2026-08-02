# February 2026 KEV Review

## Summary

This note reviews representative vulnerabilities added to CISA's Known Exploited Vulnerabilities catalog during February 2026. The goal is to translate KEV activity into practical SOC, vulnerability management, and incident response thinking.

Primary themes for this month: **edge appliance and network device risk; web application exploitation leading to code execution; identity and access control weakness; developer tooling and application framework exposure**.

## Representative KEV Entries

| Date Added | CVE | Vendor | Product | Vulnerability | Ransomware Use |
| --- | --- | --- | --- | --- | --- |
| 2026-02-25 | CVE-2022-20775 | Cisco | SD-WAN | Cisco SD-WAN Path Traversal Vulnerability | Unknown |
| 2026-02-25 | CVE-2026-20127 | Cisco | Catalyst SD-WAN Controller and Manager | Cisco Catalyst SD-WAN Controller and Manager Authentication Bypass Vulnerability | Unknown |
| 2026-02-24 | CVE-2026-25108 | Soliton Systems K.K | FileZen | Soliton Systems K.K FileZen OS Command Injection Vulnerability | Unknown |
| 2026-02-20 | CVE-2025-49113 | Roundcube | Webmail | RoundCube Webmail Deserialization of Untrusted Data Vulnerability | Unknown |
| 2026-02-20 | CVE-2025-68461 | Roundcube | Webmail | RoundCube Webmail Cross-site Scripting Vulnerability | Unknown |
| 2026-02-18 | CVE-2021-22175 | GitLab | GitLab | GitLab Server-Side Request Forgery (SSRF) Vulnerability | Unknown |

## Analyst Takeaways

- CVE-2022-20775 / Cisco SD-WAN: Cisco SD-WAN CLI contains a path traversal vulnerability that could allow an authenticated local attacker to gain elevated privileges via improper access controls on commands within the application CLI. A successful exploit could allow the attacker to execute arbitrary commands as the root user.
- CVE-2026-20127 / Cisco Catalyst SD-WAN Controller and Manager: Cisco Catalyst SD-WAN Controller, formerly SD-WAN vSmart, and Cisco Catalyst SD-WAN Manager, formerly SD-WAN vManage, contain an authentication bypass vulnerability could allow an unauthenticated, remote attacker to bypass authentication and obtain administrative privileges on an affected system. This vulnerability exists because the peering authentication mechanism in an affected system is not working properly. An attacker could exploit this vulnerability by sending crafted requests to an affected system. A successful exploit could allow the attacker to log in to an affected Cisco Catalyst SD-WAN Controller as an internal, high-privileged, non-root user account. Using this account, the attacker could access NETCONF, which would then allow the attacker to manipulate network configuration for the SD-WAN fabric.
- CVE-2026-25108 / Soliton Systems K.K FileZen: Soliton Systems K.K FileZen contains an OS command injection vulnerability when an user logs-in to the affected product and sends a specially crafted HTTP request.
- CVE-2025-49113 / Roundcube Webmail: RoundCube Webmail contains a deserialization of untrusted data vulnerability that allows remote code execution by authenticated users because the _from parameter in a URL is not validated in program/actions/settings/upload.php.
- CVE-2025-68461 / Roundcube Webmail: RoundCube Webmail contains a cross-site scripting vulnerability via the animate tag in an SVG document.
- CVE-2021-22175 / GitLab GitLab: GitLab contains a server-side request forgery (SSRF) vulnerability when requests to the internal network for webhooks are enabled.

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