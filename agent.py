import os
import operator
from typing import TypedDict, Annotated, List

# 1. IMPORTS
# LangGraph is the "Orchestrator" that manages the loops.
from langgraph.graph import StateGraph, END
# We use Gemini because it is free and powerful.
from langchain_google_genai import ChatGoogleGenerativeAI
# Tavily is our search engine tool.
from langchain_community.tools.tavily_search import TavilySearchResults
# SystemMessage is how we give the AI "Developer Instructions".
from langchain_core.messages import SystemMessage

# --- CONFIGURATION ---
# Replace these with your actual keys or use a .env file
os.environ["TAVILY_API_KEY"] = "tvly-YOUR_KEY_HERE"
os.environ["GOOGLE_API_KEY"] = "AIza-YOUR_KEY_HERE"

# --- THE SETUP ---

# 2. THE TOOLS
# We configure Tavily to bring back the top 3 search results.
tavily_tool = TavilySearchResults(max_results=3)

# 3. THE BRAIN (LLM)
# We use Gemini 1.5 Flash. It is fast and free.
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# 4. THE MEMORY (State)
# This class acts like a shared notebook. 
# Every "Node" (worker) can read from it and write to it.
class AgentState(TypedDict):
    task: str                                   # The user's original question
    search_results: Annotated[List[str], operator.add]  # List to store search data
    attempts: int                               # Counter to prevent infinite loops

# --- THE WORKERS (Nodes) ---

def search_node(state: AgentState):
    """
    WORKER 1: The Researcher.
    Its job is to take the task and find information online.
    """
    print(f"🔎 Searching for: {state['task']}...")
    
    # 1. Execute the search using Tavily
    results = tavily_tool.invoke(state['task'])
    
    # 2. Extract just the text content from the results
    # (Tavily returns a lot of metadata we don't need right now)
    content = [res['content'] for res in results]
    
    # 3. Update the shared memory (State)
    return {
        "search_results": content, 
        "attempts": state['attempts'] + 1
    }

def writer_node(state: AgentState):
    """
    WORKER 2: The Analyst.
    Its job is to read the search results and write the report.
    """
    print("✍️ Writing report...")
    
    # 1. Combine all search results into one big text block
    context = "\n\n".join(state['search_results'])
    
    # 2. Create the prompt for the AI
    prompt = f"""
    You are a Senior Research Analyst. 
    Write a concise summary report based ONLY on the context provided below.
    
    User Query: {state['task']}
    
    Context from the web:
    {context}
    
    Instructions:
    - Focus on facts and numbers.
    - Cite your sources (e.g., [Source 1]).
    """
    
    # 3. Ask Gemini to generate the text
    messages = [SystemMessage(content=prompt)]
    response = model.invoke(messages)
    
    # 4. Print the final result
    print("\n--- FINAL REPORT ---\n")
    print(response.content)
    return {}

# --- THE MANAGER (Router) ---

def router(state: AgentState):
    """
    THE BOSS: Decides what to do next.
    Logic: If we have searched less than 2 times, search again (simulate deep research).
    Otherwise, write the report.
    """
    if state['attempts'] < 1: # For this demo, we stop after 1 search to be fast
        return "search"
    else:
        return "writer"

# --- BUILDING THE GRAPH ---

# 1. Initialize the Graph with our State
workflow = StateGraph(AgentState)

# 2. Add the nodes (The workers)
workflow.add_node("search", search_node)
workflow.add_node("writer", writer_node)

# 3. Set the entry point (Where do we start?)
workflow.set_entry_point("search")

# 4. Define the flow
# After 'search', ask the router where to go next.
workflow.add_conditional_edges(
    "search",       # From this node...
    router,         # Call this logic function...
    {               # Map the output to the next node
        "search": "search",
        "writer": "writer"
    }
)

# After 'writer', we end the program.
workflow.add_edge("writer", END)

# 5. Turn it on!
app = workflow.compile()

# --- EXECUTION ---

if __name__ == "__main__":
    # This block only runs if you execute the file directly
    
    user_query = "What is the current stock price of NVIDIA and why is it moving today?"
    
    # Initialize the memory
    initial_state = {
        "task": user_query, 
        "search_results": [], 
        "attempts": 0
    }
    
    print("🚀 Starting Agent...")
    
    # Run the graph
    # app.invoke runs the whole flow from start to finish
    app.invoke(initial_state)