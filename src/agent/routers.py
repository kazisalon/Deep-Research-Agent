"""Router functions for controlling agent workflow."""

from typing import Literal
from config.settings import settings
from src.utils.logger import get_logger
from .state import AgentState

logger = get_logger()


def should_continue_search(state: AgentState) -> Literal["search", "writer"]:
    """
    Decide whether to continue searching or write the report.
    
    This is a simple counter-based router. In production, you could:
    - Use LLM to evaluate data quality
    - Check for specific information completeness
    - Implement multi-factor decision logic
    
    Args:
        state: Current agent state
        
    Returns:
        "search" to continue searching, "writer" to generate report
    """
    attempts = state['attempts']
    max_attempts = settings.max_search_attempts
    
    # Check if we have errors
    if state.get('error') and attempts >= max_attempts:
        logger.warning(f"Max attempts ({max_attempts}) reached with errors. Moving to writer.")
        return "writer"
    
    # Continue searching if under limit
    if attempts < max_attempts:
        logger.info(f"Search attempts: {attempts}/{max_attempts}. Continuing search...")
        return "search"
    
    # Reached limit, time to write
    logger.info(f"Search attempts: {attempts}/{max_attempts}. Moving to report generation.")
    return "writer"


def smart_router(state: AgentState) -> Literal["search", "writer"]:
    """
    Advanced router that could use LLM to evaluate quality.
    
    This is a placeholder for more sophisticated routing logic.
    You could implement:
    - Quality scoring of search results
    - Gap analysis (what information is missing)
    - Confidence scoring
    """
    # For now, delegate to simple router
    # TODO: Implement LLM-based quality evaluation
    return should_continue_search(state)
