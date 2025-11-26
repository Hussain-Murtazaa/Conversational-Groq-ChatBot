💬 Groq Chatbot with Memory

A conversational AI app built using Streamlit, LangChain, and Groq LLMs, featuring real-time chat, persistent memory, customizable system prompts, and exportable chat history.

This project demonstrates how to use Groq's ultra-fast inference models (LLaMA 3, Qwen, Mixtral, Gemma2) inside a Streamlit chat interface with LangChain’s memory tools.

🚀 Features

⚡ Groq LLM Integration
Supports multiple high-speed Groq models:

qwen/qwen3-32b

llama-3.1-8b-instant

llama-3.3-70b-versatile

openai/gpt-oss-20b

llama-3.1-8b-instant

🧠 Chat Memory using
InMemoryChatMessageHistory + RunnableWithMessageHistory

🛡️ Hidden system rules preventing chain-of-thought leakage

🎛️ Sidebar controls

Model selection

Temperature

Max tokens

Custom system prompt

📤 Export chat as JSON

💬 Clean Streamlit Chat UI

📦 Installation
1. Clone the repo
git clone https://github.com/Hussain-Murtazaa/Conversational-Groq-Chatbot.git
cd groq-chatbot-memory

2. Create a virtual environment
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

3. Install dependencies
pip install -r requirements.txt

4. Add your Groq API key

Create a .env file in the project root:

GROQ_API_KEY=your_api_key_here


Get your free API key here:
https://console.groq.com/keys

▶️ Run the App
streamlit run app.py


Then open your browser at:

http://localhost:8501

🗂️ Project Structure
.
├── app.py               # Main Streamlit application
├── .env                 # API key (not included in repo)
├── requirements.txt     # Python dependencies
└── README.md            # Documentation

📚 Dependencies (requirements.txt)
streamlit
python-dotenv
langchain
langchain-core
langchain-groq
groq


(If needed for compatibility:)

pydantic<3.0

🧠 How It Works
🔹 Memory

Conversation history is stored using:

InMemoryChatMessageHistory()


Wrapped with:

RunnableWithMessageHistory


This ensures the LLM remembers previous messages within the session.

🔹 Prompt Flow

The prompt includes:

Hidden hard rules

User-provided system prompt

Chat history

The new user message

🔹 Streaming

The assistant response is shown with a typing animation.

🔹 Exporting Chat

Chats can be downloaded as a clean JSON:

[
  { "role": "user", "text": "Hello" },
  { "role": "assistant", "text": "Hi! How can I help?" }
]

🛠 Troubleshooting
❌ Missing GROQ_API_KEY

Ensure:

.env contains your API key

You ran load_dotenv()

You restarted Streamlit
