# Step 3 — Baseline at low temperature: seeing non-determinism

Now reverse the experiment. **Hold the model constant** and change the knobs. Pick **one** model from Step 2 and stay on it for the rest of the lab.

1. In the playground, open the **inference configuration** panel — look for *Configurations*, *Inference parameters*, or a settings control beside the model name.
2. Find the controls for **Temperature**, **Top P**, and the maximum response length (labelled **Maximum length**, **Max tokens**, or similar). The exact set of parameters offered **depends on the model you selected** — some models expose more controls than others.
3. Set **temperature to a low value, near 0**. Leave top-P as provided.
4. Use this prompt:

   ```
   Give me a name for a new coffee shop in Singapore and one sentence
   explaining the name.
   ```

5. Run it **three times**, clearing the conversation between runs, and record each answer in the **Parameter observation table** below.
6. Look at your three answers. At low temperature they should be **similar or identical** to each other.

## What temperature actually does

A text model does not "know" the next word. At each position it computes a **probability distribution** over possible next tokens, then **samples** one from that distribution. Temperature reshapes that distribution before sampling:

- **Low temperature** sharpens the distribution towards the most probable tokens. Output becomes closer to **deterministic**, more predictable, more repetitive.
- **High temperature** flattens the distribution, giving lower-probability tokens a real chance. Output becomes more varied and more "creative" — and more likely to go off-brief.

> **Important nuance for the exam:** even at temperature 0, foundation models are **not guaranteed to be perfectly reproducible**. Low temperature makes output *closer to* deterministic; it does not turn the model into a lookup table. If your application genuinely requires the identical answer every time, a generative model is the wrong tool — use a template, a database query, or a rule.

## Parameter observation table

| Run | Temperature | Top-P | Max tokens | Answer (summarise) | What you noticed |
|---|---|---|---|---|---|
| Low temp — run 1 | | | | | |
| Low temp — run 2 | | | | | |
| Low temp — run 3 | | | | | |
| High temp — run 1 | | | | | |
| High temp — run 2 | | | | | |
| High temp — run 3 | | | | | |
| Low top-P | | | | | |
| Small max tokens | | | | | |

**Checkpoint:** Three low-temperature rows recorded, and you can describe how similar they were.
