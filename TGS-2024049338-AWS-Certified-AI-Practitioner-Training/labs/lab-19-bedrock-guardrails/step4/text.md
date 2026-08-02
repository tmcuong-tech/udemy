# Step 4 — Configure word filters

Word filters are the **literal-match** layer. They are the bluntest control in the guardrail
and, used correctly, the most predictable one.

### 4.1 Enable the managed profanity filter

Enable the **profanity filter**. This uses a word list maintained by AWS, so you inherit
maintenance you would otherwise have to do yourself.

### 4.2 Add custom blocked words

Add a small list of terms specific to your organisation. For a classroom demo use
non-offensive placeholders so the lab stays appropriate to run in a shared room:

- `CompetitorCorp`
- `ProjectFalcon`

Realistic production uses of custom word lists include unreleased product code names,
internal system names that should not appear in customer-facing output, and the names of
parties in active litigation.

Choose **Next**.

### 4.3 Know the limitation you just accepted

Word filters are exact-match style controls, and they are brittle against obfuscation:

| Evasion | Example |
|---|---|
| Spacing or punctuation | `C o m p e t i t o r C o r p` |
| Misspelling | `CompetitorKorp` |
| Homoglyphs | Cyrillic `С` substituted for Latin `C` |
| Indirection | "the company we discussed in the Q3 memo" |

This is exactly **why** word filters sit alongside — never instead of — the semantic
content filters and denied topics. Defence in depth is not a slogan here; each layer covers
a failure mode the others cannot.

> **Exam note:** If a question describes an evasion by rephrasing or obfuscation, the
> intended answer is almost never "add more words to the list". It is a semantic control —
> a content filter or a denied topic.

### 4.4 The other failure mode: over-blocking

Blunt lists also produce collateral damage. A blocked word appearing as a substring of a
legitimate word, or a product name that is also an ordinary English word, will refuse
traffic you wanted to serve. Keep custom lists short, specific, and reviewed on a schedule
with an owner — an unowned word list only ever grows.
