# Lab 09: MPLS Concepts, MPLS L3 VPN, and VRF-Lite

## Area

MPLS and VRF

## Objective

Explain MPLS and MPLS L3 VPN concepts, then configure VRF-Lite to separate routing tables.

## Scenario

The enterprise must support separate customer or business-unit routing domains while understanding service provider MPLS VPN concepts.

## Tasks

1. Explain MPLS label switching at a high level.
2. Identify MPLS provider, provider edge, and customer edge roles.
3. Explain route distinguishers and route targets conceptually.
4. Configure two VRFs on a router.
5. Assign interfaces to the correct VRFs.
6. Configure routing within each VRF.
7. Verify separate routing tables with `show ip route vrf`.
8. Test reachability inside each VRF.
9. Confirm traffic cannot cross VRFs unless route leaking is configured.

## Validation

- VRF routing tables are separate.
- Interfaces belong to intended VRFs.
- Each VRF has independent routes.
- Learners can explain MPLS L3 VPN concepts even if full MPLS is simulated.

## Troubleshooting Prompts

1. What problem does a VRF solve?
2. Why is a route distinguisher needed in MPLS VPNs?
3. What does a route target control?
4. What happens when an interface is moved into a VRF?

## Cleanup

Remove VRF-Lite configuration if the next lab requires a clean routing table.
