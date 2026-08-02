# Lab 07 - Security Operations, Incident Response, BCP/DR

## Objectives

- Build an incident response workflow.
- Define logging and monitoring requirements.
- Apply change and configuration management.
- Plan backup, recovery, BCP, and DR.
- Preserve evidence and chain of custody.

## Scenario

The portal is live. Monitoring reports suspicious administrator activity and customer service reports intermittent outages. You must coordinate operations response.

## Steps

### 1. Create an Incident Response Flow

Use:

```text
Preparation
Detection
Analysis
Containment
Eradication
Recovery
Lessons learned
```

Add owner and evidence required for each phase.

### 2. Define Evidence Handling

Document:

1. What evidence is collected first.
2. Order of volatility.
3. Who collects evidence.
4. How chain of custody is recorded.
5. Where evidence is stored.

### 3. Design Logging and Monitoring

Specify logs for:

- Authentication.
- Privileged access.
- Firewall and network events.
- Application errors.
- Database access.
- Configuration changes.

### 4. Review Change Management

Create a change record with:

```text
Change description
Risk
Approver
Backout plan
Testing evidence
Implementation window
Post-change validation
```

### 5. Plan BCP and DR

Define:

| Item | Value |
| --- | --- |
| Critical process | Customer portal |
| RTO | Target recovery time |
| RPO | Maximum tolerable data loss |
| Backup frequency | Daily or better |
| Recovery site | Cloud region or alternate site |
| Test method | Tabletop or technical restore |

## Validation

You should have incident response, evidence, logging, change, and BCP/DR notes.

## Checkpoint Questions

1. Why does evidence handling matter during incidents?
2. What is the difference between RTO and RPO?
3. Why must backups be tested?
4. What is the purpose of lessons learned?

## Exam Focus

Operations questions test process discipline: detect, preserve evidence, communicate, recover safely, and improve controls.
