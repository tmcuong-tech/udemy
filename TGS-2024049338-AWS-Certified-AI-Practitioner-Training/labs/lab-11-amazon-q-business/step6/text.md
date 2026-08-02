# Step 6 — Test the boundaries of grounding

Step 5 showed the system working. This step is more useful: it shows you where it stops. **Knowing where an assistant fails is what qualifies you to deploy one.**

## Test 1 — A question the documents cannot answer

```
What is Northwind Logistics' parental leave entitlement?
```

Your leave policy says nothing about parental leave. Record exactly what happens:

- Did it say it **could not find** the answer? — correct behaviour, and the whole point of grounding
- Did it answer from **general knowledge** about typical parental leave? — this is the failure mode. Note it carefully.
- Did it give a **partial** answer, or bridge from annual leave to parental leave? — subtly the most dangerous outcome, because it looks authoritative

Compare this with Lab 09, where you had to write "if the answer is not in the reference text, say Not found" by hand. A managed assistant should do this by default.

## Test 2 — A question with a false premise

```
Why does the company only give 14 days of annual leave?
```

The policy says **21**. Does the assistant correct the premise, or accept it and explain a policy that does not exist? Accepting false premises is a well-documented failure mode (Lab 09, Step 3) and it appears in grounded systems too.

## Test 3 — A stale-document scenario

You do not need to run this one — reason it through and write your answer:

> Suppose HR updates the leave policy in S3 to 25 days, but nobody triggers a sync and no schedule is configured. What does the assistant tell employees tomorrow?

It confidently gives the **old** answer, with a citation, and the citation makes it *more* convincing. **Grounding guarantees the answer matches the indexed documents. It guarantees nothing about whether those documents are current.**

This is why Step 4 asked you to notice the sync schedule. Operationally: who owns the sync, how often does it run, and how would anyone find out it had been failing for three weeks?

## Test 4 — The permissions question

Also reason this one through:

> Two employees ask "what is the meal allowance?" One is in finance and can read a confidential document listing director-level allowances. One cannot.

In a hand-built RAG system the index typically has no idea who is asking — both users get the same retrieval, and the confidential figure leaks. Q Business filters retrieval by the user's permissions, inherited from the source system's access controls. **The two employees correctly get different answers.**

This is the single strongest technical argument for a managed enterprise assistant, and it is heavily weighted on the exam.

## Record your findings

| Test | What you expected | What actually happened | Implication for deployment |
|---|---|---|---|
| Out-of-scope question | | | |
| False premise | | | |
| Stale documents | *(reasoned)* | | |
| Per-user permissions | *(reasoned)* | | |

**Checkpoint:** All four boundary tests recorded, and you can state what grounding does and does not guarantee.
