# Lab 1 - Build a Zero Trust Security Strategy

## Objective

Design a security strategy for Contoso Global Services that aligns with Zero Trust and Microsoft security best practices.

## Scenario

Contoso has separate teams for identity, cloud platform, endpoint operations, data governance, and security operations. Each team owns tools, but the board wants one coherent cybersecurity strategy that reduces breach likelihood and business impact.

## Prerequisites

- Read the SC-100 audience profile and skills at a glance.
- Open the Microsoft Zero Trust Guidance Center.
- Open the Microsoft Cybersecurity Reference Architectures.

## Tasks

### Step 1 - Identify business-critical assets

Create a table with these columns:

| Asset | Business process | Current risk | Security objective |
|-------|------------------|--------------|--------------------|

Add at least six assets, including:

- Microsoft 365 tenant
- Azure subscriptions
- Customer data store
- Finance application
- Privileged administrator accounts
- Remote workforce endpoints

### Step 2 - Apply Zero Trust principles

For each asset, map controls to the three Zero Trust principles:

- Verify explicitly
- Use least privilege
- Assume breach

Example:

| Asset | Verify explicitly | Least privilege | Assume breach |
|-------|-------------------|-----------------|---------------|
| Privileged admin accounts | MFA, risk-based Conditional Access | PIM, protected actions | PAW, alerting, session monitoring |

### Step 3 - Define strategy pillars

Create five security strategy pillars:

1. Identity as the control plane
2. Device and endpoint trust
3. Data discovery and protection
4. Threat detection and response
5. Governance and measurable posture

For each pillar, write:

- Target outcome
- Microsoft capabilities
- First 90-day action
- Success metric

### Step 4 - Prioritize initiatives

Use this scoring method:

- Business impact: 1 to 5
- Risk reduction: 1 to 5
- Implementation effort: 1 to 5
- Priority score = business impact + risk reduction - effort

Prioritize at least eight initiatives.

### Step 5 - Write an architecture decision record

Create an ADR with:

- Context
- Decision
- Options considered
- Selected Microsoft capabilities
- Risks accepted
- Review date

## Deliverable

Submit:

- Business-critical asset table
- Zero Trust mapping table
- Prioritized initiative list
- One-page architecture decision record

## Checkpoint questions

1. Why should identity be treated as a primary security control plane?
2. Which recommendation most directly supports "assume breach"?
3. What tradeoff did you accept when prioritizing the first 90 days?

