"""LLM client and prompting utilities."""
import json
import re
from typing import Dict, Optional, Tuple
from groq import Groq
from thesis_assistant.config import GROQ_API_KEY, GROQ_MODEL, GROQ_TEMPERATURE, GROQ_MAX_TOKENS
from thesis_assistant.logger import get_logger

logger = get_logger(__name__)

class LLMClient:
    """Client for interacting with Groq LLM."""
    
    def __init__(self):
        """Initialize Groq client."""
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not configured")
        self.client = Groq(api_key=GROQ_API_KEY)
        logger.info("Groq LLM client initialized")
    
    def call(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        model: Optional[str] = None
    ) -> str:
        """Call the LLM with a prompt.
        
        Args:
            prompt: Input prompt
            temperature: Temperature for generation (uses config default if None)
            max_tokens: Max tokens (uses config default if None)
            model: Model name (uses config default if None)
            
        Returns:
            LLM response text
        """
        if temperature is None:
            temperature = GROQ_TEMPERATURE
        if max_tokens is None:
            max_tokens = GROQ_MAX_TOKENS
        if model is None:
            model = GROQ_MODEL
        
        try:
            logger.debug(f"Calling LLM with model: {model}")
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            response = completion.choices[0].message.content.strip()
            logger.debug(f"LLM response length: {len(response)} chars")
            return response
        except Exception as e:
            logger.error(f"LLM call failed: {e}", exc_info=True)
            raise

class ThesisAnalyzer:
    """Analyzer for thesis statements using LLM."""
    
    def __init__(self, llm_client: LLMClient):
        """Initialize analyzer with LLM client.
        
        Args:
            llm_client: LLMClient instance
        """
        self.llm = llm_client
    
    def analyze_thesis(self, thesis: str) -> Tuple[str, str, str]:
        """Analyze thesis for sentiment and stance.
        
        Args:
            thesis: Thesis statement to analyze
            
        Returns:
            Tuple of (sentiment, stance, search_thesis)
        """
        analysis_prompt = (
            f"Analyze the following thesis statement: '{thesis}'.\n"
            "Respond in JSON format only with these exact keys:\n"
            "{\n"
            '  "sentiment": "Positive" or "Negative" or "Neutral",\n'
            '  "stance": "Support" or "Disprove",\n'
            '  "search_thesis": "<rephrased thesis or original if support>"\n'
            "}\n"
            "Important:\n"
            "- If stance is 'Disprove', rephrase the thesis to express the opposite viewpoint.\n"
            "- If stance is 'Support', repeat the original thesis.\n"
            "- Return ONLY valid JSON, no markdown formatting."
        )
        
        try:
            response = self.llm.call(analysis_prompt)
            result = self._parse_json_response(response)
            
            sentiment = result.get("sentiment", "Neutral")
            stance = result.get("stance", "Support")
            search_thesis = result.get("search_thesis", thesis)
            
            logger.info(f"Analyzed thesis - Sentiment: {sentiment}, Stance: {stance}")
            return sentiment, stance, search_thesis
        except Exception as e:
            logger.warning(f"Failed to analyze thesis: {e}. Using defaults.")
            return "Neutral", "Support", thesis
    
    def extract_keywords(self, text: str) -> Tuple[str, str]:
        """Extract search keywords from text using LLM.
        
        Args:
            text: Text to extract keywords from
            
        Returns:
            Tuple of (reasoning, search_query)
        """
        extraction_prompt = (
            f"Identify the core scientific concepts and paper keywords in: '{text}'.\n"
            "Respond in JSON format only:\n"
            "{\n"
            '  "reasoning": "<brief explanation>",\n'
            '  "search_query": "<technical keywords only, separated by spaces>"\n'
            "}\n"
            "Return ONLY valid JSON, no markdown."
        )
        
        try:
            response = self.llm.call(extraction_prompt)
            result = self._parse_json_response(response)
            
            reasoning = result.get("reasoning", "Keyword extraction performed")
            search_query = result.get("search_query", text)
            
            logger.info(f"Extracted keywords for ArXiv search")
            return reasoning, search_query
        except Exception as e:
            logger.warning(f"Failed to extract keywords: {e}")
            return "Keyword extraction failed", text
    
    def generate_critique(
        self,
        original_thesis: str,
        sentiment: str,
        stance: str,
        papers_summary: str
    ) -> str:
        """Generate a critique of found papers against thesis.
        
        Args:
            original_thesis: Original user thesis
            sentiment: Analyzed sentiment
            stance: Analyzed stance
            papers_summary: Summary of found papers
            
        Returns:
            Critique text
        """
        critique_prompt = (
            f"Original Thesis: {original_thesis}\n"
            f"Sentiment: {sentiment}\n"
            f"Stance: {stance}\n"
            f"Top Papers Found:\n{papers_summary}\n\n"
            f"Critique the alignment of these papers with the ORIGINAL thesis.\n"
            f"Consider the stance: if 'Disprove', evaluate if papers contradict the thesis.\n"
            f"If 'Support', evaluate if papers support the thesis.\n"
            f"Provide a brief assessment of overall alignment (Support/Contradict/Neutral)."
        )
        
        try:
            critique = self.llm.call(critique_prompt, max_tokens=500)
            logger.info("Generated critique")
            return critique
        except Exception as e:
            logger.error(f"Failed to generate critique: {e}")
            return "Critique generation failed."
    
    @staticmethod
    def _parse_json_response(response: str) -> Dict:
        """Parse JSON from LLM response, handling markdown formatting.
        
        Args:
            response: LLM response text
            
        Returns:
            Parsed JSON as dictionary
        """
        try:
            # Remove markdown code fence if present
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned.replace("```json", "", 1)
            if cleaned.startswith("```"):
                cleaned = cleaned.replace("```", "", 1)
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            return json.loads(cleaned.strip())
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response was: {response}")
            return {}
