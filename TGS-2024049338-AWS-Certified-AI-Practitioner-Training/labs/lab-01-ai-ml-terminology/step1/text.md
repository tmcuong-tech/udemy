# Step 1 — Survey the AWS AI and ML console landscape

Before defining terms, see where each idea lives in the AWS console. The console layout
itself teaches the hierarchy: AWS groups its AI/ML offerings into layers, and those layers
map almost exactly onto the vocabulary the exam tests.

### 1.1 Sign in

1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/) with an IAM
   user or role that has read access. Everything in this lab is read-only or free.
2. In the Region selector (top right), choose **US East (N. Virginia) `us-east-1`**.
   AI/ML features appear in `us-east-1` first, so screenshots and menus in this course
   assume that Region.

### 1.2 Walk the three layers

Open each of the following from the console **Services** menu (or the search bar) in a new
browser tab. Do not create anything yet — just look at the landing page and read the
one-line description AWS gives the service.

| Layer | Open this | What the landing page tells you |
|---|---|---|
| Managed AI services | **Amazon Rekognition** | Pre-trained models exposed as an API. No training, no model artefacts. |
| ML platform | **Amazon SageMaker AI** | You bring data, choose an algorithm, train, and host a model yourself. |
| Generative AI | **Amazon Bedrock** | Foundation models accessed through a single API; you prompt rather than train. |

> **Note:** If a service page prompts you to enable something or create a domain, stop
> and close the tab. Step 1 is observation only.

### 1.3 Record what distinguishes the layers

In your notes, write one sentence for each layer answering: *who supplies the model, and
who supplies the data?*

- **Managed AI service** — AWS supplies the model, you supply only the input at inference time.
- **ML platform (SageMaker)** — you supply the data and choose the algorithm; AWS supplies
  the compute, the container and the hosting.
- **Generative AI (Bedrock)** — a third party (or AWS) supplies a large pre-trained
  foundation model; you supply prompts, and optionally your own data for customisation.

This "who supplies what" question is the fastest way to answer AIF-C01 scenario questions
that ask which AWS service fits a described workload.
