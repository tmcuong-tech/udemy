# ---------------- DOMAIN 2 ----------------
section("DOMAIN 2","Fundamentals of Generative AI","24%",sub="Exam weighting 24% · Tasks 2.1–2.3 · Labs 6–11")

# ---- Task 2.1 · Basic concepts of generative AI ----
big_statement("Generative AI creates new content.","Foundation models trained on massive data generate text, images, code and more from a prompt.","TASK 2.1 · WHAT IS GENERATIVE AI",color=BLUE)

picture("Generative AI in Action","s138_0.png",caption="Generative AI produces original text, images and code from a natural-language prompt.",kicker="TASK 2.1 · EXAMPLE")

tile_grid("What Is a Foundation Model?",[
 ("Foundation Model (FM)","A large model pre-trained on broad data, adaptable to many tasks."),
 ("General-purpose","One model serves summarisation, Q&A, translation, code and more."),
 ("Large-scale","Billions of parameters trained on huge text/image corpora."),
 ("Reusable","Adapt one FM to many jobs instead of training from scratch.")],
 kicker="TASK 2.1 · FOUNDATION MODELS",cols=2,size=15)

picture("Foundation Models","s180_0.png",caption="A single foundation model can be adapted to power many downstream tasks.",kicker="TASK 2.1 · FOUNDATION MODELS")

two_col("Pre-training vs Adaptation",[
 ("Pre-training",0),
 ("Learn general language / patterns from massive unlabelled data",1),
 ("Expensive, done once by the model provider",1),
 ("Produces the base foundation model",1)],
 [("Adaptation",0),
 ("Fine-tuning — further train on task/domain data",1),
 ("Prompt engineering & in-context examples",1),
 ("Retrieval-augmented generation for fresh context",1)],
 kicker="TASK 2.1 · TRAIN THEN ADAPT",lhead="Pre-training",rhead="Adaptation")

tile_grid("Tokens & Context Window",[
 ("Tokens","Text split into sub-word units the model reads and predicts."),
 ("Tokenization","Words map to token IDs; cost and limits are counted in tokens."),
 ("Context window","Max tokens (input + output) a model can handle at once."),
 ("Why it matters","Long prompts / documents must fit within the window.")],
 kicker="TASK 2.1 · TOKENS",cols=2,size=15)

picture("Context Window","s154_0.jpg",caption="The context window bounds how many tokens of input and output a model can process together.",kicker="TASK 2.1 · CONTEXT WINDOW")

tile_grid("Embeddings & Vector Representations",[
 ("Embedding","Text or images encoded as a numeric vector."),
 ("Meaning as geometry","Similar meanings sit close together in vector space."),
 ("Similarity search","Compare vectors to find related content."),
 ("Powers RAG","Vector search retrieves relevant context for the model.")],
 kicker="TASK 2.1 · EMBEDDINGS",cols=2,size=15)

picture("Embeddings","s157_0.png",caption="Embeddings turn content into vectors so semantically similar items are near one another.",kicker="TASK 2.1 · EMBEDDINGS")

flow_h("How a Model Generates Text",[
 "Prompt is tokenized into input tokens",
 "Model reads context and predicts the next token",
 "Token is appended to the sequence",
 "Repeat, one token at a time",
 "Stop at a limit or stop signal"],kicker="TASK 2.1 · NEXT-TOKEN PREDICTION")

tile_grid("Prompting Basics",[
 ("Prompt","The instruction and context you give the model."),
 ("Be specific","Clear task, format and constraints improve output."),
 ("Few-shot","Include examples to guide the response."),
 ("Iterate","Refine wording and context to steer results.")],
 kicker="TASK 2.1 · PROMPTING",cols=2,size=15)

# ---- Task 2.2 · Capabilities & limitations ----
tile_grid("What Generative AI Can Do",[
 ("Summarise","Condense long documents into key points."),
 ("Generate","Draft text, images, marketing and ideas."),
 ("Translate","Convert between languages."),
 ("Write code","Generate, explain and debug code."),
 ("Chat & assist","Conversational Q&A and virtual assistants."),
 ("Extract","Pull entities and structure from unstructured text.")],
 kicker="TASK 2.2 · CAPABILITIES",cols=3,size=13)

tile_grid("Limitations to Know",[
 ("Hallucination","Can produce confident but incorrect answers."),
 ("Non-determinism","Same prompt may give different outputs."),
 ("Knowledge cutoff","No awareness of events after training."),
 ("Bias","Can reflect bias present in training data."),
 ("Cost & latency","Large models add compute cost and response time."),
 ("No true reasoning","Predicts tokens; it does not verify facts.")],
 kicker="TASK 2.2 · LIMITATIONS",cols=3,size=13)

big_statement("Fit the tool to the problem.","Generative AI suits open-ended language and content tasks — not exact, deterministic calculations or hard guarantees.","TASK 2.2 · WHEN GEN-AI FITS",color=AMBER)

tile_grid("Does Generative AI Fit This Problem?",[
 ("Good fit","Content creation, summarisation, chat, code assistance."),
 ("Poor fit","Exact math, guaranteed outputs, simple rules."),
 ("Needs grounding","Add retrieval / RAG when facts must be current."),
 ("Weigh trade-offs","Balance quality, cost, latency and risk.")],
 kicker="TASK 2.2 · BUSINESS FIT",cols=2,size=15)

# ---- Task 2.3 · AWS infrastructure for generative AI ----
big_statement("Amazon Bedrock: build with FMs.","A fully managed service to access leading foundation models through one serverless API.","TASK 2.3 · AWS INFRASTRUCTURE",color=BLUE)

tile_grid("Amazon Bedrock",[
 ("Managed FM API","Call foundation models through a single API."),
 ("Model choice","Access multiple providers' models in one place."),
 ("Serverless","No infrastructure to provision or manage."),
 ("Customisation","Fine-tuning and retrieval-augmented generation."),
 ("Agents & KBs","Build agents and knowledge bases on your data."),
 ("Secure","Runs within your AWS security and privacy controls.")],
 kicker="TASK 2.3 · AMAZON BEDROCK",cols=3,size=13)

tile_grid("Amazon Q Business",[
 ("Generative AI assistant","Answers questions from your enterprise data."),
 ("Connects your data","Links to company documents and sources."),
 ("Grounded answers","Responds using your content, with references."),
 ("Everyday productivity","Summarise, draft and search across content.")],
 kicker="TASK 2.3 · AMAZON Q",cols=2,size=15)

picture("Amazon SageMaker JumpStart","s150_0.png",caption="SageMaker JumpStart offers pre-trained foundation models you can deploy and fine-tune.",kicker="TASK 2.3 · SAGEMAKER")

cards3("Choosing the Right Service",[
 (BLUE,"Managed AI services",["Ready-made APIs","e.g. Comprehend, Rekognition","Least effort, fixed tasks"]),
 (TEAL,"Amazon Bedrock",["Foundation models via API","Serverless, multi-model","Build gen-AI apps fast"]),
 (VIOLET,"Amazon SageMaker",["Full ML control","Build, train, deploy custom","Most effort, most flexible"])],
 kicker="TASK 2.3 · DECISION")

two_col("Bedrock vs SageMaker",[
 ("Amazon Bedrock",0),
 ("Consume foundation models via API",1),
 ("Serverless — no model hosting to manage",1),
 ("Best for building gen-AI apps quickly",1)],
 [("Amazon SageMaker",0),
 ("Build, train and host your own models",1),
 ("Full control of the ML lifecycle",1),
 ("Best when you need custom models / MLOps",1)],
 kicker="TASK 2.3 · DECISION",lhead="Bedrock",rhead="SageMaker")

# ---- Recap ----
content("Domain 2 — Key Takeaways",[
 "Foundation models are large, pre-trained models adapted to many tasks; adaptation includes fine-tuning, prompting and RAG.",
 "Models read text as tokens, generate one token at a time, and are bounded by a context window.",
 "Embeddings represent content as vectors so similar meanings sit close together — the basis of similarity search and RAG.",
 "Gen-AI excels at summarising, generating, translating, coding and chat, but risks hallucination, non-determinism, knowledge cutoff, bias and cost/latency.",
 "Amazon Bedrock gives serverless API access to foundation models; use managed AI services for ready tasks and Amazon SageMaker for custom models."],kicker="RECAP")
