# Lab 11: DHCP, IPv6 First Hop Security, and Router Hardening

## Area

Infrastructure Services and Security

## Objective

Configure and troubleshoot infrastructure services and router security features.

## Scenario

Branch users need addressing services, secure router management, infrastructure logging, and protection against common first-hop and control-plane risks.

## Tasks

1. Configure DHCP server or relay behavior.
2. Verify DHCP address assignment or relay forwarding.
3. Troubleshoot a DHCP failure caused by missing helper address, ACL, or routing issue.
4. Review IPv6 first hop security tools such as RA Guard and DHCPv6 Guard where supported.
5. Configure basic router hardening: secure passwords, SSH, login banners, and management ACLs.
6. Configure AAA concepts if a local or simulated server is available.
7. Configure SNMP and Syslog settings for monitoring.
8. Configure or review control plane policing concepts.
9. Verify logs and management reachability.

## Validation

- DHCP behavior is working or accurately diagnosed.
- Router management is restricted.
- Syslog or SNMP destination is configured where available.
- IPv6 first hop security controls are explained.
- CoPP purpose is understood.

## Troubleshooting Prompts

1. Why does DHCP need a helper address across routed interfaces?
2. What problem does RA Guard reduce?
3. Why should management access be restricted by ACL?
4. What traffic should control plane policing protect?

## Cleanup

Remove lab-only users, SNMP strings, and temporary ACLs if they are not required.
