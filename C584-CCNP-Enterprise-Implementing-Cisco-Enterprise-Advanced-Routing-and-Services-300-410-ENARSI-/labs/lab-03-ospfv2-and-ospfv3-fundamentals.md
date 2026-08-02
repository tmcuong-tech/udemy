# Lab 03: OSPFv2 and OSPFv3 Fundamentals

## Area

OSPF

## Objective

Configure OSPFv2 for IPv4 and OSPFv3 for IPv6, then verify neighbors, LSDB, and routing behavior.

## Scenario

The enterprise is standardizing OSPF across IPv4 and IPv6 networks and needs consistent area design and verification procedures.

## Tasks

1. Configure OSPFv2 on IPv4 interfaces.
2. Configure router IDs explicitly.
3. Place routers into area 0 and one nonbackbone area.
4. Verify neighbor states.
5. Review the OSPF database.
6. Configure OSPFv3 for IPv6.
7. Verify IPv6 OSPF neighbors and routes.
8. Test end-to-end IPv4 and IPv6 connectivity.
9. Record key differences between OSPFv2 and OSPFv3 configuration.

## Validation

- OSPFv2 and OSPFv3 neighbors reach full adjacency where expected.
- LSDB entries are visible.
- IPv4 and IPv6 routes are installed.
- Connectivity tests succeed.

## Troubleshooting Prompts

1. What causes OSPF neighbors to remain in INIT or EXSTART?
2. Why is router ID important?
3. What information does the LSDB contain?
4. How does OSPFv3 differ from OSPFv2?

## Cleanup

Save outputs for comparison with Lab 04.
