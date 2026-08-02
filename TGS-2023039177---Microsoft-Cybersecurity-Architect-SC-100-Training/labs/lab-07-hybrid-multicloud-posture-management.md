# Lab 7 - Design Hybrid and Multicloud Posture Management

## Objective

Design a posture management architecture for Azure, hybrid servers, and multicloud workloads.

## Scenario

Contoso runs workloads in Azure, has on-premises servers, and uses a small AWS environment. Security posture is reviewed only during audits, and cloud teams use different standards.

## Prerequisites

- Review Microsoft Defender for Cloud.
- Review Azure Arc.
- Review Microsoft Cloud Security Benchmark.
- Review security exposure management concepts.

## Tasks

### Step 1 - Inventory environments

Create an environment table:

| Environment | Workloads | Owner | Current visibility | Security risk |
|-------------|-----------|-------|--------------------|---------------|

Include:

- Azure production
- Azure development
- On-premises servers
- AWS workloads
- Internet-facing assets

### Step 2 - Design Defender for Cloud coverage

For each environment, define:

- Onboarding method
- Defender plan
- Benchmark or standard
- Alert routing
- Remediation owner
- Reporting cadence

### Step 3 - Design Azure Arc integration

Specify which non-Azure resources should be connected through Azure Arc:

- Windows servers
- Linux servers
- Kubernetes clusters
- SQL servers

For each resource type, list the posture or governance benefit.

### Step 4 - Design exposure management priorities

Create a prioritized exposure list:

| Exposure | Attack path concern | Business impact | Remediation priority |
|----------|---------------------|-----------------|----------------------|

Include examples:

- Public management ports
- Overprivileged cloud roles
- Missing endpoint protection
- Unencrypted storage
- Unpatched internet-facing server
- Weak identity controls

### Step 5 - Define secure score governance

Write a governance process:

- Baseline secure score
- Target secure score
- Control ownership
- Weekly review
- Monthly executive reporting
- Exception management

## Deliverable

Submit:

- Environment inventory
- Defender for Cloud coverage design
- Azure Arc integration plan
- Exposure priority list
- Secure score governance process

## Checkpoint questions

1. Why is posture management more than alert monitoring?
2. Which workloads benefit most from Azure Arc?
3. How should architects prevent secure score from becoming a vanity metric?

