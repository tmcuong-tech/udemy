# Step 3 — Configure a custom model job — DO NOT SUBMIT

> ## ⚠️ STOP BEFORE THE FINAL BUTTON
>
> Walk through every screen and fill in every field. **Do not choose Create, Submit or Start.** A training job incurs charges, and the custom model it produces can only be served through provisioned throughput, which is the expensive commitment described in Step 4.
>
> The whole of Task 3.3 is in understanding these fields. Submitting the job teaches you nothing further and costs real money.

### Open the configuration

1. Open the Bedrock console at <https://console.aws.amazon.com/bedrock/> and check your Region. **Model customisation is not offered in every Region, and the models available for customisation are a subset of those available for inference.** The console tells you what is offered where you are.
2. In the left navigation, find the **custom models** area and begin creating a customisation job.

### Field by field

**Job type — fine-tuning or continued pre-training.**

This is the first and most consequential choice, and it is the Step 1 distinction made concrete. Select **fine-tuning** — you have labelled prompt–completion pairs. Continued pre-training would expect unlabelled text and a much larger corpus.

**Base model.**

Choose the model to customise. Only some models support customisation, and the set differs by Region. Note two things:

- Your custom model is **derived from a specific version** of the base model. When the provider releases a newer base version, your customisation does **not** carry over — you retrain. This is real, recurring maintenance cost.
- Different base models expect different training data schemas. Changing base model may mean reformatting your dataset.

**Custom model name and job name.**

Name them so you can identify them later. A job that fails at 3am is much easier to investigate when it is not called `job-3`.

**Encryption.**

You can supply a KMS key to encrypt the custom model artefacts. **Your training data becomes part of the model's weights**, so if that data is sensitive, this is not optional. See Lab 23.

**Input data — training and validation.**

Point at the S3 locations of the two JSONL files from Step 2. The console shows the required schema for your selected base model — read it and confirm your files match. Format errors are caught at validation, after the job has started, so check before submitting.

**Hyperparameters.**

The set offered depends on the model. You will typically be able to configure some of:

| Hyperparameter | What it controls | Failure mode at the wrong value |
|---|---|---|
| **Epochs** | How many complete passes over the training data | Too few: undertrained, no behaviour change. Too many: **overfitting** — memorises training data, performs worse on new input |
| **Batch size** | Examples processed before each weight update | Affects stability and memory; interacts with learning rate |
| **Learning rate** | Size of each weight update | Too high: unstable, may destroy existing capability. Too low: slow, may never converge |
| **Learning rate warmup steps** | Gradual ramp of learning rate at the start | Improves early stability |

**Leave these at their defaults for a first run.** Defaults are chosen by the model provider to be reasonable, and changing several at once means you cannot attribute any result to any change.

**Overfitting is the concept to hold on to.** The model learns the training examples so specifically that it generalises worse. The symptom is training loss continuing to fall while validation loss flattens or rises — which is precisely why the validation set exists and why it must not overlap the training set.

**Output data.**

An S3 location for training metrics and artefacts. **Do check this after any real job** — the training and validation loss curves are the primary evidence of whether training worked or overfitted.

**Service role.**

The job needs to read your S3 input, write output, and access the base model. Let the console create a role unless your organisation requires otherwise.

### Now stop

**Review the summary page. Read every value. Then leave the page without submitting.**

Confirm nothing was created:

```bash
aws bedrock list-model-customization-jobs --region us-east-1
aws bedrock list-custom-models --region us-east-1
```

Both should return empty. If either does not, you submitted a job — go to Step 6 immediately and stop it.

### What would happen if you did submit

For completeness, since the exam may describe it:

1. The job validates the dataset format. Malformed JSONL fails here.
2. Training runs for hours, longer with more data or more epochs.
3. Loss metrics are written to your S3 output location.
4. On success, a **custom model** appears in your account.
5. **That custom model cannot be invoked on demand.** To use it at all you must first purchase provisioned throughput. Which is Step 4.

**Checkpoint:** You walked every configuration screen, can explain epochs, learning rate and overfitting, and both list commands return empty because you submitted nothing.
