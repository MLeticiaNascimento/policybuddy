from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]


DOCUMENTS_PATH = BASE_DIR / "docs" / "policies"


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


CHROMA_PATH = BASE_DIR / "data" / "chroma"