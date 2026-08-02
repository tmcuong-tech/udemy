# Step 1 — Map the shared responsibility model onto an AI workload

Before you write a single policy, you need to know which security controls are yours to configure and which AWS already handles. The exam tests this directly.

Under the AWS shared responsibility model, AWS is responsible for **security *of* the cloud** and you are responsible for **security *in* the cloud**. The line moves depending on how managed the service is.

Open a text editor and copy this table. Fill in the last column yourself before reading on.

| Control | Amazon Bedrock | Amazon SageMaker | Who owns it? |
|---|---|---|---|
| Patching the host operating system | AWS | AWS | |
| Physical data centre security | AWS | AWS | |
| Choosing which IAM principals may call the model | You | You | |
| Encrypting training data in S3 | You | You | |
| Patching the training container image | AWS (managed FM) | You (custom container) | |
| Deciding what data goes into a prompt | You | You | |
| Availability of the underlying service | AWS | AWS | |

The pattern to remember:

- **AWS always owns** the physical infrastructure, the hypervisor, the managed service software, and the security of the foundation model hosting environment.
- **You always own** identity and access management, data classification, encryption configuration, network exposure, and what you choose to send to a model.
- **The boundary shifts** with the service model. With Amazon Bedrock (fully managed, serverless) AWS handles far more of the stack. With a SageMaker training job using your own container, you own the container contents, its dependencies and its vulnerabilities.

Three points that come up repeatedly in exam questions:

1. **AWS does not use your Bedrock prompts or completions to train the base foundation models.** Your inputs and outputs are not shared with model providers. This is a service property, not something you configure.
2. **Encryption is available but not automatic at the level you may need.** S3 encrypts objects by default with an AWS managed key. Using a *customer managed* KMS key — so that you control the key policy, rotation and deletion — is your decision and your configuration work.
3. **Network isolation is your job.** By default an API call to Bedrock or SageMaker travels over the public internet to a public AWS endpoint (still TLS-encrypted). Keeping that traffic on the AWS network requires you to create VPC endpoints.

Write one sentence in your notes answering: *if a developer pastes a customer's medical record into a Bedrock prompt, whose responsibility was the failure?* You will confirm the answer in the discussion questions.
