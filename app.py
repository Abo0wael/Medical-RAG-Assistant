__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from models import State
from workflow import Workflow
from gui import render_header, render_sidebar, render_message
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Medical RAG Assistant", page_icon="🩺", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
selected_model = render_sidebar()

# Main UI Header
render_header()

# Quick FAQ suggestions for empty chat
if len(st.session_state.messages) == 0:
    st.markdown("### 💡 Frequently Asked Questions")
    col1, col2, col3 = st.columns(3)
    preset_question = None
    if col1.button("What is Glaucoma?", use_container_width=True):
        preset_question = "What is Glaucoma?"
    if col2.button("Symptoms of Tuberous Sclerosis", use_container_width=True):
        preset_question = "What are the symptoms of Tuberous Sclerosis?"
    if col3.button("Outlook for LEMS", use_container_width=True):
        preset_question = "What is the outlook for Lambert-Eaton Myasthenic Syndrome?"
else:
    preset_question = None

# Render chat history
for i, message in enumerate(st.session_state.messages):
    render_message(message, i)

# Check if a suggestion was clicked from history
if "preset_question" in st.session_state and st.session_state.preset_question:
    preset_question = st.session_state.preset_question
    st.session_state.preset_question = None

prompt = st.chat_input("Ask a medical question...")

if preset_question:
    prompt = preset_question

if prompt:
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    try:
        workflow = Workflow()
        
        initial_state = State(
            user_input=prompt,
            messages=st.session_state.messages.copy(),
            content=None,
            response=None,
            rewritten_query=None,
            selected_model=selected_model
        )
        
        with st.spinner(f"Processing with {selected_model}..."):
            result = workflow.run(initial_state)
            
            final_response = result.get('response', "Sorry, I couldn't generate a response.")
            
            # Store in session state
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": final_response})
            
            st.rerun()
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
