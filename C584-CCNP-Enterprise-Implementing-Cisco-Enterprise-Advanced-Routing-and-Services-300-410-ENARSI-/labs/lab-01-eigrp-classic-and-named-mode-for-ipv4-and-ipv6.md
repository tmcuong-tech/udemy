# Lab 01: EIGRP Classic and Named Mode for IPv4 and IPv6

## Area

EIGRP

## Objective

Configure and verify EIGRP for IPv4 and IPv6 using classic mode and named mode.

## Scenario

Your enterprise network is migrating from a legacy EIGRP configuration to a standardized named-mode design while preserving IPv4 and IPv6 reachability.

## Tasks

1. Build a four-router topology with loopback interfaces.
2. Configure IPv4 addressing and IPv6 addressing on all transit links.
3. Configure EIGRP classic mode for IPv4 on one part of the topology.
4. Verify neighbors with `show ip eigrp neighbors`.
5. Verify the topology table with `show ip eigrp topology`.
6. Configure named-mode EIGRP for IPv4 and IPv6 on another part of the topology.
7. Advertise loopbacks into EIGRP.
8. Verify IPv4 and IPv6 route installation.
9. Test end-to-end reachability with ping and traceroute.

## Validation

- EIGRP neighbors are established.
- Loopback routes are visible in routing tables.
- The topology table shows successor routes.
- IPv4 and IPv6 reachability succeeds.

## Troubleshooting Prompts

1. What happens if autonomous system numbers do not match?
2. What happens if passive interfaces are applied incorrectly?
3. What output confirms a feasible successor?
4. How does named mode organize address families?

## Cleanup

Save the completed configuration or restore the baseline for Lab 02.
