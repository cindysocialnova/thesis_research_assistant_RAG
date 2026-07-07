"""Logging configuration for the thesis assistant."""
import logging
from typing import Optional
from thesis_assistant.config import LOG_LEVEL, LOG_FILE

def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Set log level
        logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
        
        # File handler
        try:
            file_handler = logging.FileHandler(LOG_FILE)
            file_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
        except Exception:
            file_handler = None
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        if file_handler:
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
    return logger
