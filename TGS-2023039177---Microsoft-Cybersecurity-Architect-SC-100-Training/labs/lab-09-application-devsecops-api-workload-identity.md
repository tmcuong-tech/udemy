# Lab 9 - Design Application, DevSecOps, API, and Workload Identity Security

## Objective

Design security for applications, DevSecOps processes, APIs, web workloads, and workload identities.

## Scenario

Contoso has several custom applications. Development teams deploy through CI/CD pipelines, but security reviews are late, API inventories are incomplete, and secrets are sometimes stored in pipeline variables.

## Prerequisites

- Review secure DevOps guidance in Microsoft Cloud Adoption Framework.
- Review workload identities in Microsoft Entra ID.
- Review Azure Key Vault and Web Application Firewall concepts.

## Tasks

### Step 1 - Build an application risk inventory

Create a table:

| Application | Business criticality | Data sensitivity | Internet exposure | Risk rating |
|-------------|----------------------|------------------|-------------------|-------------|

Add at least six application types:

- Customer portal
- Finance application
- Internal HR app
- Public API
- Data processing job
- AI-enabled assistant

### Step 2 - Perform lightweight threat modeling

Choose one application and identify threats using STRIDE:

- Spoofing
- Tampering
- Repudiation
- Information disclosure
- Denial of service
- Elevation of privilege

For each threat, propose one mitigation.

### Step 3 - Design DevSecOps controls

Specify controls for each pipeline stage:

| Stage | Security control | Tool or capability | Evidence |
|-------|------------------|--------------------|----------|

Include:

- Code review
- Dependency scanning
- Secret scanning
- Infrastructure as code scanning
- Container image scanning
- Deployment approval
- Runtime monitoring

### Step 4 - Design workload identity and secrets management

Write requirements for:

- Managed identities where possible
- Workload identity federation
- Service principal lifecycle
- Key Vault access
- Certificate rotation
- Secretless deployment patterns
- Logging of privileged workload identity use

### Step 5 - Design API and web workload security

Define requirements for:

- API inventory
- Authentication and authorization
- Rate limiting
- Azure API Management
- Azure Web Application Firewall
- TLS
- Logging
- Threat detection

## Deliverable

Submit:

- Application risk inventory
- STRIDE threat model
- DevSecOps control table
- Workload identity and secrets design
- API and web workload security requirements

## Checkpoint questions

1. Why should security be added to the pipeline instead of only before production?
2. What risk is reduced by managed identities?
3. How does threat modeling support architecture decisions?

