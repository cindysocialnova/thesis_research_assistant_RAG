"""Embedding and semantic search functionality."""
import numpy as np
from typing import List, Tuple
from langchain_community.embeddings import HuggingFaceEmbeddings
from thesis_assistant.config import EMBEDDING_MODEL, TOP_PAPERS_COUNT
from thesis_assistant.logger import get_logger
from thesis_assistant.arxiv_search import ArxivPaper

logger = get_logger(__name__)

class EmbeddingService:
    """Service for managing embeddings and similarity searches."""
    
    def __init__(self):
        """Initialize the embedding model."""
        try:
            logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
            self.model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}", exc_info=True)
            raise
    
    def embed_text(self, text: str) -> np.ndarray:
        """Embed a single text string.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        try:
            return np.array(self.model.embed_query(text))
        except Exception as e:
            logger.error(f"Failed to embed text: {e}", exc_info=True)
            raise
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Embed multiple text strings.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            Array of embedding vectors
        """
        try:
            return np.array(self.model.embed_documents(texts))
        except Exception as e:
            logger.error(f"Failed to embed texts: {e}", exc_info=True)
            raise
    
    def rank_papers(
        self,
        papers: List[ArxivPaper],
        query: str,
        top_k: int = TOP_PAPERS_COUNT
    ) -> Tuple[List[ArxivPaper], List[float]]:
        """Rank papers by semantic similarity to query.
        
        Args:
            papers: List of papers to rank
            query: Query text
            top_k: Number of top papers to return
            
        Returns:
            Tuple of (ranked_papers, scores)
        """
        if not papers:
            logger.warning("No papers to rank")
            return [], []
        
        try:
            logger.info(f"Computing embeddings for {len(papers)} papers")
            paper_strings = [p.to_string() for p in papers]
            paper_embeddings = self.embed_texts(paper_strings)
            query_embedding = self.embed_text(query)
            
            # Cosine similarity
            logger.debug("Computing cosine similarity scores")
            scores = np.dot(paper_embeddings, query_embedding) / (
                np.linalg.norm(paper_embeddings, axis=1) * np.linalg.norm(query_embedding)
            )
            
            # Get top-k indices
            indices = np.argsort(scores)[::-1][:top_k]
            ranked_papers = [papers[i] for i in indices]
            ranked_scores = [float(scores[i]) for i in indices]
            
            logger.info(f"Ranked {len(ranked_papers)} papers")
            return ranked_papers, ranked_scores
            
        except Exception as e:
            logger.error(f"Failed to rank papers: {e}", exc_info=True)
            return [], []
