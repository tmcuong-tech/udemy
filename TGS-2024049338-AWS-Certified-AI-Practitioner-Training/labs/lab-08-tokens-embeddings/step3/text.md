# Step 3 — Generate an embedding

An **embedding** is a text turned into a list of numbers — a **vector**. An embedding model does not generate text; it converts text into coordinates in a high-dimensional space, arranged so that **texts with similar meaning land close together**.

That single property is what makes semantic search, recommendation and RAG possible.

## Find an embedding model in your Region

Do not assume a model ID. Ask the API which embedding models exist where you are:

```bash
aws bedrock list-foundation-models \
  --region us-east-1 \
  --by-output-modality EMBEDDING \
  --query 'modelSummaries[].[modelId,providerName]' \
  --output table
```

Pick one you have access to — an Amazon Titan Text Embeddings model is the usual choice — and store its exact ID in a shell variable so the rest of the lab does not depend on a version string printed in a handout:

```bash
MODEL_ID="<paste-the-exact-model-id-from-the-table-above>"
REGION="us-east-1"
```

> If the table is empty or your model shows no access, return to the **Model access** page in the Bedrock console and request an embeddings model. Check that page for the models available in your Region.

## Invoke it

```bash
aws bedrock-runtime invoke-model \
  --region "$REGION" \
  --model-id "$MODEL_ID" \
  --content-type application/json \
  --accept application/json \
  --cli-binary-format raw-in-base64-out \
  --body '{"inputText":"The cat sat on the mat."}' \
  embed-cat.json

cat embed-cat.json
```

Note the two flags people forget:

- `--cli-binary-format raw-in-base64-out` lets you pass the request body as plain JSON text rather than base64
- the trailing `embed-cat.json` is the **output file** — `invoke-model` writes the response to a file, it does not print it

## Read the response

```bash
# How many numbers are in the vector? (its dimensionality)
python3 -c "import json;d=json.load(open('embed-cat.json'));print('dimensions:',len(d['embedding']))"

# The first few coordinates
python3 -c "import json;d=json.load(open('embed-cat.json'));print(d['embedding'][:8])"
```

Observe:

- The output is a **fixed-length list of floating point numbers**. That length — the **dimensionality** — is a property of the model, not of your input.
- A six-word sentence and a whole paragraph produce vectors of the **same length**. Embedding compresses any input into the same fixed shape.
- The individual numbers mean nothing on their own. **No single coordinate is "the sentiment" or "the topic."** Meaning lives in the *direction* of the whole vector, and only becomes useful when you compare one vector with another.
- The response also reports how many input tokens were consumed — embedding calls are billed on tokens too, though typically far more cheaply than text generation.

## Console alternative

If you do not have CLI access, the Bedrock playground may offer an embeddings or text playground where an embeddings model can be selected. Submit the same sentence and observe the array of numbers returned. The concepts are identical; only the interface differs.

**Checkpoint:** You have a JSON file containing an embedding vector and you can state its dimensionality.
