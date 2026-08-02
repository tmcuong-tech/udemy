# Step 5 — See the same catalogue from the AWS CLI

Everything you just clicked through is available through the API. Seeing it as data makes the Region-specific, ID-based nature of the catalogue concrete.

If you have the AWS CLI configured with credentials that allow Bedrock read actions, run:

```bash
# Which models exist in this Region?
aws bedrock list-foundation-models --region us-east-1

# Narrow it down to text models
aws bedrock list-foundation-models \
  --region us-east-1 \
  --by-output-modality TEXT

# Just the IDs, so the list is readable
aws bedrock list-foundation-models \
  --region us-east-1 \
  --query 'modelSummaries[].modelId' \
  --output table

# Everything one provider offers here
aws bedrock list-foundation-models \
  --region us-east-1 \
  --by-provider amazon
```

Then look at a single model in detail. Copy one model ID from the output above:

```bash
aws bedrock get-foundation-model \
  --region us-east-1 \
  --model-identifier <paste-a-model-id-here>
```

Read the response and find:

- `modelId` — the string your application passes when it invokes the model
- `providerName` — who built it
- `inputModalities` / `outputModalities` — what goes in and what comes out
- `responseStreamingSupported` — whether the model can stream tokens back as they are produced, rather than making the user wait for the whole answer

Now change the Region and run the first command again:

```bash
aws bedrock list-foundation-models \
  --region us-west-2 \
  --query 'modelSummaries[].modelId' \
  --output table
```

Compare the two lists. If they differ, you have just demonstrated to yourself why "is this model available?" is always a Region-specific question.

> **Note the two different API namespaces.** `aws bedrock ...` is the **control plane** — listing models, managing access, custom models. `aws bedrock-runtime ...` is the **data plane** — actually invoking a model to get an answer. You will use `bedrock-runtime` in Lab 08.

If you do not have CLI access in your training account, read this step for the concepts and move on. The console work in Steps 2–4 is sufficient to complete the lab.

**Checkpoint:** You can explain the difference between `bedrock` and `bedrock-runtime`, and you have seen that the model list is a per-Region result.
