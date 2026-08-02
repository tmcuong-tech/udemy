# Lab 4 - Design SIEM, XDR, SOAR, and Incident Response

## Objective

Design an integrated security operations capability using Microsoft Sentinel, Microsoft Defender XDR, SOAR, hunting, and incident response.

## Scenario

Contoso receives alerts from endpoint, identity, email, cloud, and firewall systems. Analysts manually correlate alerts, and incident response playbooks are inconsistent.

## Prerequisites

- Review Microsoft Sentinel concepts.
- Review Microsoft Defender XDR concepts.
- Review MITRE ATT&CK Enterprise matrix.

## Tasks

### Step 1 - Define telemetry sources

Create a telemetry inventory:

| Source | Security value | Retention need | Destination |
|--------|----------------|----------------|-------------|

Include:

- Microsoft Entra sign-in logs
- Defender for Endpoint alerts
- Defender for Office 365 alerts
- Defender for Cloud alerts
- Azure activity logs
- Microsoft Purview audit
- Firewall or network logs
- SaaS application logs

### Step 2 - Design SIEM and XDR responsibilities

Create a decision table:

| Capability | Microsoft Sentinel | Microsoft Defender XDR | Notes |
|------------|--------------------|------------------------|-------|

Cover:

- Cross-domain incident correlation
- Advanced hunting
- Threat intelligence
- Log retention
- SOAR automation
- Case management

### Step 3 - Map detections to MITRE ATT&CK

Choose five likely attack techniques, such as:

- Phishing
- Valid accounts
- Privilege escalation
- Data exfiltration
- Command and control

For each, define:

- Signal source
- Detection rule
- Response action
- Owner

### Step 4 - Design SOAR playbooks

Design three automation workflows:

1. High-risk user sign-in response
2. Malware on endpoint response
3. Suspicious OAuth application consent response

For each workflow, list:

- Trigger
- Automated actions
- Human approval step
- Evidence captured
- Closure condition

### Step 5 - Define operating metrics

Define metrics for:

- Mean time to detect
- Mean time to respond
- False positive rate
- Alert backlog
- Playbook automation rate
- Incidents by severity

## Deliverable

Submit:

- Telemetry inventory
- SIEM/XDR responsibility table
- MITRE ATT&CK detection map
- Three SOAR workflows
- SOC metrics list

## Checkpoint questions

1. When should data be sent to Sentinel instead of staying only in an XDR portal?
2. Why should automation include human approval for some actions?
3. Which metric best shows whether operations are improving?

