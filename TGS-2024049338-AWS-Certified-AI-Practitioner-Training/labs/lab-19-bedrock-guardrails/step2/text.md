# Step 2 — Configure content filters

Content filters are the **semantic** harm controls. They classify the meaning of the text
rather than matching literal strings, so they generalise to phrasings you never anticipated.
This is the **safety** dimension of responsible AI.

### 2.1 Enable the harmful-content categories

Enable content filters and configure each of the five harmful-content categories. Each
category can be tuned independently for **prompts** and for **responses**.

| Category | What it targets | Set filter strength to |
|---|---|---|
| Hate | Content attacking a group based on a protected characteristic | High |
| Insults | Demeaning, humiliating or belittling language aimed at a person | High |
| Sexual | Sexually explicit material | High |
| Violence | Content glorifying or instructing physical harm | High |
| Misconduct | Guidance on criminal or wrongful activity | High |

Set the strength for **both** the prompt column and the response column for all five.
Higher strength blocks more aggressively; lower strength lets more through.

### 2.2 Enable the prompt-attack filter if it is offered

If your console version offers a **prompt attack** filter (prompt injection and jailbreak
detection), enable it. Note two things about it:

- It applies to **input only** — a jailbreak is something a user does to you, not something
  the model emits.
- It is the **robustness** control in this guardrail. The five harm categories above stop
  bad content; the prompt-attack filter stops attempts to disable your controls in the
  first place.

If you do not see this filter in your Region's console version, skip it and note that in
your findings table.

### 2.3 Understand what "strength" is actually doing

The filter emits a confidence that the text belongs to a harm category. The strength
setting is effectively where you place the threshold on that confidence.

- **High strength** — lower threshold, more content blocked, more **false positives**
  (legitimate requests refused).
- **Low strength** — higher threshold, less content blocked, more **false negatives**
  (harmful content allowed through).

There is no setting that eliminates both. You are choosing which error you would rather
make, and that choice should follow from your use case — a children's education assistant
and an internal security-research tool sit at opposite ends.

> **Exam note:** You will be asked *which control mitigates which harm*, not to memorise
> strength values. Know that content filters are semantic and bidirectional, and that
> tightening them trades false negatives for false positives.

Choose **Next**.
