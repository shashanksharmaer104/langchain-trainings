# Project Overview
This project, `langchain-trainings`, is a repository for LangChain training materials, including Jupyter notebooks and Python scripts. It is designed for learning and practicing LangChain 1.0 features, with a focus on local LLM integration using Ollama and evaluation using RAGAS and DeepEval.

## Technologies
- **Main Framework:** LangChain (>=1.0.3)
- **Local LLMs:** Ollama (via `langchain-ollama`)
- **Remote LLMs:** OpenAI (via `langchain-openai`)
- **Vector Database:** ChromaDB (via `langchain-chroma`)
- **Evaluation:** RAGAS (>=0.2.6), DeepEval (>=1.5.3)
- **Environment:** Python (>=3.12 recommended), `python-dotenv` for managing environment variables.
- **Utilities:** `pypdf` for document loading, `pandas` for data processing, `playwright` and `wikipedia` for agent tools.

## Directory Structure
- `section1_basics/`: Contains introductory materials.
  - `langchain_basics.ipynb`: Jupyter notebook for initial LangChain and Ollama exploration.
  - `langchain_basics.py`: Python script counterpart for testing basic LangChain functionality.
- `test_notebook/`: A placeholder or test directory for notebooks.
- `requirements.txt`: Project dependencies.
- `.env`: (User-provided) Should contain necessary API keys (e.g., `LANGSMITH_API_KEY`, `OPENAI_API_KEY`) and project configurations (e.g., `LANGSMITH_PROJECT`).

## Building and Running

### Prerequisites
1.  **Python:** Ensure Python 3.12+ is installed.
2.  **Ollama:** Install [Ollama](https://ollama.com/) and ensure it is running locally (`localhost:11434`).
    - Pull the default model used in examples: `ollama pull llama3.2:latest`.
3.  **Environment Variables:** Create a `.env` file in the root directory (or as specified in scripts) with at least the following:
    ```env
    LANGSMITH_TRACING_V2=true
    LANGSMITH_API_KEY=your_api_key
    LANGSMITH_PROJECT=your_project_name
    OPENAI_API_KEY=your_openai_key # If using OpenAI components
    ```

### Installation
```bash
pip install -r requirements.txt
```

### Running Scripts
- **Python Scripts:** `python section1_basics/langchain_basics.py`
- **Jupyter Notebooks:** Start Jupyter Lab or Notebook and open the `.ipynb` files.
  ```bash
  jupyter lab
  ```

## Development Conventions
- **Environment Variables:** Always use `python-dotenv` to load configurations. Use `load_dotenv('./../.env')` or appropriate paths depending on the script location.
- **Local Development:** Default LLM configuration typically points to local Ollama instances for cost-effective development.
- **Evaluation:** Use `ragas` and `deepeval` for assessing RAG pipelines and LLM outputs as demonstrated in future training sections.
