"""Thesis Research Assistant - RAG-based research paper discovery."""

__version__ = "2.0.0"
__author__ = "Cindy Social Nova"

from thesis_assistant.core import ThesisResearchAssistant
from thesis_assistant.config import validate_config
from thesis_assistant.logger import get_logger

__all__ = [
    "ThesisResearchAssistant",
    "validate_config",
    "get_logger",
]
