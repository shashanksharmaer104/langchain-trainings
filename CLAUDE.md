# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal LangChain training repository containing Jupyter notebooks and Python scripts for learning LangChain concepts. The codebase uses local LLMs via Ollama and integrates with LangSmith for API key management.

## Environment Setup

- Python virtual environment: `myenv312` (located at project root)
- Dependencies are defined in `requirements.txt`
- Environment variables are loaded from `.env` file at project root

## Running Code

```bash
# Activate the virtual environment
source myenv312/bin/activate

# Run a Python script
python section1_basics/langchain_basics.py

# Run Jupyter notebooks
jupyter notebook section1_basics/langchain_basics.ipynb
```

## Key Dependencies

- **langchain-core**, **langchain-community**: Core LangChain packages
- **langchain-ollama**: Local LLM integration (connects to http://localhost:11434)
- **langchain-openai**: OpenAI integration
- **langchain-chroma**: Vector store (Chroma)
- **ragas**, **deepeval**: Evaluation frameworks
- **pypdf**: Document loading

## Code Architecture

The main training content is in `section1_basics/`:
- `langchain_basics.py`: Python script demonstrating ChatOllama initialization
- `langchain_basics.ipynb`: Jupyter notebook with PromptTemplate and ChatPromptTemplate examples

Current LLM configuration uses Ollama with:
- Base URL: `http://localhost:11434`
- Model: `llama3.2:latest`
- Temperature: 0.5
- Max tokens: 250

## Testing

This project uses deepeval for testing (configuration in `.deepeval/` directory).
