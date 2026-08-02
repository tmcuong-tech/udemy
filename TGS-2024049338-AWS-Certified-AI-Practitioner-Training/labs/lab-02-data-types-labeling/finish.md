# Well done!

You have completed Lab 02 — Data Types and Labelling for ML:

✅ Classify structured, semi-structured and unstructured data
✅ Create an S3 bucket and organise a dataset
✅ Understand labelled versus unlabelled data
✅ Create a SageMaker Ground Truth labelling job
✅ Label the images and read the output manifest
✅ Clean up

**Key takeaways:**

- Structured data has a fixed schema and suits classical ML; unstructured data (images, audio, free text) usually needs deep learning or a managed AI service. Semi-structured data such as JSON sits between the two.
- Time-series is distinguished from ordinary tabular data by the fact that row order carries signal.
- Only labelled data can train a supervised model, and labelling is normally the most expensive, slowest and most bias-prone stage of the pipeline.
- SageMaker Ground Truth offers private, vendor and public (Mechanical Turk) workforces — choose by data sensitivity and required expertise. Automated data labelling uses active learning to reduce human effort on large jobs.
- Ground Truth returns an augmented manifest that pairs each object with its label, its provenance and a confidence value, and SageMaker training jobs can consume it directly.
- Amazon S3 is the landing zone for ML data; its "folders" are really key prefixes.

**Next:** Lab 03 — AWS Managed AI Services Tour
