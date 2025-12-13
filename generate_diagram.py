"""
Generate Architecture Diagram for Deep Research Agent
This creates a visual representation of the agent's workflow
"""

import operator
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END

# --- REPLICATE YOUR ARCHITECTURE ---

class AgentState(TypedDict):
    task: str
    search_results: Annotated[List[str], operator.add]
    attempts: int
    error: str = None
    final_report: str = None

# Dummy nodes just for visualization structure
def search_node(state): 
    return {}

def writer_node(state): 
    return {}

# Your exact router logic
def should_continue_search(state: AgentState):
    """Router that decides whether to continue searching or write report"""
    if state['attempts'] < 3:  # Match your actual config
        return "search"
    else:
        return "writer"

# Build the exact same graph structure as your agent
workflow = StateGraph(AgentState)
workflow.add_node("search", search_node)
workflow.add_node("writer", writer_node)
workflow.set_entry_point("search")
workflow.add_conditional_edges(
    "search",
    should_continue_search,
    {"search": "search", "writer": "writer"}
)
workflow.add_edge("writer", END)

# Compile the graph
app = workflow.compile()

# --- GENERATE THE DIAGRAM ---
print("🎨 Generating architecture diagram...")
print("="*60)

try:
    # Generate PNG from the graph structure
    png_bytes = app.get_graph().draw_mermaid_png()
    
    # Save it to a file
    filename = "agent_architecture.png"
    with open(filename, "wb") as f:
        f.write(png_bytes)
    
    print(f"✅ Successfully saved diagram to: {filename}")
    print("📂 Location: " + __file__.replace("generate_diagram.py", filename))
    print("\n💡 Use this diagram in:")
    print("   - Your blog post header")
    print("   - README.md")
    print("   - LinkedIn/Twitter posts")
    print("   - Interview presentations")
    print("="*60)

except Exception as e:
    print("❌ Could not generate diagram.")
    print(f"Error detail: {e}")
    print("\n🔧 Troubleshooting:")
    print("   1. Make sure you installed grandalf: pip install grandalf")
    print("   2. Check if you have the latest langgraph version")
    print("="*60)
