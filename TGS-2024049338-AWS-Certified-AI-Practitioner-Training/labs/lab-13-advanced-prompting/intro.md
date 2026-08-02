# Lab 13 — Advanced Prompting and Prompt Templates

Apply system prompts, role assignment, chain-of-thought and negative prompting to a rule-heavy triage task, then package the result as a reusable, tested prompt template.

**What you will do:**
- Set up a rule-heavy triage scenario where the model cannot guess the business rules
- Separate the trusted system prompt from untrusted user input, and assign a role
- Use structured chain-of-thought to make the model apply several rules in sequence
- Rewrite negative instructions as positive constraints and compare reliability
- Build a reusable prompt template with named placeholders and a delimited input region
- Test the template against empty, off-topic, oversized, multilingual and instruction-bearing input
