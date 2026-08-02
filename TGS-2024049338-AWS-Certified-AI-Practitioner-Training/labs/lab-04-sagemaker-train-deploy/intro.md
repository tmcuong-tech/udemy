# Lab 04 — Train and Deploy a Model with SageMaker

Train a binary classifier with the SageMaker built-in XGBoost algorithm, deploy it to a real-time endpoint, evaluate it, and delete every billing resource.

**⚠️ This lab creates resources that bill continuously — a notebook instance and an inference endpoint. Complete the Clean up step.**

**What you will do:**
- Review the cost model for SageMaker notebooks, training jobs and endpoints, and set a billing guard
- Create a SageMaker notebook instance and understand its execution role
- Split a tabular dataset into train, validation and test sets and upload them to Amazon S3
- Run a training job with the built-in XGBoost algorithm and inspect it in the console
- Deploy the trained model to a real-time endpoint
- Score the held-back test set and interpret accuracy, precision, recall, F1 and AUC
