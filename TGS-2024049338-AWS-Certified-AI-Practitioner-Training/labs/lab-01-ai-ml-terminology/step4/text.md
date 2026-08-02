# Step 4 — Separate algorithm, model, training and inference

These four words are used loosely in conversation and precisely on the exam.

### 4.1 Definitions

- **Algorithm** — the *procedure* for learning. XGBoost, K-Means and a neural network
  architecture are algorithms. An algorithm on its own has learned nothing.
- **Training** — running the algorithm over a dataset so that it adjusts internal
  parameters (in a neural network, the **weights** and **biases**) to reduce error.
- **Model** — the *artefact produced by training*: the learned parameters plus enough
  structure to reproduce the computation. In SageMaker this is a `model.tar.gz` file in
  Amazon S3, registered as a SageMaker **model** object.
- **Inference** — using a trained model to produce an output for new, unseen input. Also
  called prediction or scoring.

A one-line summary worth memorising: **algorithm + data → training → model → inference → prediction.**

### 4.2 Neural network vocabulary

A neural network is layers of connected **neurons** (nodes):

- **Input layer** takes the features.
- **Hidden layers** transform them. "Deep" simply means more than one hidden layer.
- **Output layer** produces the prediction.
- **Weights and biases** are the learned parameters adjusted during training.
- **Activation function** introduces non-linearity, letting the network model curves and
  interactions a linear model cannot.
- An **epoch** is one full pass over the training data.

Distinguish **parameters** (learned by training — weights and biases) from
**hyperparameters** (set *before* training — learning rate, number of layers, batch size).
The exam tests this pair often, and Lab 05 revisits hyperparameter tuning.

### 4.3 See the artefacts in the console

1. Open the **Amazon SageMaker AI** console.
2. In the left navigation, expand the training section and choose **Training jobs**. This
   is where *training* runs are recorded — each has an input data location, an algorithm
   or container image, hyperparameters, and an output S3 path.
3. In the left navigation, find **Models** (under the inference section). This is the
   registry of trained *model* artefacts that can be deployed.
4. Still under inference, open **Endpoints**. An endpoint is where *inference* happens.

If your account is new all three lists will be empty. That is expected — the point is to
see that AWS gives training, models and inference three separate console pages, because
they are three separate stages with separate costs and separate lifecycles. Lab 04 fills
all three lists in.
