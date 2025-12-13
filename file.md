"Your code uses temperature=0. Why? When would you use higher temperature?"

#model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# Answer:
# temperature=0 → Deterministic, factual, no creativity
# Good for: Research reports, data summarization
# 
# temperature=0.7-1.0 → Creative, varied outputs
# Good for: Marketing copy, creative writing
#
# For research, we want facts, not creativity


"How would you deploy this in production?"

# Expected answer:
# 1. Environment variables for API keys
# 2. API endpoint (FastAPI/Flask)
# 3. Rate limiting
# 4. Caching layer (Redis)
# 5. Error handling and logging
# 6. Monitoring (track costs, latency)
# 7. Async for better performance

# Example:
from fastapi import FastAPI
app_server = FastAPI()

@app_server.post("/research")
async def research(query: str):
    result = app.invoke({"task": query, "search_results": [], "attempts": 0})
    return {"report": result}


<!-- "How would you add memory so the agent remembers past conversations?"

class AgentState(TypedDict):
    task: str
    search_results: Annotated[List[str], operator.add]
    attempts: int
    chat_history: Annotated[List[dict], operator.add]  # Add this

def writer_node(state: AgentState):
    # Include chat history in prompt
    history = "\n".join([f"{m['role']}: {m['content']}" for m in state['chat_history']])
    
    prompt = f"""
    Previous conversation:
    {history}
    
    Current task: {state['task']}
    ... -->
    """


    <!-- "What are the limitations of your current implementation?" -->

# Be honest - shows self-awareness:
# 1. No error handling
# 2. API keys hardcoded (should use .env)
# 3. Router is too simple (just counts)
# 4. No caching (repeated searches waste API calls)
# 5. No conversation memory (one-shot only)
# 6. Max 3 results limit might not be enough
# 7. No cost tracking (Tavily and Gemini have limits)


"If you needed to research multiple topics in parallel, how would you redesign this?"

# Answer: Show understanding of parallel execution

# Option 1: Multiple search nodes running concurrently
workflow.add_node("search_stocks", search_stocks_node)
workflow.add_node("search_news", search_news_node)

# Run both from entry point
workflow.set_entry_point("parallel_start")
workflow.add_edge("parallel_start", "search_stocks")
workflow.add_edge("parallel_start", "search_news")

# Option 2: Use asyncio
async def parallel_search(queries):
    tasks = [tavily_tool.ainvoke(q) for q in queries]
    return await asyncio.gather(*tasks)


#4

"How does state merging work in LangGraph?"
# Initial state
state = {"task": "query", "search_results": [], "attempts": 0}

# Node returns partial update
return {"attempts": 1, "search_results": ["new"]}

# LangGraph merges (shallow merge)
# Final state: {"task": "query", "search_results": ["new"], "attempts": 1}



# add_edge - Always goes to the same next node
workflow.add_edge("writer", END)  # Always END after writer

# add_conditional_edges - Calls a function to decide
workflow.add_conditional_edges(
    "search", 
    router,  # This function decides where to go
    {"search": "search", "writer": "writer"}
)