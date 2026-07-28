# 🛡️ PolicyBuddy

## AI-powered Compliance Assistant using RAG, LangGraph and LLM

PolicyBuddy is an AI assistant designed to help employees understand whether a specific action complies with company policies.

The system uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant internal policies and combines this information with a Large Language Model (LLM) to generate reliable, context-based compliance answers.

The main goal is to provide employees with quick guidance while reducing risks related to policy violations.

---


# 🎯 Project Objective

Organizations have many internal policies related to:

* Information Security
* Data Privacy
* Confidential Information
* Cloud Storage
* Acceptable Use
* Compliance Procedures

Employees often need quick answers about whether an action is allowed or prohibited.

PolicyBuddy solves this problem by:

1. Receiving a user question.
2. Searching internal policy documents.
3. Retrieving the most relevant information.
4. Sending the retrieved context to an LLM.
5. Generating a compliance-oriented response based only on approved sources.

---


# 🏗️ Architecture Overview

PolicyBuddy follows a **Retrieval-Augmented Generation architecture**.

User Question
|
v
Streamlit Interface
|
v
LangGraph Workflow
|
v
Retrieve Context Node
|
v
Retriever
|
v
ChromaDB Vector Database
|
v
Relevant Policy Documents
|
v
Context + Question
|
v
Generate Answer Node
|
v
Large Language Model (LLM)
|
v
Compliance Answer

---


# 🔄 LangGraph Workflow

# 🔄 LangGraph Workflow

PolicyBuddy uses **LangGraph** to orchestrate the RAG workflow. The current workflow contains two main nodes:


```
START

  |
  v

retrieve_context_node

  |
  v

generate_answer_node

  |
  v

END
```

## 1. Retrieve Context Node

Responsible for:

* Receiving the user's question.
* Querying the vector database.
* Finding relevant policy documents.
* Preparing the context that will be sent to the LLM.
* Adding retrieval metadata:

  * Retrieval status.
  * Evidence confidence.
  * Similarity score.

Example:

```
Question:
Can I upload internal files to an external cloud storage?

Retrieved information:

- Cloud Storage Security Policy
- Confidential Data Policy
- Internal Compliance Incident Report
```

---

## 2. Generate Answer Node

Responsible for:

* Creating the RAG chain.
* Loading the system prompt.
* Sending:

```
Question + Retrieved Context
```

to the LLM.

The LLM generates the final response following the compliance rules defined in the prompt.

---

# 🤖 LLM Integration

PolicyBuddy uses:

* Google Gemini LLM
* LangChain integration
* Custom system prompts

The LLM is not used as a general knowledge source.

The application follows a controlled approach:

```
Internal Policies
        +
Retrieved Context
        +
LLM Reasoning
        =
Compliance Response
```

The answer is grounded in the retrieved company documentation.

---

# 🔎 Retrieval-Augmented Generation (RAG)

The RAG pipeline contains:

## Document Loading

Supported formats:

* Markdown files (`.md`)
* PDF files (`.pdf`)

Documents are stored in: docs/

---

## Document Processing

The pipeline:

1. Loads documents.
2. Splits documents into smaller chunks.
3. Generates embeddings.
4. Stores vectors.

---

## Embeddings

PolicyBuddy uses:

```
BAAI/bge-small-en-v1.5
```

through Hugging Face Transformers.

Embeddings allow semantic search instead of only keyword matching.

Example:

A user asks:

```
Can I send company files using my personal email?
```

The system can retrieve policies mentioning:

```
unauthorized sharing
personal accounts
confidential information
external communication
```

---

## Vector Database

PolicyBuddy uses ChromaDB as the vector database for storing document embeddings.

During the indexing process, documents from the `docs/` directory are converted into embeddings and persisted by ChromaDB. The retriever uses this database to search relevant policy information before sending the context to the LLM.

---

# 🛠️ Technology Stack

## Frontend

* Streamlit

## AI Frameworks

* LangChain
* LangGraph

## LLM

* Google Gemini

## Retrieval

* ChromaDB
* Hugging Face Embeddings

## Document Processing

* PyPDF
* Markdown loaders

## Development

* Python 3.12
* Git
* VS Code

---

# 📂 Project Structure

```
PolicyBuddy/

├── docs/
│   └── Internal policy documents
│
├── vectorstore/
│   └── ChromaDB database
│
├── src/
│   └── policybuddy/
│
│       ├── app/
│       │   └── Streamlit interface
│       │
│       ├── graph/
│       │   └── LangGraph workflow
│       │
│       ├── rag/
│       │   ├── loader.py
│       │   ├── splitter.py
│       │   ├── embeddings.py
│       │   ├── retriever.py
│       │   └── store.py
│       │
│       ├── llm/
│       │   ├── chains.py
│       │   └── providers.py
│       │
│       └── prompts/
│           └── system_prompt.txt
│
├── tests/
│
├── .env
├── pyproject.toml
└── README.md
```

---

# 🚀 Running Locally

## Requirements

Install:

* Python 3.12+
* Git
* VS Code (recommended)

---

# 1. Clone Repository

```bash
git clone <https://github.com/MLeticiaNascimento/policybuddy>

cd src/policybuddy
```

---

# 2. Create Virtual Environment

Windows:

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux/macOS:

```bash
python -m venv .venv

source .venv/bin/activate
```

---

# 3. Install Dependencies

Using pip:

```bash
pip install -r requirements.txt
```

or using uv:

```bash
uv sync
```

---

# 4. Configure Environment Variables

Create a file: .env

Add: GOOGLE_API_KEY=your_gemini_api_key

Example file: .env.example

---

## 5. Create Vector Database

Before running the application, create the ChromaDB vector database by processing the documents stored in the `docs/` folder.

The pipeline loads the documents, splits them into chunks, generates embeddings using the configured Hugging Face model, and stores the vectors for retrieval.

Run:

```bash
python scripts/build_vectorstore.py
```


# 6. Run Application

Start Streamlit:

```bash
streamlit run src/policybuddy/app/app.py
```

---

# 🧪 Testing Examples

Examples of questions:

```
Can I use my personal email to send company documents?
```

```
Can I upload internal files to an external cloud storage?
```

```
Am I allowed to paste confidential source code into ChatGPT?
```

Expected flow:

```
User Question

↓

LangGraph starts

↓

Retriever searches ChromaDB

↓

Relevant policies are selected

↓

Context is sent to Gemini

↓

LLM generates compliance response
```

---

# 🧰 Troubleshooting

## Gemini connection error

Check:

* `.env` exists.
* API key is valid.
* Environment variable name is:

```
GOOGLE_API_KEY
```

---

## No documents retrieved

Verify:

* Documents exist in:

```
docs/
```

* Vector database was created.

Rebuild:

```bash
python -m policybuddy.rag.store
```

---

## Streamlit cache

Clear cache:

```bash
streamlit cache clear
```

Restart the application.

---

# 🔁 Reproducibility

A new developer should be able to run PolicyBuddy by following:

1. Clone repository.
2. Install dependencies.
3. Configure Gemini API key.
4. Add policy documents.
5. Generate ChromaDB vector database.
6. Start Streamlit.

No model training is required.

PolicyBuddy uses a production-oriented **Retrieval-Augmented Generation architecture**, combining deterministic document retrieval with LLM reasoning.
