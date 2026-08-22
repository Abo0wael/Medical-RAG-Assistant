# Medical RAG Assistant 🩺

A Retrieval-Augmented Generation (RAG) application built using **LangGraph**, **LangChain**, **Streamlit**, **ChromaDB**, **HuggingFace Embeddings**, and **Groq**, specialized in answering medical questions.

This intelligent assistant uses state-of-the-art open-source LLMs through Groq's blazing-fast inference API, augmented by local document retrieval, to provide accurate and context-aware medical information.

---

## 🌟 Key Features

- **LangGraph Workflow**: Robust state management and flow control for the RAG pipeline.
- **Dynamic AI Models**: Switch seamlessly between powerful models like `openai/gpt-oss-120b`, `groq/compound`, and `qwen/qwen3.6-27b` via the sidebar.
- **Interactive Streamlit GUI**: A beautiful, responsive chat interface with predefined FAQ suggestions for quick onboarding.
- **Chroma Vector DB**: Fast, local vector database for document storage and retrieval.
- **HuggingFace Embeddings**: Local embedding generation using `BAAI/bge-base-en-v1.5` for high-quality semantic search.
- **Smart Query Rewriting**: Automatically refines user queries based on conversation history for better context retrieval.

---

## 🚀 Setup & Installation (Local Development)

### 1. Clone the repository
```bash
git clone https://github.com/Abo0wael/Medical-RAG-Assistant.git
cd Medical-RAG-Assistant
```

### 2. Set up a virtual environment
It is highly recommended to use Anaconda or Miniconda:
```bash
conda create -n rag_env python=3.10
conda activate rag_env
```

### 3. Install Dependencies
Install all required packages from the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
To connect to the Groq API, you need to set up your API keys.
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and replace `your_groq_api_key_here` with your actual [Groq API Key](https://console.groq.com/keys).

### 5. Run the Application
Start the Streamlit web server:
```bash
streamlit run app.py
```
The app will automatically open in your default browser at `http://localhost:8501`.

---

## ☁️ Deployment (Streamlit Community Cloud)

This project is configured to run smoothly on Streamlit Community Cloud:
1. Push this repository to your GitHub account.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and create a "New app".
3. Select your repository and `app.py` as the main file path.
4. **Important:** Before clicking "Deploy", go to **Advanced settings / Secrets** and add your Groq API key:
   ```toml
   GROQ_API_KEY = "your-actual-groq-api-key"
   ```
5. Click **Deploy**! (Note: We've already included the `pysqlite3-binary` patch in the code to ensure compatibility with Streamlit's environment).

---

## 📂 Project Structure

- `app.py`: Main application entry point (Streamlit UI layout and session state).
- `gui.py`: UI components (Custom CSS, Sidebar, Header, Chat rendering).
- `agents.py`: LangChain/LangGraph agent definitions (Query rewriting, Retrieval, Response generation).
- `ingest.py`: Script for ingesting and processing documents into the Chroma vector database.
- `models.py`: Defines the `State` classes used by LangGraph.
- `prompts.py`: Contains system prompts and templates for LLM interactions.
- `workflow.py`: Constructs the LangGraph nodes and edges for the RAG pipeline.
- `requirements.txt`: Frozen dependencies for exactly reproducible environments.
- `.env.example`: Template for environment variables.
