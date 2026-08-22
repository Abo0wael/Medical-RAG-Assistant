# Medical RAG Assistant

A Retrieval-Augmented Generation (RAG) application built using LangGraph, LangChain, Streamlit, Chroma, HuggingFace Embeddings, and Groq, specialized in answering medical questions.

## Features
- **LangGraph Workflow**: Manages the state and flow of the RAG pipeline.
- **Streamlit GUI**: Interactive web interface for the application.
- **Chroma DB**: Local vector database for document storage and retrieval.
- **HuggingFace Embeddings**: Local embeddings generation.
- **Groq LLM**: Fast inference for conversational responses.

## Setup Instructions

1. **Clone the repository** (if not already done).

2. **Set up the environment**:
Ensure you have Anaconda or Miniconda installed. Create and activate an environment (e.g., `rag_env`).
```bash
conda create -n rag_env python=3.10
conda activate rag_env
```

3. **Install Dependencies**:
Install all the required packages specified in `requirements.txt`.
```bash
pip install -r requirements.txt
```

4. **Environment Variables**:
Create a `.env` file in the root directory and add the necessary API keys (like Groq API key, etc.).

5. **Run the Application**:
You can start the Streamlit application by running:
```bash
streamlit run app.py
```
*(Note: If `gui.py` is the main entry point, run `streamlit run gui.py` instead.)*

## Project Structure
- `app.py` / `gui.py`: Application entry points (Streamlit UI).
- `agents.py`: Contains definitions for LangChain/LangGraph agents.
- `ingest.py`: Handles document ingestion into the Chroma vector database.
- `models.py`: Defines the state and data models.
- `prompts.py`: Contains system prompts and templates.
- `workflow.py`: Sets up the LangGraph nodes and edges.
