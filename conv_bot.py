from dotenv import load_dotenv
import os
import json
import time 
import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory

## SETUP
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 

st.set_page_config(page_title="Groq Chatbot with Memory", page_icon="💬")
st.title("💬 Groq Chatbot with Memory")

## sidebar 
with st.sidebar:
    st.subheader("Controls")
    api_key_input = st.text_input("Groq API Key", type="password")
    st.markdown(":gray[<font size='2'>Enter API Key if the bot is not working or you have paid API Key</font>]", unsafe_allow_html=True)
    api_key = api_key_input or os.getenv("GROQ_API_KEY")
   
    model_name = st.selectbox(
        "Groq Model",
        [
            "qwen/qwen3-32b",
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "openai/gpt-oss-20b",
            "llama-3.1-8b-instant"
        ],
        index=1
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.slider("Max Tokens", 50, 500, 200)


    HIDDEN_INSTRUCTION = """You are a helpful, friendly assistant.
CRITICAL RULES - NEVER BREAK THESE:
- Never use <think> or </think> tags under any circumstances.
- Never show internal reasoning or chain-of-thought.
- Never say "As an AI language model..." or similar.
- Always respond directly and naturally.

Now strictly follow the user's instructions below:"""

    user_custom_prompt = st.text_area(
        "System prompt (role/style yahan likho)",
        value="You are a helpful, concise teaching assistant. Use short, clear explanations.",
        height=150
    )

    final_system_prompt = HIDDEN_INSTRUCTION + "\n\n" + user_custom_prompt

    if st.button("Clear Chat"):
        st.session_state.pop("history", None)
        st.rerun()

# Accept key from input OR .env
if not api_key:
    st.warning("🔑 Please enter your Groq API Key (or set GROQ_API_KEY in .env).")
    st.stop()

# # API Key guard
# if not GROQ_API_KEY:
#     st.error("Missing GROQ_API_KEY. Add it to your .env or deployment secrets.")
#     st.stop()

# initilize single history
if "history" not in st.session_state:
    st.session_state.history = InMemoryChatMessageHistory()

# LLM + prompt + chain
# chat groq reads GROQ_API_KEY from .env

llm = ChatGroq(
    model=model_name,
    temperature=temperature,
    max_tokens=max_tokens
)


# Role - structured prompt: System -> History -> Human

prompt = ChatPromptTemplate.from_messages([
    ("system", final_system_prompt),           # ← yahan final_system_prompt
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm | StrOutputParser()

#wrap with message history
chat_with_history = RunnableWithMessageHistory(
    chain,
    # Given a session_id, return the corresponding history object
    lambda session_id: st.session_state.history,
    input_messages_key="input",
    history_messages_key="history"
)

# Render existing conversation
for msg in st.session_state.history.messages:
    role = getattr(msg,"type",None) or getattr(msg,"role","")
    content = msg.content
    if role == "human":
        st.chat_message("user").write(content)
    elif role in ("ai","asistant"):
        st.chat_message("user").write(content)
    elif role in ("ai","assistant"):
        st.chat_message("assistant").write(content)

# handle user turn
user_input = st.chat_input(
    "Type your Message...",
    key="chat_input",
    on_submit=None  
)

if user_input:
    # Display the user message on frontend
    st.chat_message("user").write(user_input)

    # invoke the chain with hisotry tracking

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            

            response_text = chat_with_history.invoke(
                {
                    "input": user_input,
                    "system_prompt": final_system_prompt      # ← yahan final_system_prompt daalo
                },
                config={"configurable": {"session_id": "default"}}
            )
            
        except Exception as e:
            st.error(f"Model error: {e}")
            response_text = ""

        # typing effect
        typed = ""
        for ch in response_text:
            typed += ch
            placeholder.markdown(typed)

# Download chat history (JSON)
if st.session_state.history.messages:
    # convert langchain messaage to simple (role,text)
    export = []
    for m in st.session_state.history.messages:
        role = getattr(m,"type",None) or getattr(m,"role","")
        if role == "human":
            export.append({"role":"user","text":m.content})
        elif role in("ai","assistant"):
            export.append({"role":"assistant","text":m.content})
    
    st.download_button(
        "Download chat JSON",
        data=json.dumps(export,ensure_ascii=False,indent=2),
        file_name="chat_history.json",
        mime="application/json",
        use_container_width=True
    ) 



