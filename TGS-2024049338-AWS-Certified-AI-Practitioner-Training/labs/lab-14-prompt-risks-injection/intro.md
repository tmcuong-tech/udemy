# Lab 14 — Prompt Misuse, Injection and Defences

Probe a triage application you built and own with benign, educational inputs, then build a five-layer defence covering prompt hardening, input validation, output filtering, Amazon Bedrock Guardrails and least privilege.

> **Scope.** You are the defender throughout. The application under test is one you built in Lab 13 and own outright, running in your own AWS account. Every probe is benign and is immediately followed by the control that mitigates it. Only ever probe systems you own or have explicit written authorisation to test.

**What you will do:**
- Load your own triage application and write down its threat model
- Distinguish prompt injection, jailbreaking, prompt leaking, poisoning and hijacking
- Measure an undefended baseline with four benign probes against your own application
- Harden the prompt and add deterministic input validation, then re-measure
- Add output filtering, schema enforcement, Amazon Bedrock Guardrails and least privilege
