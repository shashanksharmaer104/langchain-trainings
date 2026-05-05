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

session_id = "Shashank"

st.title("How can I help you today?")
st.write("I can help you with a variety of questions and tasks. Just ask!")
session_id = st.text_input("Enter your name..", session_id)

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    return SQLChatMessageHistory(session_id=session_id, connection_string="sqlite:///./chat_history.db")

# Reset chat conversation
if st.button("Start new chat"):
    st.session_state.chat_history = []
    get_session_history(session_id).clear()  # Clear the database history for the session

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Enter your message here...")

#Chat code
template = ChatPromptTemplate.from_messages([
    ("placeholder", "{history}"),
    ("human", "{prompt}")
])

chain = template | ollama_cloud_llm | StrOutputParser()

def invoke_history(chain, session_id, prompt):
    history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="prompt",
    history_messages_key="history")

    for response in history.stream({"prompt": prompt}, config={"configurable": {"session_id": session_id}}):
        yield response

if prompt:
    # response = history.invoke( 
    #     {"prompt": prompt}, 
    #     config={"configurable": {"session_id": session_id}})

    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        streamResponse = st.write_stream(invoke_history(chain, session_id, prompt))

    st.session_state.chat_history.append({"role": "assistant", "content": streamResponse})
