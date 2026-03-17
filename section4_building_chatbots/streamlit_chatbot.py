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

# initialize LLM
ollama_local_llm = ChatOllama(
    base_url="http://localhost:11434/",
    model="llama3.2:latest ",
    temperature=0.5,
    max_tokens=350
)

# Chat code
template = ChatPromptTemplate.from_messages([
    ("placeholder", "{history}"),
    ("human", "{prompt}")
])

chain = template | ollama_local_llm | StrOutputParser()

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    return SQLChatMessageHistory(session_id=session_id, connection_string="sqlite:///./chat_history.db")

history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="prompt",
    history_messages_key="history")

session_id = "Shashank"

get_session_history(session_id).clear()

# response1 = history.invoke(
#     {"prompt": "What is the advantage of running the LLM in local machine? Just get me answer in bullet points and sub-bullet points. Keep the answer short."},
#     config={"configurable": {"session_id": session_id}})

# response2 = history.invoke(
#     {"prompt": "How about for cloud?"},
#     config={"configurable": {"session_id": session_id}})

st.title("Chatbot with Message History")
st.write("This is a simple chatbot application built using Streamlit and Langchain. The chatbot uses a message history to provide context-aware responses.")

prompt = st.chat_input("Enter your message here...")
