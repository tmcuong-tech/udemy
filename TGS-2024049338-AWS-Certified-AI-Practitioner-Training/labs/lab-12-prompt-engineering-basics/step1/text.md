# Step 1 — Set up the playground and fix one task

Prompt engineering can only be learned by comparison. To compare fairly you must change **one thing at a time** — so this lab fixes the model, the inference settings and the task, and varies only the prompt.

### Open the playground

1. Sign in to the AWS Management Console and open the Amazon Bedrock console at <https://console.aws.amazon.com/bedrock/>.
2. In the **Region selector** at the top right, choose a Region where Amazon Bedrock is offered — for example **US East (N. Virginia) us-east-1**. Everything in this lab is Region-specific.
3. In the left navigation, choose **Model access** and confirm that at least one text model shows access granted. If not, request access first (this is covered in Lab 06). The Model access page is the source of truth for which models are available in your Region.
4. In the left navigation, choose the **playground** area and open the **Chat** (or **Text**) playground.
5. Choose **Select model** and pick one text model you have access to. **Write the model name down. Do not change it for the rest of this lab.**

### Fix the inference settings

Open the inference configuration panel (labelled *Configurations*, *Inference parameters* or shown behind a settings icon).

- Set **temperature** to a **low** value, near 0.
- Leave top-P as provided.
- Set maximum response length to a comfortable value — long enough that answers are not truncated.

> **Why low temperature?** A high temperature makes the model's output vary between runs. If output varies for random reasons, you cannot tell whether a change in quality came from your prompt or from sampling noise. Low temperature is the correct setting for prompt experiments.

### The task for this lab

Every prompt in this lab does the same job: **classify a short customer support message into a category**.

The categories are exactly: `BILLING`, `TECHNICAL`, `ACCOUNT`, `FEEDBACK`.

Here are the five test messages. Copy them somewhere you can reuse them:

```
1. My card was charged twice for the same month.
2. The mobile app crashes every time I open the reports tab.
3. I need to change the email address on my profile.
4. Honestly the new dashboard is a big improvement, well done.
5. I was billed after cancelling and now I cannot log in at all.
```

Message 5 is deliberately ambiguous — it touches billing *and* account access. Watch what each prompting style does with it.

### Record your results

Keep this table beside you. You will fill in one row per prompting style.

| Prompting style | Msg 1 | Msg 2 | Msg 3 | Msg 4 | Msg 5 | Format clean? |
|---|---|---|---|---|---|---|
| Zero-shot, minimal | | | | | | |
| Zero-shot, structured | | | | | | |
| One-shot | | | | | | |
| Few-shot | | | | | | |

**Checkpoint:** You have one model selected, temperature near 0, and the five test messages to hand.
