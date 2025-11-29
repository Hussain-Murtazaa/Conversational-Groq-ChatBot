from dotenv import load_dotenv
import os
import json
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Groq ChatBot", page_icon="🚀", layout="wide")

# Simple styling that works
st.markdown("""
<style>
body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.main { background: transparent; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Groq Conversational ChatBot")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    api_key_input = st.text_input("🔑 Groq API Key", type="password")
    api_key = api_key_input or GROQ_API_KEY
    
    model_name = st.selectbox(
        "🤖 Model",
        ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
    )
    
    temperature = st.slider("🌡️ Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.slider("📝 Max Tokens", 50, 500, 200)
    
    st.markdown("---")
    
    system_prompt = st.text_area(
        "✨ System Prompt",
        "You are a helpful, friendly assistant.",
        height=100
    )
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.history = InMemoryChatMessageHistory()
        st.rerun()

if not api_key:
    st.error("❌ Please enter your Groq API Key")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = InMemoryChatMessageHistory()

try:
    llm = ChatGroq(api_key=api_key, model=model_name, temperature=temperature, max_tokens=max_tokens)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    chat_with_history = RunnableWithMessageHistory(
        chain,
        lambda sid: st.session_state.history,
        input_messages_key="input",
        history_messages_key="history"
    )
    
    # Display messages
    for msg in st.session_state.history.messages:
        role = getattr(msg, "type", None) or getattr(msg, "role", "")
        content = msg.content
        if role == "human":
            st.chat_message("user").write(content)
        elif role in ("ai", "assistant"):
            st.chat_message("assistant").write(content)
    
    # Input
    user_input = st.chat_input("💬 Type here...")
    
    if user_input:
        st.chat_message("user").write(user_input)
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            response = chat_with_history.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": "default"}}
            )
            placeholder.write(response)
    
    # Export
    st.markdown("---")
    if st.session_state.history.messages:
        export = []
        for m in st.session_state.history.messages:
            role = getattr(m, "type", None) or getattr(m, "role", "")
            if role == "human":
                export.append({"role": "user", "text": m.content})
            elif role in ("ai", "assistant"):
                export.append({"role": "assistant", "text": m.content})
        
        st.download_button(
            "📥 Download History",
            json.dumps(export, indent=2),
            "chat_history.json",
            use_container_width=True
        )

except Exception as e:
    st.error(f"Error: {e}")
