"""Input validation utilities."""
from thesis_assistant.config import THESIS_MIN_LENGTH, THESIS_MAX_LENGTH, THESIS_MAX_NEWLINES
from thesis_assistant.logger import get_logger

logger = get_logger(__name__)

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

def validate_thesis(thesis_text: str) -> str:
    """Validate and sanitize thesis input.
    
    Args:
        thesis_text: The thesis text to validate
        
    Returns:
        Cleaned thesis text
        
    Raises:
        ValidationError: If thesis fails validation
    """
    thesis = thesis_text.strip()
    
    # Check minimum length
    if len(thesis) < THESIS_MIN_LENGTH:
        msg = f"Thesis too short (minimum {THESIS_MIN_LENGTH} characters)"
        logger.warning(msg)
        raise ValidationError(msg)
    
    # Check maximum length
    if len(thesis) > THESIS_MAX_LENGTH:
        msg = f"Thesis too long (maximum {THESIS_MAX_LENGTH} characters)"
        logger.warning(msg)
        raise ValidationError(msg)
    
    # Check for excessive newlines (potential injection attack)
    if thesis.count('\n') > THESIS_MAX_NEWLINES:
        msg = f"Too many line breaks (maximum {THESIS_MAX_NEWLINES})"
        logger.warning(msg)
        raise ValidationError(msg)
    
    logger.info(f"Validated thesis: {thesis[:50]}...")
    return thesis
