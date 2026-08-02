# Lab 09 - Cross-Domain Risk Case Study

## Objectives

- Connect multiple CISSP domains in one scenario.
- Prioritize risks across business, technical, and operational concerns.
- Choose layered controls.
- Write a management-ready security recommendation.

## Scenario

The organization wants to outsource portal support to a third-party provider. The provider needs limited access to customer records, ticket history, and operational logs. Management wants approval within one week.

## Steps

### 1. Identify Cross-Domain Issues

Map concerns:

| Domain | Concern |
| --- | --- |
| Security and Risk Management | Third-party risk and contract terms |
| Asset Security | Customer data classification |
| Architecture and Engineering | Secure integration and encryption |
| Network Security | Remote access and segmentation |
| IAM | Least privilege and access review |
| Assessment | Vendor audit evidence |
| Operations | Logging, monitoring, incident notification |
| Software Security | API security and supply chain risk |

### 2. Build a Decision Matrix

| Option | Benefit | Risk | Required Control |
| --- | --- | --- | --- |
| Full access | Fast support | Excessive data exposure | Reject |
| Role-limited access | Balanced support | Configuration effort | Approve with controls |
| No access | Lowest exposure | Slow support | Use only for high-risk data |

### 3. Define Required Controls

Include:

- Contractual security clauses.
- Data processing agreement.
- Least privilege access.
- MFA and federation.
- Session logging.
- Data masking.
- Vendor incident notification.
- Audit rights.
- Access review schedule.

### 4. Write the Recommendation

Use this structure:

```text
Decision:
Reason:
Key risks:
Required controls:
Residual risk:
Approval owner:
Review date:
```

### 5. Prepare Executive Summary

Write five sentences suitable for senior management. Avoid excessive technical detail.

## Validation

You should have a domain map, decision matrix, required controls list, and executive recommendation.

## Checkpoint Questions

1. Why is third-party access a cross-domain issue?
2. What should be in a vendor security agreement?
3. Who should accept residual third-party risk?
4. Why should access be reviewed periodically?

## Exam Focus

CISSP scenarios often combine domains. Choose answers that integrate governance, legal, technical, and operational controls.
