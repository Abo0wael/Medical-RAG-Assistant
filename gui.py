import streamlit as st
import re
import os
import base64
from pathlib import Path

# Resolve absolute directory of this file
BASE_DIR = Path(__file__).parent.resolve()

def get_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Outfit', sans-serif !important;
        }

        .stChatMessage {
            border-radius: 15px !important;
            padding: 15px !important;
            margin-bottom: 15px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
            transition: all 0.3s ease;
        }
        
        .stChatMessage:hover {
            transform: translateY(-2px);
        }

        .main-title {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0px;
            font-size: 3.5rem !important;
            letter-spacing: -1px;
        }

        .subtitle {
            color: #8892b0;
            text-align: center;
            font-size: 1.2rem;
            margin-bottom: 40px;
            letter-spacing: 1px;
            font-weight: 300;
        }

        .suggestion-btn > button {
            border-radius: 25px !important;
            border: 1px solid rgba(79, 172, 254, 0.5) !important;
            background: rgba(79, 172, 254, 0.05) !important;
            color: #4facfe !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            padding: 10px 20px !important;
            margin-top: 10px !important;
        }

        .suggestion-btn > button:hover {
            background: #4facfe !important;
            color: #fff !important;
            box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4) !important;
            transform: translateY(-2px);
        }

        .main-title {
            text-align: left !important;
        }
        .subtitle {
            text-align: left !important;
        }
    </style>
    """

def render_header():
    st.markdown(get_css(), unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">Medical Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Powered by LangGraph &amp; Groq</p>', unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        selected_model = st.selectbox(
            "🧠 AI Model",
            options=["openai/gpt-oss-120b", "groq/compound", "qwen/qwen3.6-27b"],
            index=0,
            help="Choose the intelligence level of the AI."
        )

        st.divider()
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
            
        return selected_model

def render_message(message, idx):
    content = message["content"]
    suggestions = []
    
    if message["role"] == "assistant":
        # Remove <think>...</think> tags and their contents (even if unclosed)
        content = re.sub(r'<think>.*?(?:</think>|$)', '', content, flags=re.DOTALL).strip()

        # Extract suggestions
        clean_content = []
        for line in content.split('\n'):
            if line.strip().startswith("[SUGGESTION]"):
                sugg = line.replace("[SUGGESTION]", "").strip()
                if sugg:
                    suggestions.append(sugg)
            else:
                clean_content.append(line)
        content = "\n".join(clean_content)

    avatar = "🧑‍⚕️" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(content)
        
        # Display extracted suggestions as buttons (only for the last message)
        if suggestions and idx == len(st.session_state.messages) - 1:
            st.markdown("**Suggestions:**")
            cols = st.columns(len(suggestions))
            for i, sugg in enumerate(suggestions):
                with cols[i]:
                    st.markdown('<div class="suggestion-btn">', unsafe_allow_html=True)
                    if st.button(sugg, key=f"sugg_{idx}_{i}", use_container_width=True):
                        st.session_state.preset_question = sugg
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
