# Learner Guide - Microsoft Cybersecurity Architect (SC-100)

## Course information

- **Course code:** TGS-2023039177
- **Course title:** Microsoft Cybersecurity Architect (SC-100) Training
- **Registration:** https://www.tertiarycourses.com.sg/wsq-microsoft-cybersecurity-architect-sc-100-training.html#review-form
- **Exam reference:** https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/sc-100

## Course goal

This learner guide helps you practise the work of a Microsoft cybersecurity architect. You will translate business risk into security capabilities, justify architecture choices, and map Microsoft security services to Zero Trust, Microsoft Cybersecurity Reference Architectures (MCRA), Microsoft Cloud Security Benchmark (MCSB), Cloud Adoption Framework (CAF), Azure Well-Architected Framework, and SC-100 exam objectives.

## Learning outcomes

By the end of the labs, you should be able to:

1. Design a Zero Trust security strategy for identity, devices, data, applications, infrastructure, AI, and operations.
2. Prioritize ransomware resilience, BCDR, secure backup, privileged access, and update strategy controls.
3. Map Microsoft security architecture guidance to real business requirements.
4. Design security operations using Microsoft Sentinel, Microsoft Defender XDR, SOAR, hunting, and incident response.
5. Design identity and access controls with Microsoft Entra ID, Conditional Access, PIM, entitlement management, access reviews, and protected actions.
6. Translate compliance requirements into Microsoft Purview, Azure Policy, and Defender for Cloud controls.
7. Design posture management for Azure, hybrid, and multicloud environments using Defender for Cloud, Secure Score, Azure Arc, and exposure management.
8. Specify endpoint, server, SaaS, PaaS, IaaS, network, and Security Service Edge security requirements.
9. Design application, DevSecOps, API, WAF, workload identity, and data security patterns.
10. Present an executive-ready security architecture with tradeoffs, priorities, and exam-aligned reasoning.

## Suggested schedule

### Day 1 - Strategy, operations, identity, and compliance

| Time | Activity |
|------|----------|
| 09:00 - 09:30 | Course briefing, SC-100 role expectations, case study setup |
| 09:30 - 10:45 | Lab 1 - Zero Trust security strategy |
| 10:45 - 11:00 | Break |
| 11:00 - 12:15 | Lab 2 - Ransomware resilience and BCDR |
| 12:15 - 13:15 | Lunch |
| 13:15 - 14:30 | Lab 3 - MCRA, MCSB, CAF, and WAF control mapping |
| 14:30 - 14:45 | Break |
| 14:45 - 16:00 | Lab 4 - SIEM, XDR, SOAR, and incident response |
| 16:00 - 17:00 | Lab 5 - Identity, Conditional Access, and privileged access |

### Day 2 - Infrastructure, applications, data, and capstone

| Time | Activity |
|------|----------|
| 09:00 - 10:15 | Lab 6 - Compliance, Purview, Defender for Cloud, and Azure Policy |
| 10:15 - 10:30 | Break |
| 10:30 - 11:45 | Lab 7 - Hybrid and multicloud posture management |
| 11:45 - 12:45 | Lunch |
| 12:45 - 14:00 | Lab 8 - Infrastructure, endpoint, network, and SSE security |
| 14:00 - 15:15 | Lab 9 - Application, DevSecOps, API, and workload identity security |
| 15:15 - 15:30 | Break |
| 15:30 - 16:45 | Lab 10 - Data, AI, Microsoft 365, and capstone architecture |
| 16:45 - 17:00 | Exam readiness review and next steps |

## Case study used throughout the labs

You are the cybersecurity architect for **Contoso Global Services**, a regional professional services company with 4,000 users, three Azure subscriptions, a Microsoft 365 E5 tenant, a small AWS footprint, branch offices, and a mix of Windows, macOS, Linux, mobile, and SaaS workloads.

Current challenges:

- Identity sprawl across Microsoft Entra ID, legacy AD DS, SaaS applications, service accounts, and workload identities.
- Inconsistent endpoint hardening across servers, clients, and mobile devices.
- Limited visibility across Azure, AWS, Microsoft 365, and on-premises systems.
- Manual incident response and weak post-incident learning.
- Compliance pressure for data protection, audit retention, privileged access, and third-party access.
- Business concern about ransomware, accidental data exposure, and insecure AI adoption.

## Lab deliverables

Each lab asks you to produce one or more architecture artifacts:

- Architecture decision record
- Control mapping table
- Risk register
- Target-state diagram
- Detection and response workflow
- Conditional Access or privileged access design
- Compliance control matrix
- Executive recommendation

Keep outputs concise. SC-100 rewards architect reasoning: why a design is appropriate, what risks it reduces, what tradeoffs remain, and how it aligns to Microsoft guidance.

## Recommended learner folder

Create a folder on your device:

```text
SC-100-Learner-Work/
  lab-01-zero-trust.md
  lab-02-ransomware-bcdr.md
  lab-03-control-mapping.md
  lab-04-security-operations.md
  lab-05-identity-access.md
  lab-06-compliance.md
  lab-07-posture-management.md
  lab-08-infrastructure-security.md
  lab-09-application-security.md
  lab-10-capstone.md
```

## How to complete each lab

1. Read the scenario and objectives.
2. Open the listed Microsoft references.
3. Complete the architecture task step by step.
4. Record design assumptions before selecting technologies.
5. Map each recommendation to risk reduction and Microsoft security capability.
6. Answer the checkpoint questions.
7. Save the deliverable before moving to the next lab.

## Exam preparation guidance

When answering SC-100 style questions, look for:

- Business objective before technical control.
- Identity-first and least-privilege design.
- Zero Trust principles: verify explicitly, use least privilege, assume breach.
- Architect-level decisions over implementation-only details.
- Integration across Microsoft Defender, Microsoft Sentinel, Microsoft Entra, Microsoft Purview, Azure Policy, Defender for Cloud, and Microsoft 365.
- Governance and measurable operating model, not just tool deployment.

## Final capstone expectation

At the end of Lab 10, you should have a complete target-state security architecture that includes:

- Security strategy and priorities
- Identity and privileged access model
- Security operations model
- Compliance and data protection controls
- Infrastructure and endpoint posture model
- Application and workload identity security model
- Data, AI, and Microsoft 365 security model
- 30/60/90-day roadmap

