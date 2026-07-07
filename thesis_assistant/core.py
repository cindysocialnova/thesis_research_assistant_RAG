"""Core thesis research workflow."""
from typing import Tuple
from thesis_assistant.logger import get_logger
from thesis_assistant.validation import validate_thesis, ValidationError
from thesis_assistant.llm_client import LLMClient, ThesisAnalyzer
from thesis_assistant.arxiv_search import fetch_real_arxiv_papers
from thesis_assistant.embeddings import EmbeddingService
from thesis_assistant.config import TOP_PAPERS_COUNT

logger = get_logger(__name__)

class ThesisResearchAssistant:
    """Main orchestrator for thesis research workflow."""
    
    def __init__(self):
        """Initialize the assistant with all dependencies."""
        logger.info("Initializing ThesisResearchAssistant")
        self.llm_client = LLMClient()
        self.analyzer = ThesisAnalyzer(self.llm_client)
        self.embeddings = EmbeddingService()
        logger.info("ThesisResearchAssistant initialized successfully")
    
    def process_thesis(
        self,
        user_thesis: str
    ) -> Tuple[str, str, str, str, str]:
        """Process a thesis and find relevant research.
        
        Args:
            user_thesis: User's thesis statement
            
        Returns:
            Tuple of:
            - strategy (reasoning and search strategy)
            - papers (formatted list of top papers)
            - critique (LLM critique of papers vs thesis)
            - analysis (sentiment and stance)
            - error_msg (empty string if successful, error message otherwise)
        """
        try:
            # Validate input
            validated_thesis = validate_thesis(user_thesis)
            logger.info(f"Processing thesis: {validated_thesis[:60]}...")
            
            # Step 1: Analyze thesis
            logger.info("Step 1: Analyzing thesis")
            sentiment, stance, search_thesis = self.analyzer.analyze_thesis(validated_thesis)
            
            # Step 2: Extract keywords
            logger.info("Step 2: Extracting search keywords")
            reasoning, search_query = self.analyzer.extract_keywords(search_thesis)
            
            # Step 3: Fetch papers from ArXiv
            logger.info(f"Step 3: Searching ArXiv with query: {search_query}")
            papers = fetch_real_arxiv_papers(search_query)
            
            if not papers:
                # Retry with analyzed thesis
                logger.info("No results with extracted keywords, retrying with full thesis")
                papers = fetch_real_arxiv_papers(search_thesis)
                if not papers:
                    error_msg = f"No papers found for: {search_query}"
                    logger.warning(error_msg)
                    return f"Strategy: {reasoning}", error_msg, "Search yielded no results", \
                           f"Sentiment: {sentiment}, Stance: {stance}", error_msg
            
            logger.info(f"Found {len(papers)} papers")
            
            # Step 4: Rank papers by relevance
            logger.info("Step 4: Ranking papers by relevance")
            ranked_papers, scores = self.embeddings.rank_papers(
                papers,
                search_thesis,
                top_k=TOP_PAPERS_COUNT
            )
            
            # Format papers for display
            papers_display = self._format_papers(ranked_papers, scores)
            
            # Step 5: Generate critique
            logger.info("Step 5: Generating critique")
            papers_summary = "\n".join([
                f"- {p.title} (Score: {s:.4f})\n  {p.abstract}\n  {p.url}"
                for p, s in zip(ranked_papers, scores)
            ])
            
            critique = self.analyzer.generate_critique(
                validated_thesis,
                sentiment,
                stance,
                papers_summary
            )
            
            # Format analysis info
            analysis_info = f"Sentiment: {sentiment}, Stance: {stance}"
            strategy_info = f"Strategy: {reasoning}\nSearch Query: {search_query}"
            
            logger.info("Thesis processing completed successfully")
            return strategy_info, papers_display, critique, analysis_info, ""
            
        except ValidationError as e:
            logger.warning(f"Validation error: {e}")
            return str(e), "N/A", "N/A", "N/A", str(e)
        except Exception as e:
            logger.error(f"Unexpected error in process_thesis: {e}", exc_info=True)
            return "Error occurred", "N/A", "N/A", "N/A", str(e)
    
    @staticmethod
    def _format_papers(papers, scores):
        """Format papers for display.
        
        Args:
            papers: List of ArxivPaper objects
            scores: List of similarity scores
            
        Returns:
            Formatted string for display
        """
        if not papers:
            return "No papers found."
        
        formatted = []
        for paper, score in zip(papers, scores):
            formatted.append(
                f"--- {paper.title} (Score: {score:.4f}) ---\n"
                f"Link: {paper.url}\n"
                f"Abstract: {paper.abstract[:200]}...\n"
            )
        return "\n".join(formatted)
