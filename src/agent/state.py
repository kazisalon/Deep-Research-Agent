"""Agent state definition."""

import operator
from typing import TypedDict, Annotated, List, Optional


class AgentState(TypedDict):
    """
    Shared state for the research agent.
    
    This state is passed between all nodes in the workflow.
    The Annotated types with operator.add will accumulate values
    instead of replacing them.
    """
    
    # User's research query
    task: str
    
    # Accumulated search results from all searches
    search_results: Annotated[List[str], operator.add]
    
    # Number of search attempts made
    attempts: int
    
    # Optional: Track errors
    error: Optional[str]
    
    # Optional: Final report content
    final_report: Optional[str]
