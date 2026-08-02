# August 2025 KEV Review

## Summary

This note reviews representative vulnerabilities added to CISA's Known Exploited Vulnerabilities catalog during August 2025. The goal is to translate KEV activity into practical SOC, vulnerability management, and incident response thinking.

Primary themes for this month: **Microsoft enterprise platform exposure; edge appliance and network device risk; endpoint and browser exploitation; web application exploitation leading to code execution; identity and access control weakness; developer tooling and application framework exposure**.

## Representative KEV Entries

| Date Added | CVE | Vendor | Product | Vulnerability | Ransomware Use |
| --- | --- | --- | --- | --- | --- |
| 2025-08-29 | CVE-2025-57819 | Sangoma | FreePBX | Sangoma FreePBX Authentication Bypass Vulnerability | Unknown |
| 2025-08-26 | CVE-2025-7775 | Citrix | NetScaler | Citrix NetScaler Memory Overflow Vulnerability | Unknown |
| 2025-08-25 | CVE-2025-48384 | Git | Git | Git Link Following Vulnerability | Unknown |
| 2025-08-25 | CVE-2024-8068 | Citrix | Session Recording | Citrix Session Recording Improper Privilege Management Vulnerability | Unknown |
| 2025-08-25 | CVE-2024-8069 | Citrix | Session Recording | Citrix Session Recording Deserialization of Untrusted Data Vulnerability | Unknown |
| 2025-08-21 | CVE-2025-43300 | Apple | iOS, iPadOS, and macOS | Apple iOS, iPadOS, and macOS Out-of-Bounds Write Vulnerability | Unknown |

## Analyst Takeaways

- CVE-2025-57819 / Sangoma FreePBX: Sangoma FreePBX contains an authentication bypass vulnerability due to insufficiently sanitized user-supplied data allows unauthenticated access to FreePBX Administrator leading to arbitrary database manipulation and remote code execution.
- CVE-2025-7775 / Citrix NetScaler: Citrix NetScaler ADC and NetScaler Gateway contain a memory overflow vulnerability that could allow for remote code execution and/or denial of service.
- CVE-2025-48384 / Git Git: Git contains a link following vulnerability that stems from Git’s inconsistent handling of carriage return characters in configuration files.
- CVE-2024-8068 / Citrix Session Recording: Citrix Session Recording contains an improper privilege management vulnerability that could allow for privilege escalation to NetworkService Account access. An attacker must be an authenticated user in the same Windows Active Directory domain as the session recording server domain.
- CVE-2024-8069 / Citrix Session Recording: Citrix Session Recording contains a deserialization of untrusted data vulnerability that allows limited remote code execution with privilege of a NetworkService Account access. Attacker must be an authenticated user on the same intranet as the session recording server.
- CVE-2025-43300 / Apple iOS, iPadOS, and macOS: Apple iOS, iPadOS, and macOS contain an out-of-bounds write vulnerability in the Image I/O framework.

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