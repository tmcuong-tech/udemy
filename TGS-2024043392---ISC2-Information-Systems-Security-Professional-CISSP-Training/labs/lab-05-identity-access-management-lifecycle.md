# Lab 05 - Identity and Access Management

## Objectives

- Design an IAM lifecycle.
- Compare DAC, MAC, RBAC, and ABAC.
- Plan authentication and MFA.
- Review federation, SSO, and privileged access.
- Build an access review process.

## Scenario

The portal will be used by customers, support agents, administrators, developers, and auditors. You must design access controls.

## Steps

### 1. Identify Roles

Create a role table:

| Role | Access Needed | Data Sensitivity | Approval Owner |
| --- | --- | --- | --- |
| Support agent | View customer cases | Confidential | Support manager |
| Auditor | Read audit logs | Restricted | Compliance manager |

### 2. Choose Access Model

Compare:

| Model | Best Use |
| --- | --- |
| DAC | Owner-controlled sharing |
| MAC | High-security classification environments |
| RBAC | Job-role-based enterprise access |
| ABAC | Context-aware access based on attributes |

Choose the best model for the portal and explain why.

### 3. Design Identity Lifecycle

Document steps:

```text
Joiner request
Manager approval
Role assignment
MFA enrollment
Access review
Role change
Deprovisioning
Privileged access removal
```

### 4. Plan Authentication

Specify:

- Password policy.
- MFA requirement.
- Federation or SSO.
- Session timeout.
- Account lockout.
- Recovery process.

### 5. Privileged Access Management

Define:

1. Which roles are privileged.
2. How privileged access is approved.
3. Whether access is just-in-time.
4. How sessions are logged.
5. How emergency access is controlled.

## Validation

You should have an IAM matrix, access model decision, lifecycle process, and privileged access plan.

## Checkpoint Questions

1. Why is least privilege central to IAM?
2. What is the difference between authentication and authorization?
3. Why are access reviews necessary?
4. What makes privileged access different from normal access?

## Exam Focus

IAM questions test lifecycle management, access control models, federation, MFA, SSO, and privileged account controls.
