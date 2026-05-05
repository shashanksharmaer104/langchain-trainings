import os

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import chain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
#from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from dotenv import load_dotenv
import streamlit as st

# load ENV file
load = load_dotenv('./../.env', override=True)

# initialize LLM (local/cloud)
ollama_cloud_llm = ChatOllama(
    base_url="http://localhost:11434/",  # Ollama cloud endpoint
    model="devstral-small-2:24b-cloud", #gemini-3-flash-preview:cloud #qwen3.5:cloud
    temperature=0.5,
    max_tokens=350,
    headers={
        "Authorization": f"Bearer {os.getenv('OLLAMA_CLOUD_API_KEY')}"  # Cloud auth
    }
)

ollama_local_llm = ChatOllama(
    base_url="http://localhost:11434/",
    model="gemma3:1b",
    temperature=0.5,
    max_tokens=350
)

# Chat code
template = ChatPromptTemplate.from_messages([
    ("placeholder", "{history}"),
    ("human", "{prompt}")
])

chain = template | ollama_cloud_llm | StrOutputParser()

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    return SQLChatMessageHistory(session_id=session_id, connection_string="sqlite:///./chat_history.db")

history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="prompt",
    history_messages_key="history")

session_id = "Shashank"
session_id = st.text_input("Enter your name..", session_id)

st.title("How can I help you today?")
st.write("I can help you with a variety of questions and tasks. Just ask!")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Enter your message here...")

if prompt:
    response = history.invoke( {"prompt": prompt}, config={"configurable": {"session_id": session_id}})

    st.session_state.chat_history.append({"role": "user", "content": prompt})
    #st.write(f"User: {prompt}")
    with st.chat_message("user"):
        st.write(prompt)

    st.session_state.chat_history.append({"role": "assistant", "content": response})
    #st.write(f"Assistant: {response}")
    with st.chat_message("assistant"):
        st.write(response)
