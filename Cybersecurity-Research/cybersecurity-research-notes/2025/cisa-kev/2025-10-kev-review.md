# October 2025 KEV Review

## Summary

This note reviews representative vulnerabilities added to CISA's Known Exploited Vulnerabilities catalog during October 2025. The goal is to translate KEV activity into practical SOC, vulnerability management, and incident response thinking.

Primary themes for this month: **Microsoft enterprise platform exposure; web application exploitation leading to code execution**.

## Representative KEV Entries

| Date Added | CVE | Vendor | Product | Vulnerability | Ransomware Use |
| --- | --- | --- | --- | --- | --- |
| 2025-10-30 | CVE-2025-41244 | Broadcom | VMware Aria Operations and VMware Tools | Broadcom VMware Aria Operations and VMware Tools Privilege Defined with Unsafe Actions Vulnerability | Unknown |
| 2025-10-30 | CVE-2025-24893 | XWiki | Platform | XWiki Platform Eval Injection Vulnerability | Unknown |
| 2025-10-28 | CVE-2025-6204 | Dassault Systèmes | DELMIA Apriso | Dassault Systèmes DELMIA Apriso Code Injection Vulnerability | Unknown |
| 2025-10-28 | CVE-2025-6205 | Dassault Systèmes | DELMIA Apriso | Dassault Systèmes DELMIA Apriso Missing Authorization Vulnerability | Unknown |
| 2025-10-24 | CVE-2025-54236 | Adobe | Commerce and Magento | Adobe Commerce and Magento Improper Input Validation Vulnerability | Unknown |
| 2025-10-24 | CVE-2025-59287 | Microsoft | Windows | Microsoft Windows Server Update Service (WSUS) Deserialization of Untrusted Data Vulnerability | Unknown |

## Analyst Takeaways

- CVE-2025-41244 / Broadcom VMware Aria Operations and VMware Tools: Broadcom VMware Aria Operations and VMware Tools contain a privilege defined with unsafe actions vulnerability. A malicious local actor with non-administrative privileges having access to a VM with VMware Tools installed and managed by Aria Operations with SDMP enabled may exploit this vulnerability to escalate privileges to root on the same VM.
- CVE-2025-24893 / XWiki Platform: XWiki Platform contains an eval injection vulnerability that could allow any guest to perform arbitrary remote code execution through a request to SolrSearch.
- CVE-2025-6204 / Dassault Systèmes DELMIA Apriso: Dassault Systèmes DELMIA Apriso contains a code injection vulnerability that could allow an attacker to execute arbitrary code.
- CVE-2025-6205 / Dassault Systèmes DELMIA Apriso: Dassault Systèmes DELMIA Apriso contains a missing authorization vulnerability that could allow an attacker to gain privileged access to the application.
- CVE-2025-54236 / Adobe Commerce and Magento: Adobe Commerce and Magento Open Source contain an improper input validation vulnerability that could allow an attacker to take over customer accounts through the Commerce REST API.
- CVE-2025-59287 / Microsoft Windows: Microsoft Windows Server Update Service (WSUS) contains a deserialization of untrusted data vulnerability that allows for remote code execution.

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