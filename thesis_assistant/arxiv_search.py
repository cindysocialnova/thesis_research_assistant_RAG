"""ArXiv paper search functionality."""
import xml.etree.ElementTree as ET
import re
from typing import List, Dict, Optional
import requests
from thesis_assistant.config import ARXIV_BASE_URL, ARXIV_MAX_RESULTS, ARXIV_TIMEOUT
from thesis_assistant.logger import get_logger

logger = get_logger(__name__)

class ArxivPaper:
    """Represents a paper from ArXiv."""
    def __init__(self, title: str, abstract: str, url: str):
        self.title = title
        self.abstract = abstract
        self.url = url
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "abstract": self.abstract,
            "url": self.url
        }
    
    def to_string(self) -> str:
        """Convert to display string."""
        return f"{self.title}: {self.abstract}"

def clean_query_for_api(query_text: str) -> str:
    """Clean query by removing conversational filler and invalid characters.
    
    Args:
        query_text: Raw query text from LLM
        
    Returns:
        Cleaned query suitable for API
    """
    # Remove common conversational intros
    filler_phrases = [
        "I will search for",
        "Here is a query:",
        "Searching for",
        "However, I don't see",
        "I cannot find",
        "Reasoning:",
        "Search Query:"
    ]
    
    temp_q = query_text
    for phrase in filler_phrases:
        temp_q = re.sub(phrase, "", temp_q, flags=re.IGNORECASE)
    
    # Remove invalid characters but keep hyphens and underscores
    temp_q = re.sub(r'[^\w\s\-_]', '', temp_q)
    
    cleaned = temp_q.strip()
    logger.debug(f"Cleaned query: '{query_text}' -> '{cleaned}'")
    return cleaned

def fetch_real_arxiv_papers(search_query: str, max_results: Optional[int] = None) -> List[ArxivPaper]:
    """Fetch papers from ArXiv API.
    
    Args:
        search_query: Search query string
        max_results: Maximum results to return (uses config default if None)
        
    Returns:
        List of ArxivPaper objects
    """
    if max_results is None:
        max_results = ARXIV_MAX_RESULTS
    
    clean_q = clean_query_for_api(search_query)
    
    if not clean_q:
        logger.warning("Query is empty after cleaning")
        return []
    
    params = {
        "search_query": f"all:{clean_q}",
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    try:
        logger.info(f"Fetching papers from ArXiv with query: {clean_q}")
        response = requests.get(ARXIV_BASE_URL, params=params, timeout=ARXIV_TIMEOUT)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        papers = []
        for entry in root.findall('atom:entry', ns):
            try:
                title_elem = entry.find('atom:title', ns)
                abstract_elem = entry.find('atom:summary', ns)
                url_elem = entry.find('atom:id', ns)
                
                if all([title_elem is not None, abstract_elem is not None, url_elem is not None]):
                    paper = ArxivPaper(
                        title=title_elem.text.strip().replace('\n', ' '),
                        abstract=abstract_elem.text.strip().replace('\n', ' '),
                        url=url_elem.text.strip()
                    )
                    papers.append(paper)
            except Exception as e:
                logger.warning(f"Failed to parse paper entry: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(papers)} papers from ArXiv")
        return papers
        
    except requests.exceptions.Timeout:
        logger.error("ArXiv API timeout. Try a simpler query.")
        return []
    except requests.exceptions.HTTPError as e:
        logger.error(f"ArXiv API HTTP error: {e.response.status_code}")
        return []
    except ET.ParseError as e:
        logger.error(f"XML parsing error: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching papers: {e}", exc_info=True)
        return []
