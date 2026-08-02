# Lab 3 - Map MCRA, MCSB, CAF, and Well-Architected Controls

## Objective

Map business security requirements to Microsoft architecture frameworks and benchmark controls.

## Scenario

Contoso has multiple architecture documents but no common security control language. The CIO wants a single view showing how strategy maps to Microsoft guidance.

## Prerequisites

- Open Microsoft Cybersecurity Reference Architectures.
- Open Microsoft Cloud Security Benchmark.
- Open Azure Well-Architected Framework security pillar.
- Open Cloud Adoption Framework security guidance.

## Tasks

### Step 1 - Create requirement statements

Write 10 security requirements using this format:

```text
The organization must <security outcome> so that <business risk is reduced>.
```

Examples:

- The organization must enforce least-privilege administration so that unauthorized privilege escalation risk is reduced.
- The organization must monitor cloud posture continuously so that misconfigurations are detected before exploitation.

### Step 2 - Map requirements to frameworks

Create a mapping table:

| Requirement | MCRA capability | MCSB control family | CAF/WAF guidance | Microsoft service |
|-------------|-----------------|---------------------|------------------|-------------------|

Use at least eight Microsoft services across the table, such as:

- Microsoft Entra ID
- Microsoft Defender for Cloud
- Microsoft Sentinel
- Microsoft Defender XDR
- Microsoft Purview
- Azure Policy
- Microsoft Intune
- Azure Key Vault

### Step 3 - Identify control gaps

For each requirement, mark one status:

- Implemented
- Partially implemented
- Not implemented
- Unknown

Then write the missing evidence needed to confirm the status.

### Step 4 - Build a roadmap

Group gaps into:

- 0 to 30 days
- 31 to 60 days
- 61 to 90 days
- Later

Keep the roadmap realistic. Do not place every control in the first month.

### Step 5 - Prepare an executive summary

Write a short executive summary with:

- Top three risks
- Top three recommended investments
- Measurable outcomes
- Dependencies and assumptions

## Deliverable

Submit:

- 10 requirement statements
- Framework mapping table
- Control gap status
- 90-day roadmap
- Executive summary

## Checkpoint questions

1. Why is framework mapping useful for architects?
2. Which controls need evidence before they can be considered implemented?
3. What is the risk of mapping tools without mapping outcomes?

