# Lab 02: EIGRP Optimization and Troubleshooting

## Area

EIGRP

## Objective

Optimize EIGRP using stub routing, summarization, default routing, load balancing, and authentication, then troubleshoot common failures.

## Scenario

Branch routers should not become transit routers. The routing table must be simplified, links should use load balancing where appropriate, and neighbor adjacencies must be protected.

## Tasks

1. Configure EIGRP stub routing on a branch router.
2. Verify query reduction behavior conceptually and through topology outputs.
3. Configure manual route summarization at an aggregation point.
4. Inject or advertise a default route to a branch.
5. Tune variance for unequal-cost load balancing where the topology supports it.
6. Configure EIGRP authentication.
7. Introduce one fault such as mismatched authentication, missing network statement, or passive interface.
8. Troubleshoot the issue using neighbor, topology, route, and log outputs.
9. Restore the correct configuration.

## Validation

- Stub router is marked as stub.
- Summary route appears where expected.
- Default route is received by branch routers.
- Authentication-protected neighbors form successfully.
- The introduced fault is identified and fixed.

## Troubleshooting Prompts

1. Which command confirms stub status?
2. Why might a summary route create a null route?
3. How does variance affect load balancing?
4. What symptoms appear with authentication mismatch?

## Cleanup

Document the final verification output and return to baseline.
