# Lab 5 - Design Identity, Conditional Access, and Privileged Access

## Objective

Design a modern identity and access architecture using Microsoft Entra ID, Conditional Access, PIM, entitlement management, and access reviews.

## Scenario

Contoso uses Microsoft Entra ID, legacy AD DS, and several SaaS applications. Privileged roles are often permanent, guest access is not reviewed, and service accounts are poorly documented.

## Prerequisites

- Review Microsoft Entra Conditional Access.
- Review Microsoft Entra Privileged Identity Management.
- Review entitlement management and access reviews.

## Tasks

### Step 1 - Define identity populations

Create a table:

| Population | Examples | Authentication requirement | Access governance |
|------------|----------|----------------------------|-------------------|

Include:

- Employees
- Administrators
- External partners
- Break-glass users
- Workload identities
- Agent or automation identities

### Step 2 - Design Conditional Access policies

Design at least six Conditional Access policies:

| Policy | Target | Conditions | Controls | Exclusions | Risk reduced |
|--------|--------|------------|----------|------------|--------------|

Include policies for:

- Require MFA for all users
- Block legacy authentication
- Require compliant or managed devices for sensitive apps
- Require phishing-resistant MFA for administrators
- Enforce sign-in risk controls
- Protect high-risk locations or impossible travel

### Step 3 - Design privileged access

Create a privileged access model:

- Tier 0, Tier 1, and Tier 2 roles
- Eligible versus permanent assignment
- Approval requirements
- Activation duration
- Protected actions
- Access review cadence
- Emergency access account handling

### Step 4 - Design external identity governance

For B2B and external partners, define:

- Invitation approval process
- Sponsor ownership
- Terms of use
- Access package
- Review frequency
- Expiration rule

### Step 5 - Specify AD DS hardening requirements

Write requirements for:

- Domain admin reduction
- Separate admin accounts
- Tiered administration
- Protected Users group
- Kerberos and NTLM review
- Service account inventory
- Monitoring for privileged group changes

## Deliverable

Submit:

- Identity population table
- Conditional Access policy design
- Privileged access model
- External identity governance design
- AD DS hardening requirements

## Checkpoint questions

1. Why should administrator authentication differ from standard user authentication?
2. Why are break-glass accounts excluded from some policies?
3. How do access reviews reduce long-term privilege risk?

