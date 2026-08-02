# Lab 05: Routing Protocol Redistribution and Route Maps

## Area

Redistribution

## Objective

Implement and troubleshoot route redistribution using route maps, filtering mechanisms, metrics, and tags.

## Scenario

One part of the network uses EIGRP and another uses OSPF. Routes must be exchanged safely without loops or uncontrolled route leakage.

## Tasks

1. Build or load a topology with EIGRP on one side and OSPF on another.
2. Configure one-way redistribution.
3. Configure mutual redistribution.
4. Set appropriate seed metrics.
5. Use prefix lists or ACLs to match selected routes.
6. Use route maps to permit, deny, set metrics, and set tags.
7. Verify redistributed routes in routing tables.
8. Introduce a redistribution issue such as missing metric, wrong route map sequence, or route feedback.
9. Troubleshoot and correct the issue.

## Validation

- Only intended routes are redistributed.
- Metrics are appropriate for the receiving protocol.
- Route tags are visible where supported.
- Routing loops or route feedback are prevented.

## Troubleshooting Prompts

1. Why do some protocols require a seed metric?
2. How can route tags prevent feedback loops?
3. What happens when a route map has no matching permit sequence?
4. Which commands confirm redistributed route origin?

## Cleanup

Save the final redistribution policy and remove lab-only route leaks.
