# Lab 24 — Data Protection with Amazon Macie

Use Amazon Macie to discover synthetic personal data in an S3 bucket, read the findings and connect them to the controls that keep PII out of training data and prompts.

**What you will do:**
- Explain why personal data in training sets, prompts and knowledge bases creates unmanageable risk
- Create an S3 bucket and upload clearly labelled synthetic sample data — no real personal data at any point
- Enable Amazon Macie and review its no-cost S3 bucket inventory before scanning anything
- Build a custom data identifier and run a scoped sensitive data discovery job
- Read the findings and map each one to a preventive, detective or runtime control

**Cost warning:** Amazon Macie sensitive data discovery jobs are charged by the volume of data inspected, and a completed job cannot be un-run. This lab scans three files of a few kilobytes. Always check a bucket's size before pointing a job at it.
