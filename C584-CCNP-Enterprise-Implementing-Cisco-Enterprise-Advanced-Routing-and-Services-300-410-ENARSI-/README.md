# C584 CCNP Enterprise: Implementing Cisco Enterprise Advanced Routing and Services (300-410 ENARSI)

Hands-on labs for learners preparing for Cisco 300-410 ENARSI: Implementing Cisco Enterprise Advanced Routing and Services.

## Course Information

- **Course Code:** C584
- **Course Title:** CCNP Enterprise: Implementing Cisco Enterprise Advanced Routing and Services (300-410 ENARSI)
- **Duration:** 5 days / 37.5 hours
- **Level:** Intermediate
- **Course Registration:** [CCNP Enterprise ENARSI Training](https://www.tertiarycourses.com.sg/ccnp-enterprise-implementing-cisco-enterprise-advanced-routing-and-services-300-410-enarsi-exam-prep.html)
- **Reference:** [Cisco ENARSI Course Overview](https://www.cisco.com/site/us/en/learn/training-certifications/training/courses/enarsi.html)

## Labs

| Domain | Lab | Title | Focus Area |
|---|---:|---|---|
| EIGRP | 01 | EIGRP Classic and Named Mode for IPv4 and IPv6 | Neighbor adjacencies, topology table, metrics, verification |
| EIGRP | 02 | EIGRP Optimization and Troubleshooting | Stub routing, summarization, default routing, load balancing, authentication, fault isolation |
| OSPF | 03 | OSPFv2 and OSPFv3 Fundamentals | Areas, LSDB, neighbors, IPv4/IPv6 routing, verification |
| OSPF | 04 | OSPF Optimization and Troubleshooting | Stub areas, summarization, authentication, route filtering, issue diagnosis |
| Redistribution | 05 | Routing Protocol Redistribution and Route Maps | Mutual redistribution, route filtering, tags, metrics, loop prevention |
| Path Control | 06 | Policy-Based Routing and IP SLA | PBR, next-hop tracking, IP SLA, route tracking, traffic steering |
| BGP | 07 | IBGP, EBGP, and BGP Path Selection | Neighbor relationships, attributes, best path, route advertisement |
| BGP | 08 | Advanced BGP and MP-BGP | Route filtering, prefix lists, communities, MP-BGP address families |
| MPLS and VRF | 09 | MPLS Concepts, MPLS L3 VPN, and VRF-Lite | MPLS forwarding concepts, route distinguishers, route targets, VRF-Lite |
| VPN Services | 10 | Dynamic Multipoint VPN | DMVPN phases, NHRP, GRE, IPsec concepts, routing over DMVPN |
| Infrastructure Services and Security | 11 | DHCP, IPv6 First Hop Security, and Router Hardening | DHCP relay, snooping concepts, RA Guard, ACLs, AAA, SNMP, Syslog, CoPP |
| Troubleshooting and Assurance | 12 | ENARSI Troubleshooting Capstone with Cisco DNA Center Assurance | Structured troubleshooting, infrastructure services, assurance workflows, final readiness |

## Learner Guide

Start with the detailed step-by-step guide:

[LG-CCNP-Enterprise-ENARSI.md](LG-CCNP-Enterprise-ENARSI.md)

## Lab Requirements

- Cisco IOS XE lab environment, Cisco Modeling Labs, EVE-NG, GNS3, Packet Tracer where suitable, or instructor-provided rack
- 4 to 8 routers or virtual routers for routing labs
- Optional Layer 2 switches for service/security tasks
- Console or SSH access to all lab devices
- Text editor for configurations and troubleshooting notes
- Optional Cisco DNA Center or instructor screenshots/simulation for Assurance workflows

## Repository Structure

```text
.
|-- README.md
|-- LG-CCNP-Enterprise-ENARSI.md
`-- labs/
    |-- README.md
    |-- tools.md
    |-- lab-01-eigrp-classic-and-named-mode-for-ipv4-and-ipv6.md
    |-- lab-02-eigrp-optimization-and-troubleshooting.md
    |-- lab-03-ospfv2-and-ospfv3-fundamentals.md
    |-- lab-04-ospf-optimization-and-troubleshooting.md
    |-- lab-05-routing-protocol-redistribution-and-route-maps.md
    |-- lab-06-policy-based-routing-and-ip-sla.md
    |-- lab-07-ibgp-ebgp-and-bgp-path-selection.md
    |-- lab-08-advanced-bgp-and-mp-bgp.md
    |-- lab-09-mpls-concepts-mpls-l3-vpn-and-vrf-lite.md
    |-- lab-10-dynamic-multipoint-vpn.md
    |-- lab-11-dhcp-ipv6-first-hop-security-and-router-hardening.md
    `-- lab-12-enarsi-troubleshooting-capstone-with-cisco-dna-center-assurance.md
```

## Suggested GitHub About Description

12 hands-on CCNP Enterprise ENARSI labs covering EIGRP, OSPF, redistribution, route maps, PBR, IP SLA, BGP, MP-BGP, MPLS concepts, VRF-Lite, DMVPN, DHCP, IPv6 first hop security, router hardening, infrastructure services, troubleshooting, and Cisco DNA Center Assurance.
