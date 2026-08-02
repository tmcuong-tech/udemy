# Step 4 — Semantic similarity: compare the vectors

A single embedding is useless. Embeddings only earn their keep when you **compare** them.

## Embed four sentences

Two of these mean nearly the same thing but share almost no words. Two share words but mean different things. That contrast is the whole point.

```bash
embed () {
  aws bedrock-runtime invoke-model \
    --region "$REGION" \
    --model-id "$MODEL_ID" \
    --content-type application/json \
    --accept application/json \
    --cli-binary-format raw-in-base64-out \
    --body "{\"inputText\":\"$1\"}" \
    "$2" > /dev/null
  echo "embedded -> $2"
}

embed "How do I reset my password?"            a.json
embed "I forgot my login credentials."          b.json
embed "What are your office opening hours?"     c.json
embed "How do I reset my washing machine?"      d.json
```

Sentences **a** and **b** mean the same thing and share only the word "my". Sentences **a** and **d** share four words but mean completely different things.

## Measure the distance between them

The standard measure is **cosine similarity** — the cosine of the angle between two vectors. It ranges from **1.0** (pointing the same way, semantically very close) through **0** (unrelated) to **-1.0** (opposite).

```bash
cat > cosine.py <<'PY'
import json, math, itertools

def vec(path):
    return json.load(open(path))["embedding"]

def cosine(u, v):
    dot = sum(a*b for a, b in zip(u, v))
    nu  = math.sqrt(sum(a*a for a in u))
    nv  = math.sqrt(sum(b*b for b in v))
    return dot / (nu * nv)

labels = {
    "a.json": "reset my password",
    "b.json": "forgot my login credentials",
    "c.json": "office opening hours",
    "d.json": "reset my washing machine",
}
vs = {f: vec(f) for f in labels}

for x, y in itertools.combinations(labels, 2):
    print(f"{cosine(vs[x], vs[y]):+.4f}   {labels[x]:<30} vs  {labels[y]}")
PY

python3 cosine.py
```

## Record and interpret

| Pair | Cosine similarity | Shared words? | Same meaning? |
|---|---|---|---|
| a vs b — password reset / forgot credentials | | almost none | yes |
| a vs d — reset password / reset washing machine | | many | no |
| a vs c — password reset / opening hours | | none | no |
| b vs c | | | |
| c vs d | | | |

Now answer:

1. Which pair scored **highest**? Was it the pair sharing the most words, or the pair sharing the most meaning?
2. Compare **a vs b** with **a vs d**. If you had built search by keyword matching, which pair would keyword matching have ranked higher? What would that have done to the user asking about their password?
3. All four sentences are short. Would you expect **c vs d** — two unrelated sentences — to score near zero, or somewhere above it? In practice, embeddings of same-language, same-domain text often score moderately similar even when unrelated. **What matters is the ranking of scores relative to each other, not the absolute number.**

> **This is the mechanism behind semantic search.** Embed every document once and store the vectors. At query time, embed the question and find the stored vectors closest to it. The system retrieves on **meaning**, so a user who asks "I can't get into my account" finds the password reset article that never uses those words.

**Checkpoint:** Your similarity table is filled in, and the semantically similar pair scores higher than the lexically similar pair.
