from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "gemini-flash-latest"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

VECTORSTORE_PATH = (
    BASE_DIR / "vectorstore"
)