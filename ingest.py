import os
from datasets import load_dataset
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

def ingest_data():
    print("Loading dataset from HuggingFace...")
    # Loading the entire Medical Q&A dataset
    dataset = load_dataset("keivalya/MedQuad-MedicalQnADataset", split="train")
    
    documents = []
    print("Preparing documents...")
    for row in dataset:
        q = row['Question']
        a = row['Answer']
        content = f"Question: {q}\nAnswer: {a}"
        doc = Document(page_content=content, metadata={"source": "MedQuad"})
        documents.append(doc)

    print(f"Loaded {len(documents)} documents.")
    
    print("Initializing embeddings model...")
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5", model_kwargs={'device': device})
    
    print("Creating vector database in './gen-ai'...")
    # This will create or update the chroma db in the persist_directory
    db = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory="gen-ai"
    )
    print("Ingestion complete! Vector DB is ready.")

if __name__ == "__main__":
    ingest_data()
