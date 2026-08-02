# Lab 19 — Amazon Bedrock Guardrails

Create a Bedrock guardrail with content filters, denied topics, word filters and PII filters, then test it and record which policy blocks each prompt.

**What you will do:**
- Create a guardrail and write your own blocked messages for prompts and for responses
- Configure content filters across hate, insults, sexual, violence and misconduct
- Define denied topics in terms of intent rather than keywords
- Add managed profanity and custom word filters, and name their limitations
- Configure sensitive-information filters, choosing mask versus block per entity type
- Test the guardrail against benign and adversarial prompts and complete a findings table
