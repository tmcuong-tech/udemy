# April 2026 KEV Review

## Summary

This note reviews representative vulnerabilities added to CISA's Known Exploited Vulnerabilities catalog during April 2026. The goal is to translate KEV activity into practical SOC, vulnerability management, and incident response thinking.

Primary themes for this month: **Microsoft enterprise platform exposure; web application exploitation leading to code execution; identity and access control weakness; developer tooling and application framework exposure**.

## Representative KEV Entries

| Date Added | CVE | Vendor | Product | Vulnerability | Ransomware Use |
| --- | --- | --- | --- | --- | --- |
| 2026-04-30 | CVE-2026-41940 | WebPros | cPanel & WHM and WP2 (WordPress Squared) | WebPros cPanel & WHM and WP2 (WordPress Squared) Missing Authentication for Critical Function Vulnerability | Known |
| 2026-04-28 | CVE-2024-1708 | ConnectWise | ScreenConnect | ConnectWise ScreenConnect Path Traversal Vulnerability | Known |
| 2026-04-28 | CVE-2026-32202 | Microsoft | Windows | Microsoft Windows Protection Mechanism Failure Vulnerability | Unknown |
| 2026-04-24 | CVE-2025-29635 | D-Link | DIR-823X | D-Link DIR-823X Command Injection Vulnerability | Unknown |
| 2026-04-24 | CVE-2024-7399 | Samsung | MagicINFO 9 Server | Samsung MagicINFO 9 Server Path Traversal Vulnerability | Unknown |
| 2026-04-24 | CVE-2024-57728 | SimpleHelp  | SimpleHelp | SimpleHelp Path Traversal Vulnerability | Known |

## Analyst Takeaways

- CVE-2026-41940 / WebPros cPanel & WHM and WP2 (WordPress Squared): WebPros cPanel & WHM (WebHost Manager) and WP2 (WordPress Squared) contain an authentication bypass vulnerability in the login flow that allows unauthenticated remote attackers to gain unauthorized access to the control panel.
- CVE-2024-1708 / ConnectWise ScreenConnect: ConnectWise ScreenConnect contains a path traversal vulnerability which could allow an attacker to execute remote code or directly impact confidential data and critical systems.
- CVE-2026-32202 / Microsoft Windows: Microsoft Windows Shell contains a protection mechanism failure vulnerability that allows an unauthorized attacker to perform spoofing over a network.
- CVE-2025-29635 / D-Link DIR-823X: D-Link DIR-823X contains a command injection vulnerability that allows an authorized attacker to execute arbitrary commands on remote devices by sending a POST request to /goform/set_prohibiting via the corresponding function. The impacted product could be end-of-life (EoL) and/or end-of-service (EoS). Users should discontinue product utilization.
- CVE-2024-7399 / Samsung MagicINFO 9 Server: Samsung MagicINFO 9 Server contains a path traversal vulnerability that could allow an attacker to write arbitrary files as system authority.
- CVE-2024-57728 / SimpleHelp  SimpleHelp: SimpleHelp contains a path traversal vulnerability that allows admin users to upload arbitrary files anywhere on the file system by uploading a crafted zip file (i.e. zip slip). This can be exploited to execute arbitrary code on the host in the context of the SimpleHelp server user.

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