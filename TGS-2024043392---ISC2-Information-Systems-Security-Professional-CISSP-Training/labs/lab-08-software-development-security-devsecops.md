# Lab 08 - Software Development Security and DevSecOps

## Objectives

- Integrate security into the SDLC.
- Identify application security risks.
- Compare SAST, DAST, IAST, and SCA.
- Plan secure coding and review controls.
- Assess software supply chain risk.

## Scenario

Developers are building the portal using open-source libraries and a CI/CD pipeline. You must define security requirements before release.

## Steps

### 1. Map Security into SDLC

Create a table:

| SDLC Phase | Security Activity |
| --- | --- |
| Requirements | Security and privacy requirements |
| Design | Threat modeling |
| Development | Secure coding and peer review |
| Testing | SAST, DAST, dependency checks |
| Deployment | Change approval and release gates |
| Maintenance | Patch and vulnerability management |

### 2. Threat Model the Application

Identify:

- Trust boundaries.
- Data flows.
- Entry points.
- Authentication paths.
- High-risk misuse cases.

### 3. Choose Testing Methods

Compare:

| Method | Use |
| --- | --- |
| SAST | Static source code analysis |
| DAST | Runtime web application testing |
| IAST | Runtime analysis with instrumentation |
| SCA | Open-source dependency analysis |

### 4. Review OWASP Risks

Pick five common risks and write one control for each, such as:

- Broken access control.
- Injection.
- Cryptographic failures.
- Insecure design.
- Security misconfiguration.

### 5. Plan Supply Chain Controls

Document:

1. Approved repositories.
2. Dependency scanning.
3. SBOM requirement.
4. Code signing.
5. Secrets scanning.
6. Build pipeline access control.

## Validation

You should have an SDLC security table, threat model notes, testing method selection, and supply chain control plan.

## Checkpoint Questions

1. Why is security cheaper earlier in the SDLC?
2. What does shift-left mean?
3. Why is SCA important?
4. What is a misuse case?

## Exam Focus

Software security questions test secure SDLC, application testing, supply chain risk, DevSecOps, and secure coding governance.
