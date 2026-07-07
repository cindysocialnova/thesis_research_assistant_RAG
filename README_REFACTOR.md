# Thesis Research Assistant - Refactored

## Overview

A modular, production-ready research assistant that analyzes thesis statements and finds relevant papers from arXiv using semantic search and LLM-powered insights.

## Key Improvements Over Original

### 1. **Modular Architecture**
The monolithic notebook has been split into focused modules:
- `config.py` - Centralized configuration with environment variables
- `logger.py` - Structured logging throughout
- `validation.py` - Input validation and error handling
- `arxiv_search.py` - ArXiv API wrapper with `ArxivPaper` class
- `embeddings.py` - `EmbeddingService` for semantic ranking
- `llm_client.py` - `LLMClient` and `ThesisAnalyzer` with robust parsing
- `core.py` - `ThesisResearchAssistant` orchestrator

### 2. **Robust Error Handling**
- Specific exception types (e.g., `ValidationError`)
- Graceful degradation with fallback strategies
- Comprehensive logging at every step
- API timeout and HTTP error handling
- JSON parsing with markdown fallback

### 3. **Configuration Management**
```bash
# Set environment variables
export GROQ_API_KEY=your_key
export GROQ_MODEL=llama-3.1-8b-instant
export EMBEDDING_MODEL=BAAI/bge-large-en-v1.5
export THESIS_MIN_LENGTH=5
export LOG_LEVEL=INFO
```

Or use `.env` file:
```
GROQ_API_KEY=your_key
THESIS_MAX_LENGTH=2000
```

### 4. **Improved LLM Integration**
- Structured JSON output with validation
- Markdown formatting fallback
- Configurable temperature and token limits
- Better error messages and logging

### 5. **Better Input Validation**
```python
from thesis_assistant.validation import validate_thesis, ValidationError

try:
    validated = validate_thesis(user_input)
except ValidationError as e:
    print(f"Invalid: {e}")
```

### 6. **Type Hints & Documentation**
- Full type hints throughout codebase
- Comprehensive docstrings
- Clear function responsibilities

## Usage

### Basic Usage
```python
from thesis_assistant import ThesisResearchAssistant

assistant = ThesisResearchAssistant()
strategy, papers, critique, analysis, error = assistant.process_thesis(
    "Machine learning improves medical diagnosis"
)

if not error:
    print(f"Papers:\n{papers}")
    print(f"Critique:\n{critique}")
```

### Using Individual Components
```python
from thesis_assistant.arxiv_search import fetch_real_arxiv_papers
from thesis_assistant.embeddings import EmbeddingService

papers = fetch_real_arxiv_papers("neural networks")
embeddings = EmbeddingService()
ranked, scores = embeddings.rank_papers(papers, "query")
```

### Gradio Interface
Run the refactored notebook `thesis_assistant_refactored.ipynb` for an interactive web UI.

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | Required | Groq API key |
| `GROQ_MODEL` | `llama-3.1-8b-instant` | Model to use |
| `GROQ_TEMPERATURE` | `0.3` | Generation temperature |
| `GROQ_MAX_TOKENS` | `1024` | Max tokens per response |
| `EMBEDDING_MODEL` | `BAAI/bge-large-en-v1.5` | HuggingFace embedding model |
| `ARXIV_MAX_RESULTS` | `6` | Papers to fetch |
| `ARXIV_TIMEOUT` | `30` | API timeout in seconds |
| `THESIS_MIN_LENGTH` | `5` | Minimum thesis characters |
| `THESIS_MAX_LENGTH` | `2000` | Maximum thesis characters |
| `TOP_PAPERS_COUNT` | `5` | Top papers to display |
| `LOG_LEVEL` | `INFO` | Logging level |

## Error Handling Examples

### Invalid Input
```python
from thesis_assistant.validation import ValidationError

try:
    assistant.process_thesis("short")
except ValidationError as e:
    print(f"Error: {e}")
# Output: Error: Thesis too short (minimum 5 characters)
```

### No Papers Found
```python
strategy, papers, critique, analysis, error = assistant.process_thesis(
    "Very obscure research topic xyz123"
)
if error:
    print(f"Error: {error}")
```

### API Failures
The system automatically falls back:
1. First tries with LLM-extracted keywords
2. Falls back to full thesis as search query
3. Returns helpful error if no results found

## Logging

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
```

Logs appear in:
- Console (stdout)
- File: `thesis_assistant.log`

Example log output:
```
2024-01-15 10:30:45 - thesis_assistant.core - INFO - Initializing ThesisResearchAssistant
2024-01-15 10:30:47 - thesis_assistant.llm_client - INFO - Groq LLM client initialized
2024-01-15 10:30:48 - thesis_assistant.embeddings - INFO - Loading embedding model: BAAI/bge-large-en-v1.5
```

## Migration from Original Notebook

Key changes:
1. Replace monolithic cell with modular imports
2. Update configuration via environment variables
3. Use `ThesisResearchAssistant` class instead of functions
4. Handle `ValidationError` for input validation
5. Access logs via `get_logger()`

## Requirements

```
groq>=0.4.0
langchain-community>=0.1.0
langchain-core>=0.1.0
python-dotenv>=0.21.0
gradio>=3.0.0
numpy>=1.20.0
requests>=2.28.0
pydantic>=2.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

## Testing

Test individual components:
```python
from thesis_assistant.arxiv_search import ArxivPaper, clean_query_for_api

# Test query cleaning
cleaned = clean_query_for_api("I will search for machine learning")
assert cleaned == "machine learning"

# Test paper object
paper = ArxivPaper(
    "Title",
    "Abstract",
    "http://arxiv.org/abs/2301.00001"
)
assert paper.title == "Title"
```

## Future Enhancements

- [ ] Redis caching layer
- [ ] Batch processing
- [ ] Multi-language support
- [ ] PDF extraction
- [ ] Citation network analysis
- [ ] Custom embedding fine-tuning
- [ ] Async API calls
- [ ] Unit test suite

## License

MIT
