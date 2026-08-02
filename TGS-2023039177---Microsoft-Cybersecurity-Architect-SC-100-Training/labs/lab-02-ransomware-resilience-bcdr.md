# Lab 2 - Design Ransomware Resilience and BCDR

## Objective

Design a ransomware resilience and business continuity strategy that protects critical services and enables recovery.

## Scenario

Contoso leadership is concerned about ransomware. The current backup process is inconsistent, privileged accounts are broad, and recovery testing is not formalized.

## Prerequisites

- Review Microsoft guidance for ransomware protection.
- Review Zero Trust privileged access guidance.
- Review backup and disaster recovery concepts for hybrid and cloud workloads.

## Tasks

### Step 1 - Define ransomware impact tiers

Classify systems into three tiers:

| Tier | Recovery expectation | Example systems |
|------|----------------------|-----------------|
| Tier 0 | Restore first, highest protection | Identity, privileged access, key vaults |
| Tier 1 | Restore within defined business window | Finance, customer systems |
| Tier 2 | Restore after core business functions | Collaboration, reporting |

Add Contoso systems to each tier.

### Step 2 - Design secure backup requirements

For each tier, define:

- Backup frequency
- Retention
- Immutability requirement
- Administrative separation
- Restore testing frequency
- Monitoring requirement

### Step 3 - Design privileged access protection

Create a privileged access design that includes:

- Separate admin accounts
- Microsoft Entra Privileged Identity Management
- Just-in-time activation
- MFA and phishing-resistant authentication
- Privileged access workstations or secure admin workstations
- Break-glass accounts
- Logging and alerting

### Step 4 - Design update and vulnerability priorities

Create a vulnerability and update policy:

| Asset class | Patch priority | Exception process | Monitoring |
|-------------|----------------|-------------------|------------|

Include endpoints, servers, internet-facing services, SaaS integrations, and identity infrastructure.

### Step 5 - Create an attack recovery workflow

Draw or describe a recovery workflow:

1. Detect ransomware indicators.
2. Isolate affected identities and devices.
3. Preserve evidence.
4. Activate incident bridge.
5. Validate clean backups.
6. Restore Tier 0 services.
7. Restore business systems.
8. Monitor for reinfection.
9. Conduct lessons learned.

## Deliverable

Submit:

- Ransomware tiering table
- Secure backup requirements
- Privileged access protection design
- Recovery workflow

## Checkpoint questions

1. Why are identity systems Tier 0?
2. Why should backup administration be separated from production administration?
3. Which control reduces ransomware blast radius the most?

