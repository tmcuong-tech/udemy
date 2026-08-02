# Lab Tools and Access

## Required Tools

- Cisco IOS XE lab devices or images
- Terminal emulator
- Console, SSH, or telnet access in a closed lab
- Text editor for configuration notes
- Diagramming tool or paper topology worksheet

## Recommended Platforms

- Cisco Modeling Labs
- EVE-NG
- GNS3
- Instructor-provided Cisco rack
- Cisco DNA Center demo or instructor screenshots for Assurance review

## Suggested Device Roles

- R1 and R2: core or distribution routers
- R3 and R4: branch routers
- R5 and R6: edge or provider simulation routers
- SW1 and SW2: optional access/distribution switches

## Common Verification Commands

```text
show ip route
show ipv6 route
show ip protocols
show running-config
show logging
ping
traceroute
show access-lists
show route-map
show ip sla statistics
```

## Reset Guidance

Save a clean baseline before each lab. If a troubleshooting exercise becomes tangled, reload from the baseline and reapply only the required fault.
