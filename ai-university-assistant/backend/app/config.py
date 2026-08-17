import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_TITLE = "AI University Assistant"
API_VERSION = "1.0.0"

# Groq Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# RAG Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K_RETRIEVAL = 3

# Vector Store
VECTOR_STORE_PATH = "vectorstore/faiss_index.bin"
METADATA_PATH = "vectorstore/metadata.pkl"

# Documents
DOCUMENTS_DIR = "documents"

# ML Models
CLASSIFIER_MODEL_PATH = "ml_dataset/classifier.pkl"
VECTORIZER_PATH = "ml_dataset/vectorizer.pkl"

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

print(f"✓ Configuration loaded")
print(f"✓ GROQ API Key: {'Set' if GROQ_API_KEY else 'Not Set'}")
