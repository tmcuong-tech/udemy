# Step 1 — Set up the comparison and run the first model

Different foundation models, given exactly the same prompt, produce noticeably different answers. Those differences are not random noise — they come from differences in training data, model size and instruction tuning. The only way to see this is to hold the prompt constant and change the model.

**Before you start,** confirm from Lab 06 that you have access granted to at least **two models from two different providers** in your Region. If not, return to the **Model access** page and request them now.

1. Open the Amazon Bedrock console at <https://console.aws.amazon.com/bedrock/> and confirm your Region.
2. In the **left navigation**, open the **playground** area and choose the **Chat** or **Text** playground.
3. Choose **Select model**, pick a provider, then pick your first model. Apply the selection.
4. Leave the inference parameters at their defaults for now. You will change them in Steps 3–5.
5. Enter this **exact prompt** — you must not change a single word of it between models:

   ```
   Explain what a foundation model is to a small business owner who has
   never used AI. Use no more than 80 words and avoid technical jargon.
   ```

6. Run it, then record four observations in the **Model comparison table** below:
   - **Length** — roughly how many words came back
   - **Tone** — formal, conversational, marketing-like, teacherly
   - **Followed the 80-word limit?** — yes or no
   - **Jargon?** — did it use technical terms despite being told not to

## Model comparison table

Fill this in as you go. You will add the second row in Step 2.

| Model | Provider | Length | Tone | Followed 80-word limit? | Jargon? |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

**Checkpoint:** One row of the comparison table is complete.
