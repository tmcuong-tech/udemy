# Lab 04: OSPF Optimization and Troubleshooting

## Area

OSPF

## Objective

Optimize and troubleshoot OSPF with stub areas, summarization, authentication, and route filtering.

## Scenario

The network team wants to reduce OSPF route noise in branch areas and secure neighbor relationships while keeping troubleshooting procedures consistent.

## Tasks

1. Convert a branch area to a stub area.
2. Convert a branch area to a totally stubby area if supported by your platform.
3. Configure OSPF summarization at an ABR.
4. Configure OSPF authentication.
5. Apply route filtering where appropriate.
6. Introduce an OSPF fault such as area mismatch, timer mismatch, MTU mismatch, or authentication mismatch.
7. Use `show ip ospf neighbor`, `show ip ospf interface`, `show ip ospf database`, and logs to find the issue.
8. Restore the correct configuration.

## Validation

- Stub or totally stubby behavior is visible in routing tables.
- Summary routes appear at the correct boundary.
- Authenticated adjacencies form successfully.
- The introduced fault is identified and resolved.

## Troubleshooting Prompts

1. What routes should a stub area suppress?
2. Where can OSPF summarization be configured?
3. Which mismatches prevent full adjacency?
4. What command shows OSPF interface timers?

## Cleanup

Restore the baseline or save the completed OSPF design for redistribution labs.
