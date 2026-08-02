# Lab 06 - Security Assessment and Testing

## Objectives

- Plan assessment, test, and audit activities.
- Distinguish vulnerability assessment, penetration testing, and audit.
- Create a remediation tracker.
- Define metrics and reporting.
- Handle exceptions and risk acceptance.

## Scenario

Before the portal goes live, management requests assurance that controls are operating effectively. You must design an assessment and reporting plan.

## Steps

### 1. Define Assessment Scope

Record:

```text
Systems included
Systems excluded
Testing window
Rules of engagement
Data handling requirements
Emergency contacts
Success criteria
```

### 2. Choose Test Types

Create a table:

| Activity | Purpose | Output |
| --- | --- | --- |
| Vulnerability assessment | Identify known weaknesses | Vulnerability list |
| Penetration test | Validate exploitability and impact | Test report |
| Audit | Confirm compliance with criteria | Audit findings |
| Code review | Identify software defects | Secure coding findings |

### 3. Build a Remediation Tracker

Use:

| Finding | Severity | Owner | Due Date | Status | Exception |
| --- | --- | --- | --- | --- | --- |
| Missing MFA for admin | High | IAM owner | 14 days | Open | No |

### 4. Define Metrics

Examples:

- Critical vulnerabilities open.
- Mean time to remediate.
- Patch compliance percentage.
- Control test pass rate.
- Repeat findings.

### 5. Handle Exceptions

For any accepted risk, record:

1. Business owner.
2. Risk description.
3. Compensating control.
4. Expiry date.
5. Approval evidence.

## Validation

You should have an assessment plan, test type table, remediation tracker, and exception process.

## Checkpoint Questions

1. Why is authorization required before penetration testing?
2. What is the difference between audit evidence and vulnerability output?
3. Who owns remediation?
4. Why should exceptions expire?

## Exam Focus

Assessment questions test scope, authorization, evidence, reporting, metrics, remediation, and risk acceptance.
