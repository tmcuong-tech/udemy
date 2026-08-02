# Step 3 — Produce a hallucination yourself and record it

This is the most important step in the lab. **You are not finished until you have made the model state something false with complete confidence, and written it down.**

Reading that models hallucinate changes nobody's behaviour. Watching a fluent, well-formatted, entirely fabricated answer appear on your own screen does.

## Why hallucination happens

A text model predicts likely next tokens. It has **no separate store of facts** and **no mechanism to check whether what it is saying is true**. Fluency and accuracy are produced by the same process, so a false answer looks exactly as confident as a true one. There is no internal signal you can read off the output that says "I am guessing here."

## Techniques that reliably provoke one

Try these in order and stop when you have a clear, checkable falsehood. Prompts that ask for **specific, verifiable, obscure facts** work best.

1. **The plausible non-existent thing.** Ask for details about something that sounds real but is not — a book, a paper, a standard, a product feature. For example, ask for a summary of a specific-sounding but invented technical paper, including its authors and its main finding.

2. **Ask for citations.** Ask the model to recommend published sources on a narrow topic and to give author, title and year for each. Then check whether they exist. Fabricated references are one of the most consistently reproducible failure modes.

3. **Very obscure specifics.** Ask for a precise number, date or name in a niche area — the population of a small town in a specific year, the exact clause number of a regulation, a minor historical figure's dates.

4. **The false premise.** Ask a question that assumes something untrue and see whether the model challenges the premise or plays along. Models often play along.

5. **A question about the near past.** Ask about something recent (see Step 4 on knowledge cutoff) and watch it answer confidently anyway rather than saying it does not know.

## Record it — this is a required deliverable

| Field | Your record |
|---|---|
| Model used | |
| Exact prompt | |
| The false claim, quoted verbatim | |
| How you verified it was false | |
| Did the model hedge at all, or state it flatly? | |
| Would a non-expert reader have spotted it? | |

**The last row is the one that matters.** A hallucination that an expert catches is a nuisance. One that a customer, a patient, a junior employee or a court filing does not catch is a business, legal or safety incident.

## Then try to fix it

Re-run your prompt with this added:

```
If you do not know the answer or are not confident it is factually
correct, say "I don't know" rather than guessing. Do not invent
sources, names, dates or figures.
```

Record whether the model now declines. Then note carefully what this **does not** give you:

> **Prompting for honesty reduces hallucination. It does not eliminate it, and it gives you no guarantee.** The model has no reliable way to know that it does not know. You cannot make a factual guarantee out of a prompt instruction — which is exactly why Step 5's mitigations are architectural rather than verbal.

**Checkpoint:** You have a verbatim false claim written down, along with how you verified it and whether a non-expert would have caught it.
