# Learner Guide: C584 CCNP Enterprise ENARSI

This guide supports a 5-day CCNP Enterprise ENARSI course focused on advanced enterprise routing and services. The labs follow Cisco's ENARSI training objectives and lab outline for the 300-410 ENARSI exam.

## Learning Outcomes

By the end of the course, you will be able to:

- Configure, optimize, verify, and troubleshoot EIGRP for IPv4 and IPv6.
- Configure, optimize, verify, and troubleshoot OSPFv2 and OSPFv3.
- Implement route redistribution with route maps, filtering, metrics, and loop-prevention controls.
- Implement path control using policy-based routing and IP SLA.
- Configure and troubleshoot IBGP, EBGP, BGP attributes, and MP-BGP address families.
- Explain MPLS and MPLS L3 VPN concepts and configure VRF-Lite.
- Implement and troubleshoot DMVPN.
- Configure and troubleshoot infrastructure services such as DHCP, Syslog, SNMP, AAA, and CoPP.
- Apply IPv6 first hop security and router hardening concepts.
- Use a structured troubleshooting method and interpret Cisco DNA Center Assurance evidence.

## Course Flow

| Day | Focus | Labs |
|---|---|---|
| Day 1 | EIGRP and OSPF foundations | Labs 01-04 |
| Day 2 | Redistribution and path control | Labs 05-06 |
| Day 3 | BGP and MP-BGP | Labs 07-08 |
| Day 4 | MPLS, VRF-Lite, DMVPN, infrastructure services | Labs 09-11 |
| Day 5 | Troubleshooting and readiness | Lab 12 plus review |

## Recommended Prerequisites

Before starting, you should be comfortable with:

- IPv4 and IPv6 addressing
- VLANs and Layer 2 switching basics
- Static routing
- EIGRP, OSPF, and BGP fundamentals
- ACLs, SNMP, DHCP, Syslog, AAA, and basic device security
- Basic Cisco IOS CLI navigation

## Lab Environment Setup

### Step 1: Choose a Lab Platform

Use one of the following:

- Cisco Modeling Labs
- EVE-NG
- GNS3
- Instructor-provided physical or virtual rack
- Packet Tracer for limited conceptual practice where supported

### Step 2: Use a Common Addressing Pattern

Use consistent lab addressing unless your instructor provides a topology:

```text
Loopbacks: 10.<lab>.<router>.1/32
Point-to-point links: 10.<lab>.<link>.0/30
IPv6 loopbacks: 2001:db8:<lab>:<router>::1/128
IPv6 links: 2001:db8:<lab>:<link>::/64
```

### Step 3: Save Baseline Configurations

Before each lab:

1. Save the startup configuration.
2. Export the baseline configuration to a text file.
3. Confirm interface status and IP addressing.
4. Confirm device reachability.
5. Record the intended routing protocol and topology goal.

### Step 4: Use a Troubleshooting Journal

For each lab, record:

- Lab objective
- Topology diagram
- Initial symptom or target behavior
- Commands used
- Output evidence
- Root cause if troubleshooting
- Final validation
- Exam takeaway

## Domain Study Path

### EIGRP

Complete Labs 01 and 02.

You should be able to verify neighbors, topology entries, successor and feasible successor routes, stub behavior, summarization, default routing, unequal-cost load balancing, and authentication.

Checkpoint questions:

1. What makes an EIGRP route a feasible successor?
2. How does stub routing reduce query scope?
3. What issues break EIGRP neighbor adjacency?
4. How do classic mode and named mode differ operationally?

### OSPF

Complete Labs 03 and 04.

You should be able to configure OSPFv2 and OSPFv3, interpret the LSDB, design areas, configure stub areas, summarize routes, authenticate neighbors, and isolate adjacency and route issues.

Checkpoint questions:

1. What states should an OSPF adjacency pass through?
2. What is stored in the link-state database?
3. How do stub and totally stubby areas reduce routing information?
4. Which mismatches commonly prevent adjacency?

### Redistribution and Path Control

Complete Labs 05 and 06.

You should be able to redistribute between routing domains safely, apply route maps and filtering, tag routes, set metrics, prevent loops, and steer selected traffic using PBR and IP SLA.

Checkpoint questions:

1. Why is redistribution risky without filtering?
2. When should route tags be used?
3. How does PBR override normal destination-based forwarding?
4. How does IP SLA help make path control conditional?

### BGP and MP-BGP

Complete Labs 07 and 08.

You should be able to form IBGP and EBGP sessions, advertise networks, interpret BGP path attributes, influence best path selection, filter prefixes, use communities, and understand MP-BGP address families.

Checkpoint questions:

1. Why does IBGP need a full mesh or route reflection?
2. Which BGP attributes commonly influence path selection?
3. How do prefix lists and route maps work together?
4. Why does MP-BGP use address families?

### MPLS, VRF-Lite, and DMVPN

Complete Labs 09 and 10.

You should understand MPLS forwarding concepts, MPLS L3 VPN architecture, VRFs, route distinguishers, route targets, VRF-Lite, DMVPN components, NHRP, GRE, IPsec concepts, and routing over overlays.

Checkpoint questions:

1. What problem does VRF-Lite solve?
2. How do route distinguishers and route targets differ conceptually?
3. What roles do hub, spoke, NHRP, GRE, and IPsec play in DMVPN?
4. How do DMVPN phases affect spoke-to-spoke traffic?

### Infrastructure Services, Security, and Assurance

Complete Labs 11 and 12.

You should be able to troubleshoot DHCP, Syslog, SNMP, AAA, ACLs, CoPP, IPv6 first hop security, router hardening, and use assurance-style evidence for troubleshooting.

Checkpoint questions:

1. What breaks DHCP relay across routed networks?
2. Which IPv6 first hop attacks do RA Guard and related controls reduce?
3. Why does CoPP protect the control plane?
4. How does assurance data complement CLI troubleshooting?

## Lab Reporting Template

```text
Lab:
Topology:
Objective:
Relevant protocols/services:
Configuration changes:
Verification commands:
Observed output:
Issue found:
Resolution:
Exam takeaway:
```

## Core Verification Commands

```text
show ip interface brief
show ipv6 interface brief
show ip route
show ipv6 route
show ip protocols
show running-config
show logging
ping
traceroute
debug condition
undebug all
```

Use protocol-specific commands in the individual labs.

## References

- [Cisco ENARSI Course Overview](https://www.cisco.com/site/us/en/learn/training-certifications/training/courses/enarsi.html)
- [Course Registration](https://www.tertiarycourses.com.sg/ccnp-enterprise-implementing-cisco-enterprise-advanced-routing-and-services-300-410-enarsi-exam-prep.html)
