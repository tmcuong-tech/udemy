# Lab 06: Policy-Based Routing and IP SLA

## Area

Path Control

## Objective

Implement traffic steering using policy-based routing and IP SLA tracking.

## Scenario

Selected application traffic should use a preferred WAN link when it is healthy and fall back to normal routing when the link fails.

## Tasks

1. Define normal routing behavior using the existing routing table.
2. Create an ACL that matches selected traffic.
3. Create a route map for policy-based routing.
4. Set a next hop for matched traffic.
5. Apply the policy to the correct inbound interface.
6. Configure IP SLA to test reachability of the preferred next hop.
7. Configure tracking for the IP SLA operation.
8. Tie the route map or route decision to tracking where supported.
9. Test traffic during normal and failed-path conditions.

## Validation

- Matched traffic follows the policy path.
- Unmatched traffic follows normal routing.
- IP SLA reports reachability status.
- Failover behavior works as designed.

## Troubleshooting Prompts

1. Why is PBR applied inbound?
2. How can PBR create asymmetric routing?
3. What does IP SLA measure in this design?
4. What happens if the route map matches too broadly?

## Cleanup

Remove PBR and IP SLA configuration if it is not needed for later labs.
