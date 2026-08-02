# Lab 10: Dynamic Multipoint VPN

## Area

VPN Services

## Objective

Implement and troubleshoot Dynamic Multipoint VPN concepts using hub-and-spoke design.

## Scenario

The enterprise wants scalable branch connectivity without building a separate static tunnel between every pair of sites.

## Tasks

1. Identify hub and spoke routers.
2. Configure tunnel interfaces.
3. Configure GRE tunnel parameters.
4. Configure NHRP hub and spoke settings.
5. Review IPsec protection concepts if supported by the lab platform.
6. Configure routing over the tunnel.
7. Verify NHRP mappings.
8. Test hub-to-spoke and spoke-to-spoke reachability.
9. Compare DMVPN phase behavior conceptually.
10. Introduce a fault such as incorrect NHRP mapping, tunnel key mismatch, routing issue, or IPsec mismatch.
11. Troubleshoot and restore connectivity.

## Validation

- Spokes register with the hub.
- Tunnel routes are learned.
- Expected traffic paths are observed.
- The introduced fault is identified and resolved.

## Troubleshooting Prompts

1. What role does NHRP play in DMVPN?
2. Why is GRE used?
3. How does routing interact with DMVPN overlays?
4. What changes between DMVPN phases?

## Cleanup

Save outputs or restore the baseline for infrastructure services.
