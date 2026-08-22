from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from models import State
from prompts import *
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import torch
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5", model_kwargs={'device': device})

try:
    persist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vector")
    vdb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
    )
    retriever = vdb.as_retriever()
except Exception as e:
    print(f"Warning: Vector DB not initialized yet or error loading: {e}")
    retriever = None

def rewitten_query_agent(state: State) -> dict:
    user_input: str = state.get("user_input", "")
    chat_history: list = state.get("messages", [])
    
    # Initialize LLM dynamically based on the selected model
    model_name = state.get("selected_model")
    if not model_name:
        model_name = "openai/gpt-oss-120b"
    
    chat_history_str = ""
    if chat_history:
        for msg in chat_history:
            if isinstance(msg, dict):
                role = msg.get('role', 'message')
                content = msg.get('content', str(msg))
            else:
                role = getattr(msg, 'type', 'message')
                content = getattr(msg, 'content', str(msg))
            chat_history_str += f"{role}: {content}\n"

    api_key = os.environ.get("GROQ_API_KEY")
    llm = ChatGroq(model=model_name, temperature=0.0, api_key=api_key)

    user_content = REWRITE_USER_PROMPT_TEMPLATE.replace("{user_input}", user_input).replace("{chat_history}", chat_history_str)

    messages: list = [
        SystemMessage(content=REWRITE_SYSTEM_PROMPT),
        HumanMessage(content=user_content)
    ]

    try:
        response: str = llm.invoke(messages).content
        return {"rewritten_query": response}
    except Exception as e:
        print(f"Error in rewriting query: {e}")
        # Return the actual error for debugging
        return {"rewritten_query": f"ERROR: {str(e)}"}

def retriever_agent(state: State) -> dict:
    rewritten_query: str = state.get("rewritten_query") or state.get("user_input")

    if retriever is None:
        return {"content": []}

    try:
        results = retriever.invoke(rewritten_query)
        content_strings = [doc.page_content for doc in results]
        return {"content": content_strings}
    except Exception as e:
        print(f"Error in retrieval: {e}")
        return {"content": [f"ERROR: {str(e)}"]}

def response_agent(state: State) -> dict:
    rewritten_query: str = state.get("rewritten_query") or state.get("user_input")
    chat_history: list = state.get("messages", [])
    content_list: list = state.get("content", [])
    
    # Initialize LLM dynamically
    model_name = state.get("selected_model")
    if not model_name:
        model_name = "openai/gpt-oss-120b"
        
    api_key = os.environ.get("GROQ_API_KEY")
    llm = ChatGroq(model=model_name, temperature=0.0, api_key=api_key)
    
    content_str = "\n\n".join(content_list) if content_list else "No relevant context found."

    chat_history_str = ""
    for msg in chat_history:
        if isinstance(msg, dict):
            chat_history_str += f"{msg.get('role', 'message')}: {msg.get('content', str(msg))}\n"
        elif hasattr(msg, 'content'):
            chat_history_str += f"{getattr(msg, 'type', 'message')}: {msg.content}\n"
        else:
            chat_history_str += f"message: {str(msg)}\n"

    sys_prompt = state.get("system_prompt")
    if not sys_prompt:
        sys_prompt = MACHINE_SYSTEM_PROMPT
        
    usr_prompt_template = state.get("user_prompt_template")
    if not usr_prompt_template:
        usr_prompt_template = USER_INPUT_PROMPT_TEMPLATE

    user_content = usr_prompt_template.replace("{user_input}", rewritten_query)
    user_content = user_content.replace("{chat_history}", chat_history_str)
    user_content = user_content.replace("{content}", content_str)

    messages: list = [
        SystemMessage(content=sys_prompt),
        HumanMessage(content=user_content)
    ]

    try:
        response: str = llm.invoke(messages).content
        return {"response": response}
    except Exception as e:
        print(f"Error in response: {e}")
        return {"response": f"I apologize, but I encountered an error: {str(e)}"}