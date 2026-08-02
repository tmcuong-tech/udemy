# Step 5 — Ask questions grounded in your documents

1. From your application in the console, open the **web experience** — the console provides a deployed URL for it. You may be asked to sign in with the identity you configured in Step 3.
2. Ask each question below and record the answer **and its citation**.

## Questions with answers in the documents

| # | Question | Answer given | Cited source? | Correct? |
|---|---|---|---|---|
| 1 | How many days of annual leave do I get? | | | |
| 2 | What happens to unused leave at the end of the year? | | | |
| 3 | What is the meal allowance when I travel overseas? | | | |
| 4 | How long do I have to submit an expense claim? | | | |
| 5 | When can I fly business class? | | | |
| 6 | My account is locked. What do I do? | | | |
| 7 | Can I install software on my laptop myself? | | | |

Check each answer against the source text from Step 2. **Every one of these facts is invented and appears nowhere in any model's training data.** A correct answer therefore proves retrieval worked.

## Now test the harder behaviours

**8. A question requiring synthesis across one document:**

```
I have been here six years and want to take three weeks off. How many
days do I have, and what approval do I need?
```

This needs the model to combine the five-year service rule (26 days), the 10-consecutive-day threshold, and the 14-day notice rule. Did it get all three?

**9. A question spanning two documents:**

```
I am travelling overseas for work next month. What do I need to know
about booking and about claiming afterwards?
```

Does it draw on the expense policy for both the booking rules and the claim rules? Does it cite more than one source?

**10. A question phrased in words the documents never use:**

```
I can't get into my account.
```

The IT document says "accounts lock after five failed attempts". Your question says none of those words. If this works, you have watched the semantic retrieval from Lab 08 operating inside a managed service.

## What to look for in every answer

- **Is there a citation?** Q Business is designed to show where an answer came from. Click through and verify the cited passage actually says what the answer claims. This is Lab 09's "cite sources" mitigation, and it is what makes checking cheap enough to actually do.
- **Is the answer complete?** A partial answer that omits a condition — the approval requirement, the deadline — is a real risk in a policy assistant.
- **Is the tone appropriate for an employee-facing tool?**

**Checkpoint:** All ten questions asked, answers and citations recorded, and you have clicked through at least one citation to verify it.
