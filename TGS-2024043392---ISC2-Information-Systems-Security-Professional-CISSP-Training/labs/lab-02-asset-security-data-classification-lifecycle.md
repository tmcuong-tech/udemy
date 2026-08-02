# Lab 02 - Asset Security, Data Classification, Lifecycle

## Objectives

- Classify information assets.
- Assign asset owners and custodians.
- Select data handling controls.
- Plan retention, disposal, and legal hold requirements.
- Map data states to protection controls.

## Scenario

The customer portal from Lab 01 stores public content, internal operating notes, customer personal information, and audit records. You must classify the data and define lifecycle controls.

## Steps

### 1. Create an Asset Inventory

Create a table:

| Asset | Owner | Custodian | Location | Classification | Business Use |
| --- | --- | --- | --- | --- | --- |
| Customer profile table | Business owner | IT operations | Cloud database | Confidential | Account management |

### 2. Define Classification Levels

Use a simple scheme:

```text
Public
Internal
Confidential
Restricted
```

Define each level in plain language.

### 3. Map Handling Requirements

For each classification, document:

- Access control.
- Encryption requirement.
- Sharing rule.
- Retention period.
- Disposal method.
- Logging requirement.

### 4. Map Data States

Identify controls for:

| State | Example Control |
| --- | --- |
| Data at rest | Encryption, access control, backup protection |
| Data in transit | TLS, VPN, secure protocols |
| Data in use | Least privilege, memory protection, secure endpoints |

### 5. Plan Retention and Disposal

1. Identify records with legal or regulatory retention needs.
2. Identify data that should not be retained longer than needed.
3. Choose disposal methods such as crypto-erase, secure wipe, or physical destruction.
4. Record who approves disposal.

## Validation

You should have an asset inventory, classification definitions, handling rules, and disposal plan.

## Checkpoint Questions

1. What is the difference between asset owner and custodian?
2. Why does classification drive control selection?
3. What is data remanence?
4. Why can over-retention increase risk?

## Exam Focus

CISSP asset security questions often test ownership, classification, data states, retention, legal hold, and secure disposal.
