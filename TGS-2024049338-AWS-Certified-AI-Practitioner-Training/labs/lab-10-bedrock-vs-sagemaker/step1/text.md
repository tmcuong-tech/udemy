# Step 1 — The three options, and the question that separates them

AWS offers AI capability at three levels of abstraction. Choosing between them is one of the most frequently examined judgements in Domain 2, and one of the most consequential real decisions an architect makes.

| Layer | What you get | What you manage | Typical example |
|---|---|---|---|
| **Managed AI services** | A trained model behind a task-specific API | Nothing — you call an API | Amazon Comprehend, Rekognition, Transcribe, Translate, Textract |
| **Amazon Bedrock** | Foundation models from several providers behind one API | Prompts and data; no infrastructure | Bedrock on-demand inference |
| **Amazon SageMaker (incl. JumpStart)** | The tools to train, tune, host and operate models yourself | The model, the instances, the endpoints, the scaling | SageMaker JumpStart, training jobs, inference endpoints |

Read down the "What you manage" column. **The layers differ by how much you are responsible for**, and responsibility trades off directly against control.

## The question that separates them

> **Does a service already exist that does exactly this task?**
>
> - **Yes** → use the **managed AI service**. It is cheaper, faster to build, needs no ML expertise, and someone else keeps the model current.
> - **No, but a general-purpose foundation model can do it with a good prompt** → use **Bedrock**.
> - **No, and I need a specific model, my own weights, custom training, or control over hosting** → use **SageMaker**.

Most teams get this wrong in one direction: they reach for a foundation model because it is the interesting technology, when a managed service would have solved the problem for less money, with lower latency and with a consistent, testable output.

**The rule to carry into the exam:** *the most specific service that solves the problem is usually the right answer.*

## Cost warning for this lab

You will **browse** these consoles. You will **not deploy** anything.

> **Deploying a model from SageMaker JumpStart creates a real-time inference endpoint that bills per instance-hour continuously — whether or not you send it a single request.** It does not stop when you close the browser tab. The same is true of a SageMaker Studio application or notebook instance. Step 3 and Step 6 return to this.

**Checkpoint:** You can state the one question that separates the three layers, and you know not to deploy anything in this lab.
