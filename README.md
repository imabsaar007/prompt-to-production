# 🚀 prompt-to-production

Welcome to **prompt-to-production**, my personal sandbox for exploring Generative AI, Large Language Models (LLMs), and orchestration frameworks. This repository serves as a living portfolio of my journey from understanding foundational prompt engineering to building fully autonomous agents and production-ready RAG pipelines.

## 🛠️ Tech Stack & Tools

- **Core Frameworks:** LangChain, LangGraph, LlamaIndex
- **LLM Providers:** OpenAI (GPT-4o), Anthropic (Claude 3.5 Sonnet), Ollama (Local Models)
- **Vector Databases:** ChromaDB / FAISS / Pinecone
- **Frontend/UI:** Streamlit / Chainlit
- **Languages & Utilities:** Python, Pydantic, Python-dotenv

---

## 📁 Repository Structure

```text
├── .gitignore
├── README.md
├── requirements.txt
├── .env.example
├── notebooks/               # Jupyter Notebooks for experimentation
│   ├── 01_prompt_engineering.ipynb
│   └── 02_langchain_basics.ipynb
└── projects/                # Standalone mini-applications
    ├── 01_pdf_rag_chatbot/  # Document QA using Retrieval-Augmented Generation
    │   ├── app.py
    │   └── utils.py
    └── 02_ai_agent/         # Autonomous agent with tool usage
        └── agent.py
```

---

## 🚀 Projects & Milestones

### 1. PDF Chatbot (RAG Pipeline)
- **Description:** A Streamlit application that allows users to upload PDF documents and ask questions based strictly on the content.
- **Key Concepts:** Text splitting (RecursiveCharacterTextSplitter), Embeddings (OpenAI / HuggingFace), Vector storage, and Contextual Retrieval.
- **Status:** 🛠️ In Progress / ✅ Completed

### 2. Autonomous Agent with Tool Use
- **Description:** An agent capable of deciding when to search the web, calculate math equations, or query a database to answer user prompts.
- **Key Concepts:** LangChain Tools, OpenAI Function Calling, AgentExecutor, and state management.
- **Status:** 📅 Planned

---

## ⚙️ Local Setup & Installation

Follow these steps to set up the development environment on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com
cd prompt-to-production
```

### 2. Set Up a Virtual Environment
```bash
# Create environment
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the root directory by copying the example file:
```bash
cp .env.example .env
```
Open the `.env` file and populate it with your respective API keys:
```text
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
```

---

## 📈 Learning Roadmap & Goals
- [ ] Master basic LangChain expression language (LCEL).
- [ ] Implement a fully local RAG pipeline using **Ollama** and **ChromaDB**.
- [ ] Learn **LangGraph** to build complex, cyclical multi-agent workflows.
- [ ] Evaluate LLM outputs using **LangSmith** to monitor latency, costs, and token usage.

---

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
