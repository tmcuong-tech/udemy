# Lab 03 - Security Architecture, Engineering, Cryptography

## Objectives

- Apply secure design principles.
- Select architecture controls.
- Compare security models.
- Choose cryptographic protections.
- Identify physical and system lifecycle risks.

## Scenario

The portal must support web users, administrators, APIs, databases, and audit logging. You must review the architecture before build approval.

## Steps

### 1. Draw the Architecture

Use diagrams.net to show:

```text
User browser
Web tier
Application tier
Database
Admin access path
Logging/SIEM destination
Backup storage
Third-party integration
```

### 2. Apply Secure Design Principles

Annotate the diagram with:

- Least privilege.
- Defense in depth.
- Fail securely.
- Secure defaults.
- Separation of duties.
- Economy of mechanism.
- Complete mediation.

### 3. Select Cryptographic Controls

Create a table:

| Requirement | Cryptographic Control |
| --- | --- |
| Protect web sessions | TLS |
| Protect stored database backups | Encryption at rest |
| Verify software integrity | Digital signatures |
| Manage certificates | PKI |
| Protect signing keys | HSM or managed key service |

### 4. Review Key Management

Answer:

1. Who owns keys?
2. Where are keys stored?
3. How are keys rotated?
4. How are compromised keys revoked?
5. Who can approve key recovery?

### 5. Review Physical and Lifecycle Risks

Document risks related to:

- Data center or cloud region availability.
- Hardware trust.
- Device retirement.
- Backup media handling.
- Administrative workstation security.

## Validation

You should have an architecture diagram, secure design annotations, crypto control table, and key management notes.

## Checkpoint Questions

1. Why is encryption not a complete security program?
2. What is the difference between symmetric and asymmetric cryptography?
3. Why is key management often harder than encryption selection?
4. What does fail securely mean?

## Exam Focus

Architecture questions often ask for the most appropriate design principle or control, not the newest tool.
