# Step 4 — Raise temperature, then narrow top-P

## High temperature

1. Stay on the same model and the same coffee shop prompt.
2. Raise **temperature** towards its maximum for this model.
3. Run the prompt **three times**, clearing between runs, and record all three answers in the parameter observation table.
4. Compare the spread. The three high-temperature answers should differ from each other **noticeably more** than the three low-temperature answers did. You may also see an answer that is odd, strains for cleverness, or drifts off the brief entirely.

Write one sentence in your table describing the difference in *variety* between the low and high temperature runs. That sentence is the whole lesson.

## Top-P

1. Return temperature to a **middle** value so it is not dominating the result.
2. Lower **top P** substantially — to a small fraction of its range.
3. Run the prompt again and record the answer.

**What top-P does.** Top-P (also called *nucleus sampling*) restricts sampling to the **smallest set of candidate tokens whose probabilities add up to P**. Everything outside that set is discarded before sampling happens.

- A **low top-P** (say 0.1) means the model only ever draws from the very few most likely tokens. Narrow vocabulary, safe and conventional output.
- A **high top-P** (near 1.0) leaves almost the entire vocabulary in play.

## Temperature versus top-P

Both increase or decrease variety, which is why they are easy to confuse. The distinction the exam cares about:

| Parameter | Mechanism | Plain-English effect |
|---|---|---|
| **Temperature** | Reshapes the probability distribution — flattens it or sharpens it | How *adventurous* the model is allowed to be |
| **Top-P** | Truncates the candidate list to the top tokens summing to P | How *many candidates* the model is allowed to consider at all |
| **Top-K** (offered by some models) | Truncates to the K most probable tokens, a fixed count | Same idea as top-P but a fixed number rather than a probability mass |

**In practice you tune one, not all of them.** Changing temperature and top-P at the same time makes the result impossible to attribute — the same discipline as Step 2.

**Rules of thumb:**
- Factual extraction, classification, structured output → **low** temperature and top-P
- Brainstorming, marketing copy, creative naming → **higher** temperature and top-P

**Checkpoint:** Three high-temperature rows and one low-top-P row recorded, and you can state the difference between the two parameters in your own words.
