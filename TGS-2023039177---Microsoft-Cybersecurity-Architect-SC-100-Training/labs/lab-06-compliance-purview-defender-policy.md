# Lab 6 - Design Compliance, Purview, Defender for Cloud, and Azure Policy

## Objective

Translate compliance requirements into security controls using Microsoft Purview, Azure Policy, and Microsoft Defender for Cloud.

## Scenario

Contoso must demonstrate audit readiness for data protection, privileged activity, cloud configuration, and retention requirements. Compliance teams need control evidence without relying on manual spreadsheets.

## Prerequisites

- Review Microsoft Purview compliance capabilities.
- Review Azure Policy.
- Review regulatory compliance in Microsoft Defender for Cloud.

## Tasks

### Step 1 - Identify compliance obligations

Create five compliance obligations:

| Obligation | Business reason | Data or system affected | Evidence required |
|------------|-----------------|-------------------------|-------------------|

Include:

- Data retention
- Audit logging
- Sensitive data classification
- Privileged access review
- Cloud configuration baseline

### Step 2 - Map obligations to Microsoft controls

Create a control matrix:

| Obligation | Microsoft Purview | Azure Policy | Defender for Cloud | Other service |
|------------|-------------------|--------------|--------------------|---------------|

Examples:

- Purview information protection labels
- Purview audit
- Data lifecycle management
- Azure Policy initiatives
- Defender for Cloud regulatory compliance dashboard
- Microsoft Sentinel evidence queries

### Step 3 - Design policy assignment strategy

Define how Azure Policy should be assigned:

- Management group
- Subscription
- Resource group
- Exemption process
- Remediation task
- Ownership model

### Step 4 - Define compliance evidence workflow

Design a workflow:

1. Control owner reviews dashboard.
2. Non-compliant resource is assigned to owner.
3. Remediation is tracked.
4. Exception is approved when justified.
5. Evidence is exported or retained.
6. Compliance status is reported monthly.

### Step 5 - Define reporting audiences

Create reports for:

- Executive leadership
- Compliance and risk team
- Cloud platform team
- Security operations team
- Application owners

For each report, define the metric and decision it supports.

## Deliverable

Submit:

- Compliance obligation table
- Microsoft control matrix
- Azure Policy assignment strategy
- Evidence workflow
- Reporting audience table

## Checkpoint questions

1. Why should compliance controls be measurable?
2. What is the difference between policy enforcement and compliance reporting?
3. When is an exemption acceptable?

