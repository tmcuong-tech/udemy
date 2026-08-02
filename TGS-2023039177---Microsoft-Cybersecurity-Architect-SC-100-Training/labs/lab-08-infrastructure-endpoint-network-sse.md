# Lab 8 - Design Infrastructure, Endpoint, Network, and SSE Security

## Objective

Specify security requirements for endpoints, servers, SaaS, PaaS, IaaS, networks, and Security Service Edge.

## Scenario

Contoso's workforce is hybrid. Users access Microsoft 365, SaaS apps, Azure workloads, and on-premises resources from managed and unmanaged locations. Network controls are inconsistent.

## Prerequisites

- Review Microsoft Intune security baselines.
- Review Defender for Endpoint and Defender for Cloud Apps concepts.
- Review Microsoft Entra Internet Access and Private Access concepts.

## Tasks

### Step 1 - Define endpoint security baselines

Create baseline requirements for:

- Windows client
- macOS client
- Linux server
- Windows server
- Mobile devices

For each, specify:

- Endpoint protection
- Encryption
- Local admin control
- Configuration baseline
- Update policy
- Monitoring

### Step 2 - Design server and workload hardening

Create a hardening checklist for:

- Azure virtual machines
- On-premises servers
- Containers
- Kubernetes clusters
- Web workloads
- IoT or OT systems

### Step 3 - Design SaaS, PaaS, and IaaS security requirements

Create a requirements table:

| Service type | Security baseline | Monitoring | Policy enforcement |
|--------------|-------------------|------------|--------------------|

Include examples for Microsoft 365, Azure App Service, Azure SQL, Azure Storage, and virtual machines.

### Step 4 - Evaluate network security architecture

Draw or describe the target network model:

- Segmentation
- Private endpoints
- Firewall and web filtering
- Remote access
- Secure admin access
- Logging and inspection

### Step 5 - Design Security Service Edge controls

Define where these fit:

- Microsoft Entra Internet Access
- Microsoft Entra Private Access
- Conditional Access
- Defender for Cloud Apps
- Cross-tenant access settings

## Deliverable

Submit:

- Endpoint baseline table
- Server and workload hardening checklist
- SaaS/PaaS/IaaS requirements table
- Network security target model
- SSE control placement

## Checkpoint questions

1. Why should endpoint baselines differ by platform?
2. Where do network controls and identity controls overlap?
3. What risk does Security Service Edge reduce for hybrid work?

