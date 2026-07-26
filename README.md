## Pré-requisitos

- Python 3.12
- uv
- Ollama

## Instalação

uv sync

## Executar comandos
uv run streamlit run app.py


## PROMPTS ARQUITECTUR3

                    User Question
                           |
                           v
                    Retriever
                           |
                           v
                Context Evaluation
                           |
        +------------------+------------------+
        |                  |                  |
      FOUND             PARTIAL             EMPTY
        |                  |                  |
        v                  v                  v
 RAG_PROMPT     INSUFFICIENT_CONTEXT   NO_CONTEXT