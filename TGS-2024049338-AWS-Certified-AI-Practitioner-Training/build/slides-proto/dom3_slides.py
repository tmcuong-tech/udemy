# ============================================================ DOMAIN 3
# Applications of Foundation Models — 28% (heaviest domain) · Tasks 3.1–3.4 · Labs 12–18
# RAW statements exec'd inside build_slides.py (components + palette in scope).

section("DOMAIN 3","Applications of Foundation Models","28%",
 sub="Exam weighting 28% · Tasks 3.1–3.4 · Labs 12–18")

# ---------------- Task 3.1 — Design considerations for FM applications ----------------
tile_grid("Designing a Foundation Model Application",[
 ("Choose the model","Match capability, context window, cost and latency to the task."),
 ("Ground the outputs","Feed the model your own trusted data with RAG."),
 ("Steer with prompts","Prompt engineering shapes tone, format and behaviour."),
 ("Customise if needed","Fine-tune only when prompting and RAG fall short."),
 ("Add guardrails","Filter harmful content, block topics, redact PII."),
 ("Evaluate & monitor","Measure quality with metrics and human review.")],
 kicker="TASK 3.1 · DESIGN CONSIDERATIONS",cols=3,size=13)

tile_grid("Selecting the Right Foundation Model",[
 ("Task fit","Text generation, summarisation, Q&A, code, image, embeddings."),
 ("Context window","How much input the model can take in one prompt."),
 ("Cost","Priced per input and output token — larger models cost more."),
 ("Latency & throughput","Response time and requests the app must sustain."),
 ("Modality","Text-only vs multimodal (image + text) requirements."),
 ("Customisation","Whether the model supports fine-tuning on Bedrock.")],
 kicker="TASK 3.1 · MODEL SELECTION",cols=3,size=13)

cards3("Three Ways to Customise Model Behaviour",[
 (BLUE,"Prompt engineering",["No training, lowest cost","Instructions + examples in the prompt","Fast to iterate; start here"]),
 (TEAL,"RAG",["Inject your data at query time","Grounds answers, cuts hallucination","No model retraining needed"]),
 (VIOLET,"Fine-tuning",["Retrain on labelled examples","Best when behaviour must change","Highest cost — data + compute"])],
 kicker="TASK 3.1 · PROMPT vs RAG vs FINE-TUNE")

big_statement("Start with the prompt, then reach for RAG, fine-tune last.",
 "Prompt engineering is cheapest and fastest. RAG adds your knowledge without retraining. Fine-tuning is powerful but costs data, compute and time.",
 "TASK 3.1 · A DECISION LADDER",color=BLUE)

flow_h("Retrieval Augmented Generation (RAG) Pipeline",[
 "User asks a question",
 "Embed the query into a vector",
 "Search the vector store for relevant chunks",
 "Augment the prompt with retrieved context",
 "Model generates a grounded answer"],
 kicker="TASK 3.1 · RAG",color=TEAL)

content("Why RAG Grounds Answers and Reduces Hallucination",[
 "A foundation model only knows what it saw in training — it can confidently invent facts (hallucinate).",
 "RAG retrieves relevant passages from your trusted documents and adds them to the prompt as context.",
 "The model answers from that supplied context instead of guessing, so responses stay grounded.",
 "You can surface source citations, giving users a way to verify each answer.",
 "Knowledge stays current and private: update the documents, not the model — no retraining required."],
 kicker="TASK 3.1 · WHY RAG",size=18)

two_col("Knowledge Bases, Embeddings & Vector Stores",[
 ("Knowledge Bases for Amazon Bedrock",0),
 ("Managed RAG — connects a model to your data",1),
 ("Ingests, chunks and embeds source documents",1),
 ("Handles retrieval and prompt augmentation for you",1),
 ("Returns answers with source attribution",1)],
 [("Embeddings & vector stores",0),
 ("Embeddings turn text into numeric vectors",1),
 ("Similar meaning → nearby vectors",1),
 ("Stored and searched in a vector database",1),
 ("e.g. Amazon OpenSearch Serverless, Aurora pgvector",1)],
 kicker="TASK 3.1 · KNOWLEDGE BASES",lhead="Managed RAG on Bedrock",rhead="How retrieval works")

picture("Retrieval Augmented Generation (RAG)","s197_0.png",
 caption="RAG retrieves relevant context from a knowledge source and augments the prompt before generation.",
 kicker="TASK 3.1 · RAG IN PRACTICE")

picture("Amazon Bedrock","s193_0.png",
 caption="Amazon Bedrock delivers foundation models, Knowledge Bases and Guardrails through a single managed API.",
 kicker="TASK 3.1 · THE PLATFORM")

tile_grid("Beyond RAG — Agents & Orchestration",[
 ("Amazon Bedrock Agents","Break a task into steps and call APIs / tools."),
 ("Action groups","Let the model invoke your functions to act."),
 ("Knowledge Bases","Give the agent grounded data to reason over."),
 ("Multi-step reasoning","Chain retrieval, tool calls and generation.")],
 kicker="TASK 3.1 · AGENTS",cols=2,size=15)

# ---------------- Task 3.2 — Prompt engineering ----------------
section("TASK 3.2","Prompt Engineering","",
 sub="Anatomy · shot techniques · chain-of-thought · risks & defences")

tile_grid("Anatomy of a Prompt",[
 ("Instructions","The task you want the model to perform."),
 ("Context","Background or retrieved data to ground the answer."),
 ("Input data","The specific content to act on."),
 ("Output indicator","The format, structure or style you expect back.")],
 kicker="TASK 3.2 · PROMPT ANATOMY",cols=2,size=15)

two_col("Shot Techniques — Learning from Examples",[
 ("Zero-shot",0),
 ("Just the instruction, no examples",1),
 ("Relies on the model's pre-trained knowledge",1),
 ("One-shot",0),
 ("A single worked example in the prompt",1)],
 [("Few-shot",0),
 ("Several examples showing the pattern",1),
 ("Steers format, tone and edge cases",1),
 ("More examples → clearer intent",1),
 ("Costs more tokens per request",1)],
 kicker="TASK 3.2 · ZERO / ONE / FEW-SHOT",lhead="Zero & one-shot",rhead="Few-shot")

tile_grid("Advanced Prompting Techniques",[
 ("Chain-of-thought","Ask the model to reason step by step for complex tasks."),
 ("Prompt templates","Reusable prompts with placeholders for consistency."),
 ("Negative prompting","State what to avoid or exclude from the output."),
 ("Role / persona","Assign a role to shape tone and expertise.")],
 kicker="TASK 3.2 · TECHNIQUES",cols=2,size=15)

picture("Prompt Engineering Techniques","s214_0.png",
 caption="Zero-shot, few-shot and chain-of-thought prompting each steer the model toward better answers.",
 kicker="TASK 3.2 · IN PRACTICE")

two_col("Prompt Risks & Defences",[
 ("Risks",0),
 ("Prompt injection — hidden instructions hijack the model",1),
 ("Jailbreaking — bypassing safety rules",1),
 ("Prompt leaking — exposing the system prompt",1),
 ("Poisoning of retrieved or external content",1)],
 [("Defences",0),
 ("Guardrails for Amazon Bedrock — content filters",1),
 ("Denied topics and word filters",1),
 ("PII detection and redaction",1),
 ("Separate trusted instructions from user input",1)],
 kicker="TASK 3.2 · SECURITY",lhead="What can go wrong",rhead="How to defend")

big_statement("Never trust the prompt alone.",
 "Guardrails for Amazon Bedrock apply content filters, denied topics and PII redaction consistently across models — a safety layer independent of any single prompt.",
 "TASK 3.2 · GUARDRAILS",color=AMBER)

# ---------------- Task 3.3 — Training & fine-tuning ----------------
section("TASK 3.3","Training & Fine-Tuning","",
 sub="Pre-training · fine-tuning · continued pre-training · instruction tuning")

cards3("From Pre-Training to Fine-Tuning",[
 (BLUE,"Pre-training",["Trained on massive general data","Learns language & world patterns","Done by the model provider"]),
 (TEAL,"Fine-tuning",["Further training on labelled examples","Adapts to a specific task or style","You supply the training data"]),
 (VIOLET,"Continued pre-training",["More unlabelled domain data","Deepens domain knowledge","No task labels required"])],
 kicker="TASK 3.3 · TRAINING APPROACHES")

content("Instruction Tuning",[
 "Instruction tuning fine-tunes a model on prompt-and-response pairs that demonstrate desired behaviour.",
 "It teaches the model to follow instructions and produce answers in the format you want.",
 "The result is a model aligned to your task without you writing lengthy prompts every time.",
 "On Amazon Bedrock you supply labelled examples; the service manages the fine-tuning job and hosts the custom model."],
 kicker="TASK 3.3 · INSTRUCTION TUNING",size=18)

two_col("When Is Fine-Tuning Worth It?",[
 ("Fine-tune when",0),
 ("Prompting and RAG can't reach the quality you need",1),
 ("You need a consistent tone, format or domain voice",1),
 ("You have enough high-quality labelled examples",1),
 ("The task is stable and repeated at scale",1)],
 [("Think twice when",0),
 ("Data is scarce, noisy or changes often",1),
 ("Budget for compute and data prep is limited",1),
 ("RAG could supply the missing knowledge instead",1),
 ("Requirements are still shifting",1)],
 kicker="TASK 3.3 · COST vs DATA",lhead="Good fit",rhead="Reconsider")

# ---------------- Task 3.4 — Evaluating FM performance ----------------
section("TASK 3.4","Evaluating Foundation Model Performance","",
 sub="Automatic metrics · benchmarks · human evaluation · Bedrock model evaluation")

tile_grid("Automatic Evaluation Metrics",[
 ("ROUGE","Overlap of words/phrases — used for summarisation."),
 ("BLEU","Precision of n-grams — used for translation."),
 ("BERTScore","Semantic similarity using embeddings, not exact match."),
 ("Perplexity","How well the model predicts the next token.")],
 kicker="TASK 3.4 · METRICS",cols=2,size=15)

flow_h("Amazon Bedrock Model Evaluation",[
 "Pick candidate models",
 "Choose a task type & dataset",
 "Select automatic metrics or human review",
 "Run the evaluation job",
 "Compare scores and select a model"],
 kicker="TASK 3.4 · WORKFLOW",color=TEAL)

two_col("Automatic vs Human Evaluation",[
 ("Automatic evaluation",0),
 ("Fast, repeatable, low cost",1),
 ("Metrics like ROUGE, BLEU, BERTScore",1),
 ("Great for regression and A/B checks",1),
 ("May miss nuance and correctness",1)],
 [("Human evaluation",0),
 ("People rate helpfulness, accuracy, tone",1),
 ("Catches subtle quality and safety issues",1),
 ("Slower and more costly",1),
 ("Bedrock supports human review workflows",1)],
 kicker="TASK 3.4 · METHODS",lhead="Machine metrics",rhead="Human judgement")

content("Benchmarks & Choosing What to Measure",[
 "Benchmarks are standard datasets that let you compare models on the same task under the same conditions.",
 "Pick metrics that match the job: ROUGE for summarisation, BLEU for translation, BERTScore for semantic match.",
 "No single number is enough — combine automatic metrics with human review for quality and safety.",
 "Amazon Bedrock model evaluation runs both automatic and human evaluations so you can pick the best model for your use case."],
 kicker="TASK 3.4 · BENCHMARKS",size=18)

picture("Amazon Q","s270_0.png",
 caption="Amazon Q is a generative AI assistant that applies these FM application patterns to real business tasks.",
 kicker="TASK 3.4 · APPLYING FMs")

# ---------------- Recap ----------------
content("Domain 3 — Key Takeaways",[
 "Customise behaviour in order of cost: prompt engineering, then RAG, then fine-tuning.",
 "RAG retrieves your trusted data at query time to ground answers and cut hallucination — Knowledge Bases for Amazon Bedrock makes it managed.",
 "Prompts have four parts (instructions, context, input, output); zero/one/few-shot and chain-of-thought steer results — guard against injection and jailbreaking with Guardrails for Amazon Bedrock.",
 "Fine-tuning and continued pre-training adapt a model when prompting and RAG aren't enough, at the cost of data and compute.",
 "Evaluate with the right metric (ROUGE, BLEU, BERTScore) plus human review; Amazon Bedrock model evaluation runs both."],
 kicker="RECAP")
