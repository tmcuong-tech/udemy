# Well done!

You have completed Lab 04 — Train and Deploy a Model with SageMaker:

✅ Read the cost warning and plan the run
✅ Create a SageMaker notebook instance
✅ Prepare the dataset and upload it to S3
✅ Train a model with the built-in XGBoost algorithm
✅ Deploy the model to a real-time endpoint
✅ Run inference and evaluate the model
✅ Clean up

**Key takeaways:**

- A training job bills only for the seconds it runs; a real-time endpoint and a notebook instance bill continuously until deleted. This single distinction is the most commonly tested cost fact in Domain 1.
- Deployment creates three separate objects — model, endpoint configuration and endpoint — and all three must be deleted. Deleting the endpoint is what stops the billing.
- The deployment option (real-time, batch transform, serverless, asynchronous) is a decision separate from the model itself, driven by latency, traffic pattern and payload size.
- Hyperparameters such as `num_round`, `max_depth` and `eta` are set before training; the tree structures XGBoost learns are parameters.
- Three splits do three jobs: training fits the model, validation guards against overfitting and tunes hyperparameters, and the test set stays unseen for an honest final estimate.
- Accuracy misleads on imbalanced data. Precision matters when false positives are costly, recall when misses are costly, and AUC-ROC summarises ranking quality independently of any threshold.
- The classification threshold is a business decision layered on top of the model — moving it changes precision and recall without retraining anything.
- The execution role is how a SageMaker training job or endpoint gets permission to read your data; `AmazonSageMakerFullAccess` is acceptable for a lab, not for production.

**Next:** Lab 05 — The ML Pipeline and Data Preparation
