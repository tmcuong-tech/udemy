# March 2026 KEV Review

## Summary

This note reviews representative vulnerabilities added to CISA's Known Exploited Vulnerabilities catalog during March 2026. The goal is to translate KEV activity into practical SOC, vulnerability management, and incident response thinking.

Primary themes for this month: **edge appliance and network device risk; endpoint and browser exploitation; web application exploitation leading to code execution; developer tooling and application framework exposure**.

## Representative KEV Entries

| Date Added | CVE | Vendor | Product | Vulnerability | Ransomware Use |
| --- | --- | --- | --- | --- | --- |
| 2026-03-30 | CVE-2026-3055 | Citrix | NetScaler | Citrix NetScaler Out-of-Bounds Read Vulnerability | Unknown |
| 2026-03-27 | CVE-2025-53521 | F5 | BIG-IP | F5 BIG-IP Stack-Based Buffer Overflow Vulnerability | Unknown |
| 2026-03-26 | CVE-2026-33634 | Aquasecurity | Trivy | Aquasecurity Trivy Embedded Malicious Code Vulnerability | Unknown |
| 2026-03-25 | CVE-2026-33017 | Langflow | Langflow | Langflow Code Injection Vulnerability | Unknown |
| 2026-03-20 | CVE-2025-32432 | Craft CMS | Craft CMS | Craft CMS Code Injection Vulnerability | Unknown |
| 2026-03-20 | CVE-2025-54068 | Laravel | Livewire | Laravel Livewire Code Injection Vulnerability | Unknown |

## Analyst Takeaways

- CVE-2026-3055 / Citrix NetScaler: Citrix NetScaler ADC (formerly Citrix ADC), NetScaler Gateway (formerly Citrix Gateway) and NetScaler ADC FIPS and NDcPP contain an out-of-bounds reads vulnerability when configured as a SAML IDP leading to memory overread.
- CVE-2025-53521 / F5 BIG-IP: F5 BIG-IP APM contains a stack-based buffer overflow vulnerability that could allow a threat actor to achieve remote code execution.
- CVE-2026-33634 / Aquasecurity Trivy: Aquasecurity Trivy contains an embedded malicious code vulnerability that could allow an attacker to gain access to everything in the CI/CD environment, including all tokens, SSH keys, cloud credentials, database passwords, and any sensitive configuration in memory.
- CVE-2026-33017 / Langflow Langflow: Langflow contains a code injection vulnerability that could allow building public flows without requiring authentication.
- CVE-2025-32432 / Craft CMS Craft CMS: Craft CMS contains a code injection vulnerability that allows a remote attacker to execute arbitrary code.
- CVE-2025-54068 / Laravel Livewire: Laravel Livewire contain a code injection vulnerability that could allow unauthenticated attackers to achieve remote command execution in specific scenarios.

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