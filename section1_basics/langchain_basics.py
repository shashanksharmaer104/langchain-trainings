from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os

llm = ChatOllama(
    base_url="http://localhost:11434",
    model="llama3.2:latest",
    temperature=0.5,
    max=250
)

response = llm.invoke("Hello, how are you doing today?")

print(response)

load = load_dotenv('./../.env')

print(os.getenv('LANGSMITH_API_KEY'))