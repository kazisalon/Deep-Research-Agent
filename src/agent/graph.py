"""LangGraph workflow definition."""

from langgraph.graph import StateGraph, END
from src.utils.logger import get_logger
from src.utils.cost_tracker import CostTracker
from .state import AgentState
from .nodes import SearchNode, WriterNode
from .routers import should_continue_search

logger = get_logger()


def create_research_agent(cost_tracker: CostTracker):
    """
    Create and compile the research agent workflow.
    
    Architecture:
    1. Entry point: search node
    2. Conditional routing: Continue searching or write report
    3. Writer node generates final report
    4. End
    
    Args:
        cost_tracker: Cost tracking instance
        
    Returns:
        Compiled LangGraph application
    """
    logger.info("🔧 Building research agent workflow...")
    
    # Initialize nodes
    search_node = SearchNode(cost_tracker)
    writer_node = WriterNode(cost_tracker)
    
    # Create workflow graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("search", search_node)
    workflow.add_node("writer", writer_node)
    
    # Set entry point
    workflow.set_entry_point("search")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "search",
        should_continue_search,
        {
            "search": "search",  # Loop back for more searches
            "writer": "writer"   # Move to report generation
        }
    )
    
    # Add terminal edge
    workflow.add_edge("writer", END)
    
    # Compile the graph
    app = workflow.compile()
    
    logger.info("✅ Research agent workflow compiled successfully")
    
    return app
