# Lab 08: Advanced BGP and MP-BGP

## Area

BGP

## Objective

Configure advanced BGP filtering and policy, then explore MP-BGP address families.

## Scenario

The enterprise needs precise BGP policy control and must understand how multiprotocol BGP carries multiple address families.

## Tasks

1. Configure prefix lists for inbound and outbound filtering.
2. Apply route maps to BGP neighbors.
3. Set and match BGP communities.
4. Configure route filtering to allow only selected prefixes.
5. Review soft reconfiguration or route refresh behavior.
6. Configure an IPv6 or VPN-related address family if supported by the lab platform.
7. Activate neighbors under the address family.
8. Verify address-family-specific routes.
9. Introduce a policy error and troubleshoot route advertisement.

## Validation

- Prefix filtering behaves as expected.
- Route maps modify or filter advertised routes.
- Communities are set or matched correctly.
- MP-BGP address-family behavior is understood.

## Troubleshooting Prompts

1. Why can a BGP neighbor be up but exchange no routes?
2. How do prefix lists differ from ACLs in routing policy?
3. Why are route maps often paired with prefix lists?
4. What does address-family activation control?

## Cleanup

Remove lab-only BGP policies or save the final configuration for review.
