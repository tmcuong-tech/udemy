# Step 6 — Run inference and evaluate the model

The endpoint is live. Send it the held-back test data and find out how good the model
actually is.

### 6.1 Predict a single record

```python
X_test = test_df.drop(columns=["target"])
y_test = test_df["target"].values

single = X_test.iloc[0].tolist()
result = predictor.predict(single).decode("utf-8")
print("Raw response:", result)
print("Actual label:", y_test[0])
```

The endpoint returns a **probability** between 0 and 1, not a class. That is what
`objective="binary:logistic"` asked for.

### 6.2 Apply a threshold

```python
prob = float(result)
threshold = 0.5
predicted_class = 1 if prob >= threshold else 0
print(f"probability={prob:.4f}  predicted={predicted_class}  actual={y_test[0]}")
```

**The threshold is a business decision, not a model property.** Lowering it catches more
positives at the cost of more false alarms. In a medical screening context you would
lower it deliberately, because a missed positive costs far more than a false alarm.

### 6.3 Score the whole test set

```python
import numpy as np

payload = "\n".join(",".join(str(v) for v in row) for row in X_test.values)
raw = predictor.predict(payload).decode("utf-8")
probs = np.array([float(p) for p in raw.strip().split("\n")])
preds = (probs >= 0.5).astype(int)

print("predictions:", preds.shape)
```

### 6.4 Build the confusion matrix

```python
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()

print(f"True negatives : {tn}")
print(f"False positives: {fp}")
print(f"False negatives: {fn}")
print(f"True positives : {tp}")
print()
print(f"Accuracy : {accuracy_score(y_test, preds):.4f}")
print(f"Precision: {precision_score(y_test, preds):.4f}")
print(f"Recall   : {recall_score(y_test, preds):.4f}")
print(f"F1       : {f1_score(y_test, preds):.4f}")
print(f"AUC      : {roc_auc_score(y_test, probs):.4f}")
```

Learn these definitions — Domain 1 and Domain 3 both test them:

| Metric | Formula | Answers |
|---|---|---|
| **Accuracy** | (TP + TN) / all | What fraction did it get right? Misleading when classes are imbalanced. |
| **Precision** | TP / (TP + FP) | Of the ones it flagged, how many were real? Optimise when false positives are costly. |
| **Recall (sensitivity)** | TP / (TP + FN) | Of the real ones, how many did it catch? Optimise when misses are costly. |
| **F1** | Harmonic mean of precision and recall | A single balanced score. |
| **AUC-ROC** | Area under the ROC curve | Ranking quality across *all* thresholds, independent of the one you chose. |

Precision and recall trade off against each other; moving the threshold in 6.2 moves you
along that trade-off. AUC does not depend on the threshold at all, which is why it is the
better headline number when the operating point is still undecided.

### 6.5 Try moving the threshold

```python
for t in [0.2, 0.35, 0.5, 0.65, 0.8]:
    p = (probs >= t).astype(int)
    print(f"threshold={t:<5} precision={precision_score(y_test, p):.3f}  recall={recall_score(y_test, p):.3f}")
```

Watch precision rise and recall fall as the threshold increases. **The model did not
change** — only the decision rule you wrapped around it. This is one of the most useful
practical insights in the whole course.

### 6.6 Invoke from outside the SDK (optional)

The endpoint is an ordinary HTTPS service any authorised application can call:

```python
import boto3, json

runtime = boto3.client("sagemaker-runtime", region_name=region)
row = ",".join(str(v) for v in X_test.iloc[1].values)

response = runtime.invoke_endpoint(
    EndpointName="aif-lab04-endpoint",
    ContentType="text/csv",
    Body=row,
)
print(response["Body"].read().decode("utf-8"))
```

This is what a web application, a Lambda function or an API Gateway integration would do.
The model is now a piece of infrastructure, not a notebook artefact.

**Now go straight to Step 7 and delete the endpoint.**
