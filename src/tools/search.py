"""Web search tool integration."""

import os
from typing import List, Dict, Any
from config.settings import settings
from src.utils.logger import get_logger

logger = get_logger()


class SearchTool:
    """Wrapper for Tavily search with error handling and retry logic."""
    
    def __init__(self):
        """Initialize Tavily search tool."""
        # Set environment variable for Tavily
        os.environ["TAVILY_API_KEY"] = settings.tavily_api_key
        
        # Try new package first, fall back to old one
        try:
            from langchain_tavily import TavilySearchResults
            logger.debug("Using langchain-tavily package")
        except ImportError:
            from langchain_community.tools.tavily_search import TavilySearchResults
            logger.debug("Using langchain-community tavily (deprecated)")
        
        self.tavily = TavilySearchResults(
            max_results=settings.max_search_results
        )
    
    def search(self, query: str, max_retries: int = 3) -> List[Dict[str, Any]]:
        """
        Execute a web search with retry logic.
        
        Args:
            query: Search query string
            max_retries: Maximum number of retry attempts
            
        Returns:
            List of search results
            
        Raises:
            Exception: If all retries fail
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                logger.debug(f"Search attempt {attempt + 1}/{max_retries}")
                results = self.tavily.invoke(query)
                
                if not results:
                    logger.warning("Search returned empty results")
                    return []
                
                return results
                
            except Exception as e:
                last_error = e
                logger.warning(f"Search attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < max_retries - 1:
                    import time
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)
        
        # All retries failed
        error_msg = f"Search failed after {max_retries} attempts: {str(last_error)}"
        logger.error(error_msg)
        raise Exception(error_msg)
