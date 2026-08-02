# Lab 12: ENARSI Troubleshooting Capstone with Cisco DNA Center Assurance

## Area

Troubleshooting and Assurance

## Objective

Use a structured troubleshooting method to diagnose advanced routing and services issues, then interpret assurance-style evidence.

## Scenario

Multiple faults have been introduced into an enterprise routing environment. Users report intermittent reachability, slow failover, and missing routes. You must isolate and resolve the problems.

## Tasks

### Task 1: Build the Troubleshooting Plan

1. Record the reported symptom.
2. Identify the affected source, destination, protocol, and time window.
3. Draw the expected traffic path.
4. List the routing protocols and services involved.
5. Decide which outputs to collect first.

### Task 2: Diagnose Routing Issues

1. Check interface status.
2. Check routing tables.
3. Check EIGRP, OSPF, or BGP neighbors.
4. Check redistribution policy.
5. Check route maps, prefix lists, and ACLs.
6. Check path control or IP SLA state.

### Task 3: Diagnose Services and Security Issues

1. Check DHCP relay or server behavior.
2. Check Syslog and SNMP configuration.
3. Check AAA and management access.
4. Check CoPP or ACL impact.
5. Check IPv6 first hop security settings where applicable.

### Task 4: Interpret Assurance Evidence

1. Review Cisco DNA Center Assurance concepts.
2. Identify client, device, path, and application health indicators.
3. Match assurance symptoms to possible CLI checks.
4. Explain how assurance data changes troubleshooting priority.

### Task 5: Present Findings

Prepare a short incident report:

- Symptom
- Scope
- Root cause
- Commands or assurance evidence used
- Fix applied
- Validation result
- Prevention recommendation

## Validation

- Each introduced fault has a documented root cause.
- Fixes are validated with command output.
- The final routing and service state is stable.
- Assurance evidence is connected to CLI findings.

## Review Questions

1. Why should troubleshooting start with symptom scope?
2. Which command outputs are most useful for routing failures?
3. How can assurance tools reduce mean time to repair?
4. What evidence would you include in an escalation?

## Cleanup

Restore the final clean baseline and keep the incident report for exam revision.
