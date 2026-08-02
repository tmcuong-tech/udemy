# Lab 07: IBGP, EBGP, and BGP Path Selection

## Area

BGP

## Objective

Configure IBGP and EBGP sessions, advertise networks, and analyze BGP best path selection.

## Scenario

The enterprise connects to multiple routing domains and must control how routes are learned, advertised, and selected.

## Tasks

1. Configure EBGP between an enterprise edge and provider simulation router.
2. Configure IBGP between enterprise routers.
3. Advertise loopback and internal network prefixes.
4. Verify neighbor state with `show ip bgp summary`.
5. Inspect the BGP table with `show ip bgp`.
6. Modify attributes such as weight, local preference, AS path, MED, or next hop where appropriate.
7. Observe best path changes.
8. Test reachability.
9. Introduce a BGP issue such as wrong AS, missing update source, TTL problem, or next-hop reachability problem.
10. Troubleshoot and fix the issue.

## Validation

- IBGP and EBGP peers are established.
- Intended routes appear in the BGP table.
- Best path selection can be explained.
- The BGP fault is resolved using evidence.

## Troubleshooting Prompts

1. What is the difference between IBGP and EBGP neighbor behavior?
2. Why might loopback peering require update source and multihop?
3. Which attributes are evaluated early in best path selection?
4. Why can next-hop reachability break BGP routing?

## Cleanup

Save the BGP baseline for Lab 08.
