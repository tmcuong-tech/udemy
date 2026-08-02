# Well done!

You have completed Lab 05 — The ML Pipeline and Data Preparation:

✅ Frame the business problem and map the pipeline
✅ Collect data and explore it
✅ Pre-process the data
✅ Engineer features and store them
✅ Train, tune and evaluate
✅ Deploy, monitor and close the loop
✅ Clean up

**Key takeaways:**

- The ML lifecycle runs from business framing through collection, EDA, pre-processing, feature engineering, training, tuning, evaluation, deployment and monitoring — and it is a loop, not a line. Data stages consume most of the effort.
- Target leakage is the most damaging silent error in ML: test every feature by asking whether you would have that value, with that value, at the moment of a live prediction.
- Fit every transformation on the training split only. Splitting by time and by group matters whenever the data is temporal or has many rows per entity.
- Feature engineering — time-window aggregations, ratios, recency counts and domain flags — usually adds more value than a better algorithm.
- SageMaker Feature Store gives training and inference one shared feature definition, preventing training/serving skew; the online store serves real-time inference, the offline store serves training, and event time makes point-in-time correct training sets possible.
- Overfitting shows as excellent training performance with worse validation performance; automatic model tuning searches hyperparameters against an objective metric, and cost scales with the maximum job count.
- Accuracy is misleading on imbalanced data — choose AUC, precision, recall or precision-at-k according to the business constraint and the relative cost of each error type.
- Choose batch transform when nobody is waiting and all inputs exist; choose a real-time endpoint only when latency demands it.
- Models decay through data drift, concept drift and data quality failures. Model Monitor compares live traffic against a training baseline and alerts through CloudWatch; SageMaker Pipelines and the Model Registry automate the retraining and approval loop.

**Next:** Lab 06 — Amazon Bedrock Getting Started
