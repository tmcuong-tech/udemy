# Lab 04 - Communication and Network Security

## Objectives

- Design network segmentation.
- Place firewalls, proxies, IDS/IPS, and monitoring points.
- Select secure communication channels.
- Identify OSI/TCP-IP security concerns.
- Review wireless, remote access, and third-party connectivity.

## Scenario

The portal needs internet access, administrator access, partner API connectivity, and internal database communication. You must design network controls.

## Steps

### 1. Draw Network Zones

Create zones:

```text
Internet
DMZ
Application network
Database network
Management network
Logging and monitoring network
Third-party connection
```

### 2. Define Traffic Rules

Create a matrix:

| Source | Destination | Protocol | Allowed | Justification |
| --- | --- | --- | --- | --- |
| Internet | Web tier | HTTPS | Yes | Customer portal access |
| Web tier | Database | Direct DB | No | Enforce application tier mediation |

### 3. Place Security Devices

Mark where you would use:

- Web application firewall.
- Network firewall.
- Reverse proxy.
- IDS/IPS.
- VPN or ZTNA.
- Network access control.
- Central logging.

### 4. Secure Remote Access

Design administrator access:

1. MFA required.
2. Privileged access workstation or hardened endpoint.
3. No direct internet SSH/RDP.
4. Session logging.
5. Time-bound privileged access.

### 5. Review Third-Party Connectivity

Document:

- Business owner.
- Data exchanged.
- Authentication method.
- Encryption requirement.
- Monitoring requirement.
- Contractual security requirement.

## Validation

You should have a network diagram, traffic matrix, remote access design, and third-party connectivity notes.

## Checkpoint Questions

1. Why is segmentation a defense-in-depth control?
2. What is the difference between VPN and ZTNA?
3. Where should monitoring be placed?
4. Why should firewall rules have business justification?

## Exam Focus

Network security questions often test segmentation, secure protocols, remote access, monitoring, and control placement.
