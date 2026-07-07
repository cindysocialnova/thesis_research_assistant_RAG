"""Configuration management for the thesis assistant."""
import os
from typing import Optional

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# API Configuration
GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.3"))
GROQ_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "1024"))

# Embedding Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-large-en-v1.5")

# ArXiv Configuration
ARXIV_BASE_URL = "http://export.arxiv.org/api/query"
ARXIV_MAX_RESULTS = int(os.getenv("ARXIV_MAX_RESULTS", "6"))
ARXIV_TIMEOUT = int(os.getenv("ARXIV_TIMEOUT", "30"))

# Input Validation
THESIS_MIN_LENGTH = int(os.getenv("THESIS_MIN_LENGTH", "5"))
THESIS_MAX_LENGTH = int(os.getenv("THESIS_MAX_LENGTH", "2000"))
THESIS_MAX_NEWLINES = int(os.getenv("THESIS_MAX_NEWLINES", "10"))

# Search Configuration
TOP_PAPERS_COUNT = int(os.getenv("TOP_PAPERS_COUNT", "5"))

# Cache Configuration (TTL in minutes)
CACHE_TTL_MINUTES = int(os.getenv("CACHE_TTL_MINUTES", "60"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "thesis_assistant.log")

def validate_config():
    """Validate critical configuration values."""
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY environment variable not set. "
            "Please set it before running the assistant."
        )
    return True
