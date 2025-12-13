# Deep Research Agent - Interview Preparation Guide

## Table of Contents
1. [How Agents Make Decisions](#how-agents-make-decisions)
2. [Expected Interview Questions](#expected-interview-questions)
3. [Technical Deep Dives](#technical-deep-dives)
4. [Production Considerations](#production-considerations)

---

# How Agents Make Decisions

## The Decision-Making Framework

### 1. **ReAct Pattern (Reason + Act)**

Your agent follows the **ReAct** paradigm - it alternates between reasoning and acting:

```
User Query → REASON (should I search?) → ACT (search web) → REASON (enough data?) → ACT (write report)
```

**In your code:**
```python
def router(state: AgentState):
    # REASONING STEP
    if state['attempts'] < 1:
        return "search"  # DECISION: Need more data
    else:
        return "writer"  # DECISION: Have enough data
```

### 2. **Three Levels of Decision Making**

#### Level 1: **Static Logic (Your Current Implementation)**
```python
# Decision based on simple rules
if attempts < 1:
    return "search"
else:
    return "writer"
```

**Pros:** Fast, predictable, cheap  
**Cons:** Not intelligent, rigid

---

#### Level 2: **LLM-Based Decisions (Agentic Reasoning)**
```python
def smart_router(state: AgentState):
    # Ask the LLM to DECIDE what to do next
    decision_prompt = f"""
    You are a research coordinator.
    
    Task: {state['task']}
    Current data: {state['search_results']}
    Attempts so far: {state['attempts']}
    
    Should we:
    A) Search for more information
    B) Write the report now
    
    Answer only A or B with reasoning.
    """
    
    response = model.invoke(decision_prompt)
    
    if "A" in response.content:
        return "search"
    else:
        return "writer"
```

**Pros:** Intelligent, adapts to context  
**Cons:** Slower, costs API calls, can be unpredictable

---

#### Level 3: **Multi-Agent Consensus (Advanced)**
```python
def consensus_router(state: AgentState):
    # Multiple AI "experts" vote on the decision
    
    experts = [
        "You are a data quality expert. Is the data sufficient?",
        "You are a research strategist. Should we search more?",
        "You are a cost optimizer. Is more searching worth it?"
    ]
    
    votes = []
    for expert_role in experts:
        prompt = f"{expert_role}\n\nData: {state['search_results']}\nVote: SEARCH or WRITE"
        vote = model.invoke(prompt)
        votes.append(vote.content)
    
    # Majority wins
    if votes.count("SEARCH") > votes.count("WRITE"):
        return "search"
    else:
        return "writer"
```

**Pros:** More robust, diverse perspectives  
**Cons:** Expensive, slow, complex

---

## Agent Decision-Making Patterns

### Pattern 1: **Chain-of-Thought (CoT) Decisions**

The agent "thinks out loud" before deciding:

```python
def cot_router(state: AgentState):
    prompt = f"""
    Let me think step by step:
    
    1. User asked: {state['task']}
    2. We have searched {state['attempts']} times
    3. We have {len(state['search_results'])} search results
    4. The results contain: {state['search_results'][0][:100]}...
    
    Reasoning:
    - If results directly answer the question → WRITE
    - If results are vague or off-topic → SEARCH
    - If we've searched 3+ times → WRITE (to avoid infinite loops)
    
    My decision: [SEARCH or WRITE]
    Explanation: [why]
    """
    
    response = model.invoke(prompt)
    
    if "SEARCH" in response.content:
        return "search"
    else:
        return "writer"
```

**Why this matters:** Transparent, debuggable, shows reasoning

---

### Pattern 2: **Tool Selection Decisions**

When agents have MULTIPLE tools, they must decide which to use:

```python
# Imagine your agent has 3 tools:
tools = {
    "web_search": tavily_tool,
    "database_query": db_tool,
    "calculator": calc_tool
}

def tool_selector(state: AgentState):
    prompt = f"""
    Task: {state['task']}
    
    Available tools:
    1. web_search - Search the internet
    2. database_query - Query internal database
    3. calculator - Perform calculations
    
    Which tool should I use? Answer with the tool name.
    """
    
    decision = model.invoke(prompt)
    
    if "web_search" in decision.content:
        return "web_search_node"
    elif "database" in decision.content:
        return "database_node"
    elif "calculator" in decision.content:
        return "calc_node"
```

---

### Pattern 3: **Self-Reflection / Self-Critique**

The agent evaluates its own work:

```python
def writer_with_reflection(state: AgentState):
    # First, write the report
    draft = write_report(state)
    
    # Then, critique it
    critique_prompt = f"""
    You are a quality checker.
    
    Report draft: {draft}
    Original task: {state['task']}
    
    Does this report fully answer the task?
    - YES: It's complete
    - NO: Missing [specific info]
    """
    
    critique = model.invoke(critique_prompt)
    
    if "NO" in critique.content:
        # Extract what's missing
        missing_info = extract_missing(critique.content)
        # Trigger another search
        return {"next_action": "search", "refined_query": missing_info}
    else:
        # Report is good, end
        return {"next_action": "end", "final_report": draft}
```

**Real-world example:**
- Agent writes: "NVIDIA stock is up 3%"
- Critique: "Missing: WHY is it up?"
- Agent: Searches again for "NVIDIA stock increase reason"
- Rewrites with complete info

---

## Visual Decision Flow

### Your Current Agent:
```
┌─────────────────┐
│  User Query     │
└────────┬────────┘
         ↓
    ┌────────────┐
    │  Search    │ ← Hardcoded: Always search first
    └────┬───────┘
         ↓
    ┌────────────┐
    │  Router    │ ← Simple logic: attempts < 1?
    └────┬───────┘
         │
    ┌────┴────┐
    │         │
    ↓         ↓
 [Loop]    [Write Report]
```

### Advanced Agent with LLM Decisions:
```
┌─────────────────┐
│  User Query     │
└────────┬────────┘
         ↓
    ┌────────────────┐
    │ Query Analyzer │ ← LLM decides: What type of question is this?
    └────────┬───────┘
             │
       ┌─────┴─────┐
       │           │
       ↓           ↓
 [Factual]    [Opinion]
       │           │
       ↓           ↓
 [Search Web] [Generate]
       │
       ↓
    ┌──────────────┐
    │ Quality Check│ ← LLM decides: Is data good enough?
    └──────┬───────┘
           │
      ┌────┴────┐
      │         │
      ↓         ↓
   [Yes]      [No → Search Again]
      │
      ↓
 [Write Report]
      ↓
    ┌──────────────┐
    │ Self-Critique│ ← LLM decides: Is report complete?
    └──────┬───────┘
           │
      ┌────┴────┐
      │         │
      ↓         ↓
   [Good]    [Missing info → Refine search]
      │
      ↓
    [END]
```

---

## Key Insight: Declarative vs Imperative Decisions

### Imperative (Traditional Code):
```python
# YOU tell the agent exactly what to do
if attempts < 1:
    search()
else:
    write()
```

### Declarative (Agentic):
```python
# YOU give the agent goals, IT decides how
prompt = """
Goal: Answer the user's question comprehensively.
Resources: Web search, database, calculator
Constraint: Minimize API costs

Decide your next action.
"""

decision = model.invoke(prompt)
# Agent might decide: "I'll search once, then check quality, then write"
```

---

# Expected Interview Questions

## Section 1: Conceptual Understanding

### Q1: "Explain what an AI agent is and how it differs from a regular LLM."

**Answer:**
- **LLM:** Takes input → Generates output (one-shot, no actions)
- **Agent:** Can take ACTIONS, use TOOLS, make DECISIONS, and operate in a LOOP

**Example from your code:**
```python
# LLM alone:
response = model.invoke("What is NVIDIA's stock price today?")
# Output: "I don't have real-time data"

# Agent:
# 1. Decides to search web (DECISION)
# 2. Calls Tavily API (ACTION with TOOL)
# 3. Gets results, decides if enough (DECISION)
# 4. Synthesizes with LLM (ACTION)
# Output: "NVIDIA is trading at $495, up 3% because..."
```

---

### Q2: "What problem does this agent solve that ChatGPT alone cannot?"

**Answer:**
Two main problems:

1. **Knowledge Cutoff**
```python
# ChatGPT's knowledge ends at April 2024
# Your agent searches the web in REAL-TIME
tavily_tool.invoke("NVIDIA stock price today")  # Gets TODAY'S data
```

2. **No Tool Access**
```python
# ChatGPT can't:
# - Browse the web
# - Query databases
# - Execute code
# - Call APIs

# Your agent can do all of these by integrating tools
```

---

### Q3: "Walk me through your agent's architecture."

**Answer (use this structure):**

1. **State Management** (`AgentState`)
   - Shared memory across all components
   - Tracks task, results, attempts

2. **Tools** (External capabilities)
   - Tavily: Web search
   - Gemini: Text generation

3. **Nodes** (Workers)
   - `search_node`: Fetches data
   - `writer_node`: Synthesizes report

4. **Router** (Decision logic)
   - Determines workflow path
   - Currently: Simple counter
   - Could be: LLM-based reasoning

5. **Orchestrator** (LangGraph)
   - Executes workflow
   - Manages state passing
   - Handles control flow

---

## Section 2: Technical Implementation

### Q4: "Why use LangGraph instead of a while loop?"

**Bad Answer:** "I followed a tutorial"

**Good Answer:**
```python
# Option 1: Manual loop (what you COULD do)
def manual_agent(query):
    state = {"results": [], "attempts": 0}
    
    while state['attempts'] < 1:
        # You manage everything manually
        results = search(query)
        state['results'].extend(results)
        state['attempts'] += 1
    
    return write_report(state)

# Problems:
# - Manual state management (error-prone)
# - Hard to debug
# - Can't visualize flow
# - No checkpointing (can't save/resume)
# - Difficult to add complexity

# Option 2: LangGraph (what you DID)
workflow = StateGraph(AgentState)
workflow.add_node("search", search_node)
workflow.add_node("writer", writer_node)
# ... define flow

# Benefits:
# ✅ Automatic state management
# ✅ Visual graph representation
# ✅ Built-in debugging tools
# ✅ Easy to modify/extend
# ✅ Production-ready (checkpointing, error handling)
# ✅ Scales to complex multi-agent systems
```

---

### Q5: "Explain `Annotated[List[str], operator.add]`. What does it do?"

**Answer:**
```python
class AgentState(TypedDict):
    search_results: Annotated[List[str], operator.add]
    attempts: int

# Without Annotation:
# Node 1 returns: {"search_results": ["A", "B"]}
# State becomes: {"search_results": ["A", "B"]}
# Node 2 returns: {"search_results": ["C", "D"]}
# State becomes: {"search_results": ["C", "D"]}  ← REPLACED!

# With operator.add Annotation:
# Node 1 returns: {"search_results": ["A", "B"]}
# State becomes: {"search_results": ["A", "B"]}
# Node 2 returns: {"search_results": ["C", "D"]}
# State becomes: {"search_results": ["A", "B", "C", "D"]}  ← APPENDED!

# Why it matters:
# - Multiple searches accumulate results
# - Don't lose previous search data
# - Can do multi-step research
```

---

### Q6: "Your router only checks attempt count. How would you make it smarter?"

**Answer (show you can think beyond the basics):**

```python
# Current (dumb):
def router(state: AgentState):
    if state['attempts'] < 1:
        return "search"
    else:
        return "writer"

# Improved Version 1: Quality Check
def smart_router_v1(state: AgentState):
    # Ask LLM if data is sufficient
    prompt = f"""
    Task: {state['task']}
    Data collected: {state['search_results']}
    
    Is this enough to write a comprehensive answer?
    Answer: YES or NO
    Reasoning: [explain]
    """
    
    decision = model.invoke(prompt)
    
    if "YES" in decision.content:
        return "writer"
    elif state['attempts'] >= 3:  # Safety limit
        return "writer"  # Give up after 3 tries
    else:
        return "search"

# Improved Version 2: Multi-Factor Decision
def smart_router_v2(state: AgentState):
    # Consider multiple factors
    
    # Factor 1: Number of attempts
    if state['attempts'] >= 3:
        return "writer"  # Hard limit
    
    # Factor 2: Amount of data
    total_content = sum(len(r) for r in state['search_results'])
    if total_content < 500:  # Too little data
        return "search"
    
    # Factor 3: Relevance (LLM-based)
    relevance_check = f"""
    Task: {state['task']}
    Results: {state['search_results'][-1]}  # Last search
    
    Is this result relevant to the task? Rate 1-10.
    """
    score = model.invoke(relevance_check)
    
    if "9" in score.content or "10" in score.content:
        return "writer"  # High quality result
    else:
        return "search"  # Try again

# Improved Version 3: Self-Reflection
def reflective_router(state: AgentState):
    # Agent reflects on what it knows vs what it needs
    
    reflection = f"""
    I am a research agent.
    
    User needs: {state['task']}
    I currently know: {state['search_results']}
    
    What am I MISSING to fully answer this?
    If nothing is missing, say "COMPLETE".
    If something is missing, specify what.
    """
    
    analysis = model.invoke(reflection)
    
    if "COMPLETE" in analysis.content:
        return "writer"
    else:
        # Extract missing info for next search
        state['refined_query'] = extract_missing_info(analysis.content)
        return "search"
```

---

### Q7: "What happens if the Tavily API fails? How would you handle errors?"

**Honest Answer:**
"Currently, my code has NO error handling. If Tavily fails, the agent crashes. Here's how I would fix it:"

```python
def search_node_v1(state: AgentState):
    # Current code - NO error handling
    results = tavily_tool.invoke(state['task'])
    content = [res['content'] for res in results]
    return {"search_results": content, "attempts": state['attempts'] + 1}

# Improved with error handling:
def search_node_v2(state: AgentState):
    try:
        print(f"🔎 Searching for: {state['task']}...")
        results = tavily_tool.invoke(state['task'])
        
        # Validate results exist
        if not results or len(results) == 0:
            raise ValueError("No search results returned")
        
        content = [res['content'] for res in results]
        
        return {
            "search_results": content,
            "attempts": state['attempts'] + 1,
            "error": None
        }
        
    except Exception as e:
        print(f"❌ Search failed: {str(e)}")
        
        # Option 1: Return error state
        return {
            "search_results": [f"Search failed: {str(e)}"],
            "attempts": state['attempts'] + 1,
            "error": str(e)
        }
        
        # Option 2: Retry with exponential backoff
        # Option 3: Fall back to alternative search tool
        # Option 4: Ask user for manual input

# Advanced: Retry logic
def search_node_with_retry(state: AgentState):
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            results = tavily_tool.invoke(state['task'])
            return {"search_results": [r['content'] for r in results]}
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} in {wait_time}s...")
                time.sleep(wait_time)
            else:
                return {"search_results": [f"Failed after {max_retries} attempts: {e}"]}
```

---

## Section 3: LangChain/LangGraph Deep Dive

### Q8: "Explain the difference between `add_edge` and `add_conditional_edges`."

**Answer:**

```python
# add_edge - STATIC, always goes to the same next node
workflow.add_edge("writer", END)
# Meaning: "After writer finishes, ALWAYS go to END"

# No decisions, no branching, deterministic path

# add_conditional_edges - DYNAMIC, calls a function to decide
workflow.add_conditional_edges(
    "search",     # From this node
    router,       # Call this function with current state
    {             # Map function's return value to next node
        "search": "search",   # If router returns "search"
        "writer": "writer"    # If router returns "writer"
    }
)

# Example execution:
# 1. search_node completes
# 2. LangGraph calls router(state)
# 3. router returns "writer"
# 4. LangGraph looks up mapping: "writer" → writer_node
# 5. LangGraph executes writer_node
```

**Visual:**
```
add_edge:
┌────────┐
│ Writer │──────────→ END
└────────┘
  (always goes here)

add_conditional_edges:
┌────────┐
│ Search │─────→ [router() decides]
└────────┘              │
                  ┌─────┴─────┐
                  │           │
                  ↓           ↓
              "search"    "writer"
                  │           │
                  ↓           ↓
            ┌────────┐   ┌────────┐
            │ Search │   │ Writer │
            └────────┘   └────────┘
```

---

### Q9: "What is the `END` marker? Can you skip it?"

**Answer:**

```python
from langgraph.graph import END

# END is a special sentinel value
# It tells LangGraph: "The workflow is complete, stop execution"

workflow.add_edge("writer", END)

# What happens during execution:
# 1. writer_node completes
# 2. LangGraph sees next node is END
# 3. LangGraph stops execution
# 4. Returns final state to user

# Can you skip it? NO!
# ❌ Bad:
workflow.add_node("writer", writer_node)
# No edge after writer → LangGraph doesn't know when to stop

# ❌ Also bad:
workflow.add_edge("writer", "nonexistent_node")
# Error: No node named "nonexistent_node"

# ✅ Correct:
workflow.add_edge("writer", END)
# or
workflow.add_conditional_edges("writer", some_router, {"end": END, "continue": "other_node"})
```

**Every workflow MUST have at least one path to END, otherwise it runs forever or crashes.**

---

### Q10: "How does state merging work in LangGraph?"

**Answer:**

```python
# State merging is SHALLOW by default

# Initial state:
state = {
    "task": "What is NVIDIA's stock?",
    "search_results": [],
    "attempts": 0
}

# Node 1 returns:
return {
    "search_results": ["result 1", "result 2"],
    "attempts": 1
}

# LangGraph merges:
state = {
    "task": "What is NVIDIA's stock?",  # Unchanged (not in return)
    "search_results": ["result 1", "result 2"],  # Updated
    "attempts": 1  # Updated
}

# Node 2 returns:
return {
    "search_results": ["result 3"],  # Would normally REPLACE
    "attempts": 2
}

# But we have Annotated[List[str], operator.add]:
state = {
    "task": "What is NVIDIA's stock?",
    "search_results": ["result 1", "result 2", "result 3"],  # APPENDED
    "attempts": 2  # REPLACED
}

# Key rules:
# 1. Keys not in return dict → unchanged
# 2. Keys in return dict → updated/replaced
# 3. Annotated with operator.add → appended instead of replaced
```

---

## Section 4: System Design & Scalability

### Q11: "Your agent does only 1 search. How would you implement multi-step deep research?"

**Answer:**

```python
# Approach 1: Increase attempt limit
def simple_deep_research_router(state: AgentState):
    if state['attempts'] < 3:  # Do 3 searches instead of 1
        return "search"
    else:
        return "writer"

# Approach 2: Different search strategies per step
workflow.add_node("broad_search", broad_search_node)     # Step 1: Overview
workflow.add_node("specific_search", specific_search_node)  # Step 2: Details
workflow.add_node("verification_search", verify_search_node)  # Step 3: Fact-check

workflow.set_entry_point("broad_search")
workflow.add_edge("broad_search", "specific_search")
workflow.add_edge("specific_search", "verification_search")
workflow.add_edge("verification_search", "writer")

# Approach 3: Iterative refinement
def iterative_router(state: AgentState):
    if state['attempts'] == 0:
        return "broad_search"  # First pass: get overview
    elif state['attempts'] == 1:
        # Analyze what we found, search for gaps
        gaps = identify_gaps(state['search_results'])
        state['refined_query'] = gaps
        return "targeted_search"
    elif state['attempts'] >= 2:
        return "writer"

# Approach 4: Quality-gated progression
def quality_gated_router(state: AgentState):
    if state['attempts'] == 0:
        return "search"
    
    # Evaluate quality of current data
    quality_score = evaluate_quality(state)
    
    if quality_score >= 8 or state['attempts'] >= 3:
        return "writer"
    else:
        # Refine search based on what's missing
        return "search"
```

---

### Q12: "How would you handle rate limits on Tavily API?"

**Answer:**

```python
import time
from datetime import datetime, timedelta

# Approach 1: Simple delay
def search_node_with_delay(state: AgentState):
    if state['attempts'] > 0:
        time.sleep(2)  # Wait 2 seconds between searches
    
    results = tavily_tool.invoke(state['task'])
    return {"search_results": [r['content'] for r in results]}

# Approach 2: Rate limiter class
class RateLimiter:
    def __init__(self, max_calls=5, time_window=60):
        self.max_calls = max_calls
        self.time_window = time_window  # seconds
        self.calls = []
    
    def wait_if_needed(self):
        now = datetime.now()
        
        # Remove old calls outside time window
        self.calls = [t for t in self.calls if now - t < timedelta(seconds=self.time_window)]
        
        if len(self.calls) >= self.max_calls:
            # Calculate wait time
            oldest_call = min(self.calls)
            wait_seconds = (oldest_call + timedelta(seconds=self.time_window) - now).total_seconds()
            print(f"Rate limit reached. Waiting {wait_seconds:.1f}s...")
            time.sleep(wait_seconds)
        
        self.calls.append(now)

# Usage:
rate_limiter = RateLimiter(max_calls=3, time_window=60)  # 3 calls per minute

def search_node_rate_limited(state: AgentState):
    rate_limiter.wait_if_needed()
    results = tavily_tool.invoke(state['task'])
    return {"search_results": [r['content'] for r in results]}

# Approach 3: Exponential backoff on error
def search_with_backoff(state: AgentState):
    for retry in range(3):
        try:
            results = tavily_tool.invoke(state['task'])
            return {"search_results": [r['content'] for r in results]}
        except RateLimitError:
            if retry < 2:
                wait = (2 ** retry) * 5  # 5s, 10s, 20s
                print(f"Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            else:
                return {"search_results": ["Rate limit exceeded"]}
```

---

### Q13: "What are the limitations of your current implementation?"

**Honest Answer (shows self-awareness):**

```python
# 1. NO ERROR HANDLING
# ❌ If Tavily API fails → Agent crashes
# ❌ If Gemini times out → Agent crashes
# ✅ Fix: Add try-except blocks and retry logic

# 2. HARDCODED API KEYS
os.environ["TAVILY_API_KEY"] = "tvly-YOUR_KEY_HERE"  # ❌ Security risk!
# ✅ Fix: Use environment variables
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

# 3. DUMB ROUTER (just counts)
if state['attempts'] < 1:  # ❌ No quality check
    return "search"
# ✅ Fix: LLM-based quality evaluation

# 4. NO CACHING
# ❌ Same query searched multiple times wastes API calls
# ✅ Fix: Cache search results
cache = {}
def cached_search(query):
    if query in cache:
        return cache[query]
    results = tavily_tool.invoke(query)
    cache[query] = results
    return results

# 5. NO CONVERSATION MEMORY
# ❌ Can't have multi-turn conversations
# ✅ Fix: Add chat_history to state

# 6. LIMITED SEARCH RESULTS (max_results=3)
tavily_tool = TavilySearchResults(max_results=3)  # ❌ Might miss important info
# ✅ Fix: Increase or make it dynamic

# 7. NO COST TRACKING
# ❌ No idea how much API calls cost
# ✅ Fix: Track API usage
total_cost = 0
def track_cost(api_call):
    global total_cost
    result = api_call()
    total_cost += calculate_cost(result)
    return result

# 8. SINGLE-THREADED
# ❌ Can't search multiple topics in parallel
# ✅ Fix: Use async/await or parallel nodes

# 9. NO SOURCE ATTRIBUTION
# ❌ Report doesn't cite which search result info came from
# ✅ Fix: Track sources and include citations

# 10. NO USER FEEDBACK LOOP
# ❌ Can't ask user for clarification if query is ambiguous
# ✅ Fix: Add human-in-the-loop node
```

---

## Section 5: Real-World Application

### Q14: "How would you deploy this in production?"

**Answer:**

```python
# Production Architecture:

# 1. API WRAPPER (FastAPI)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app_server = FastAPI()

class ResearchRequest(BaseModel):
    query: str
    max_searches: int = 3

class ResearchResponse(BaseModel):
    report: str
    sources: list[str]
    cost: float
    duration: float

@app_server.post("/research", response_model=ResearchResponse)
async def research_endpoint(request: ResearchRequest):
    try:
        start_time = time.time()
        
        # Run agent
        result = app.invoke({
            "task": request.query,
            "search_results": [],
            "attempts": 0
        })
        
        duration = time.time() - start_time
        
        return ResearchResponse(
            report=result['report'],
            sources=result['sources'],
            cost=calculate_cost(result),
            duration=duration
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. ENVIRONMENT VARIABLES
from dotenv import load_dotenv
load_dotenv()

TAVILY_KEY = os.getenv("TAVILY_API_KEY")
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")

# 3. CACHING LAYER (Redis)
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cached_search(query: str):
    # Check cache first
    cached = redis_client.get(f"search:{query}")
    if cached:
        return json.loads(cached)
    
    # Cache miss - call API
    results = tavily_tool.invoke(query)
    
    # Store in cache (expire after 1 hour)
    redis_client.setex(f"search:{query}", 3600, json.dumps(results))
    
    return results

# 4. RATE LIMITING (per user)
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app_server.post("/research")
@limiter.limit("10/minute")  # Max 10 requests per minute per IP
async def research_endpoint(request: ResearchRequest):
    # ...

# 5. LOGGING & MONITORING
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_node_production(state: AgentState):
    logger.info(f"[{datetime.now()}] Starting search: {state['task']}")
    
    try:
        results = tavily_tool.invoke(state['task'])
        logger.info(f"Search successful. Got {len(results)} results")
        return {"search_results": [r['content'] for r in results]}
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise

# 6. ASYNC FOR PERFORMANCE
import asyncio

async def async_search_node(state: AgentState):
    # Use async version of Tavily
    results = await tavily_tool.ainvoke(state['task'])
    return {"search_results": [r['content'] for r in results]}

# 7. COST TRACKING
class CostTracker:
    def __init__(self):
        self.total_cost = 0
        self.tavily_calls = 0
        self.gemini_calls = 0
    
    def track_tavily(self, num_results):
        cost_per_search = 0.001  # Example pricing
        self.total_cost += cost_per_search
        self.tavily_calls += 1
    
    def track_gemini(self, input_tokens, output_tokens):
        input_cost = input_tokens * 0.00001
        output_cost = output_tokens * 0.00003
        self.total_cost += input_cost + output_cost
        self.gemini_calls += 1

# 8. DOCKER DEPLOYMENT
# Dockerfile:
"""
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app_server", "--host", "0.0.0.0", "--port", "8000"]
"""

# docker-compose.yml:
"""
version: '3.8'
services:
  agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - TAVILY_API_KEY=${TAVILY_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    depends_on:
      - redis
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
"""

# 9. HEALTH CHECK ENDPOINT
@app_server.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

---

### Q15: "How would you test this agent?"

**Answer:**

```python
import pytest
from unittest.mock import Mock, patch

# 1. UNIT TESTS - Test individual nodes

def test_search_node():
    """Test search node returns correct structure"""
    # Mock Tavily
    with patch('tavily_tool.invoke') as mock_tavily:
        mock_tavily.return_value = [
            {"content": "Result 1"},
            {"content": "Result 2"}
        ]
        
        state = {"task": "test query", "search_results": [], "attempts": 0}
        result = search_node(state)
        
        assert "search_results" in result
        assert len(result['search_results']) == 2
        assert result['attempts'] == 1

def test_router_logic():
    """Test router makes correct decisions"""
    # Test: Should search when attempts < 1
    state = {"attempts": 0}
    assert router(state) == "search"
    
    # Test: Should write when attempts >= 1
    state = {"attempts": 1}
    assert router(state) == "writer"
    
    state = {"attempts": 5}
    assert router(state) == "writer"

def test_writer_node():
    """Test writer node generates output"""
    with patch('model.invoke') as mock_model:
        mock_response = Mock()
        mock_response.content = "Test report"
        mock_model.return_value = mock_response
        
        state = {
            "task": "test",
            "search_results": ["data 1", "data 2"]
        }
        
        result = writer_node(state)
        assert mock_model.called


# 2. INTEGRATION TESTS - Test full workflow

def test_full_workflow():
    """Test complete agent execution"""
    with patch('tavily_tool.invoke') as mock_tavily, \
         patch('model.invoke') as mock_model:
        
        # Mock search results
        mock_tavily.return_value = [{"content": "NVIDIA stock: $495"}]
        
        # Mock LLM response
        mock_response = Mock()
        mock_response.content = "NVIDIA is trading at $495"
        mock_model.return_value = mock_response
        
        # Run workflow
        initial_state = {
            "task": "NVIDIA stock price",
            "search_results": [],
            "attempts": 0
        }
        
        result = app.invoke(initial_state)
        
        # Assertions
        assert mock_tavily.called
        assert mock_model.called


# 3. ERROR HANDLING TESTS

def test_search_failure_handling():
    """Test agent handles search failures gracefully"""
    with patch('tavily_tool.invoke') as mock_tavily:
        mock_tavily.side_effect = Exception("API Error")
        
        state = {"task": "test", "search_results": [], "attempts": 0}
        
        # Should not crash
        try:
            result = search_node(state)
            # Should return error state
            assert "error" in result or "failed" in str(result)
        except Exception as e:
            pytest.fail(f"Agent should handle errors gracefully, got: {e}")


# 4. QUALITY TESTS

def test_report_quality():
    """Test that generated reports meet quality standards"""
    state = {
        "task": "What is AI?",
        "search_results": [
            "AI is artificial intelligence...",
            "Machine learning is a subset of AI..."
        ]
    }
    
    with patch('model.invoke') as mock_model:
        mock_response = Mock()
        mock_response.content = "Report on AI"
        mock_model.return_value = mock_response
        
        result = writer_node(state)
        
        # Check that prompt includes context
        call_args = mock_model.call_args[0][0]
        assert "AI is artificial intelligence" in str(call_args)


# 5. PERFORMANCE TESTS

@pytest.mark.slow
def test_performance():
    """Test agent completes within acceptable time"""
    import time
    
    start = time.time()
    
    # Run with mocks to isolate agent logic
    with patch('tavily_tool.invoke'), patch('model.invoke'):
        app.invoke({"task": "test", "search_results": [], "attempts": 0})
    
    duration = time.time() - start
    
    assert duration < 5.0, f"Agent took {duration}s, should be < 5s"


# 6. STATE MANAGEMENT TESTS

def test_state_accumulation():
    """Test that search results accumulate correctly"""
    state = {
        "task": "test",
        "search_results": ["result 1"],
        "attempts": 0
    }
    
    with patch('tavily_tool.invoke') as mock_tavily:
        mock_tavily.return_value = [{"content": "result 2"}]
        
        updated_state = search_node(state)
        
        # Should append, not replace (due to operator.add)
        # Note: This requires actually running through LangGraph
        # which handles the merging


# 7. END-TO-END TESTS

@pytest.mark.e2e
def test_real_api_integration():
    """Test with real APIs (skip in CI/CD)"""
    # Only run if API keys are set
    if not os.getenv("TAVILY_API_KEY"):
        pytest.skip("No API key")
    
    result = app.invoke({
        "task": "What is 2+2?",
        "search_results": [],
        "attempts": 0
    })
    
    # Very basic check - just ensure it completed
    assert result is not None
```

**Test Coverage Strategy:**
```bash
# Run all tests
pytest

# Run only unit tests
pytest -m "not slow and not e2e"

# Run with coverage report
pytest --cov=agent --cov-report=html

# Run integration tests
pytest -m integration

# Run end-to-end tests (with real APIs)
pytest -m e2e --api-key=$TAVILY_KEY
```

---

## Section 6: Curveball Questions

### Q16: "Why Gemini and not OpenAI GPT-4?"

**Answer:**

```python
# Comparison:

# Gemini 1.5 Flash (what you used):
# ✅ FREE (within quota)
# ✅ Fast response times (~1-2s)
# ✅ Good enough for summarization
# ✅ 1M token context window
# ❌ Less powerful than GPT-4 for complex reasoning

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# OpenAI GPT-4:
# ✅ More powerful reasoning
# ✅ Better at complex tasks
# ✅ Industry standard
# ❌ Expensive ($0.03 per 1K input tokens)
# ❌ Slower (~3-5s response)

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# My reasoning for choosing Gemini:
# 1. This is a DEMO/LEARNING project
# 2. Task is simple (summarize search results)
# 3. Cost matters for prototyping
# 4. Speed is important for UX

# In production, I would:
# - Benchmark both for quality
# - Calculate cost per query
# - A/B test user satisfaction
# - Maybe use GPT-4 for complex queries, Gemini for simple ones
```

---

### Q17: "Why `temperature=0`? When would you use higher temperature?"

**Answer:**

```python
# Temperature controls randomness/creativity

# temperature=0 (Deterministic)
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# Same input → SAME output every time
# Output: "NVIDIA is trading at $495, up 3% due to earnings beat"
# Output: "NVIDIA is trading at $495, up 3% due to earnings beat"  (identical)

# Use when:
# ✅ Factual reporting (your use case)
# ✅ Data extraction
# ✅ Summarization
# ✅ Code generation
# ✅ Need consistency/reproducibility

# temperature=0.7-1.0 (Creative)
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.9)

# Same input → DIFFERENT outputs each time
# Output: "NVIDIA stock surged 3% to $495 after stellar earnings"
# Output: "The chipmaker's shares climbed to $495, reflecting strong demand"  (varied)

# Use when:
# ✅ Creative writing
# ✅ Marketing copy
# ✅ Brainstorming
# ✅ Diverse responses needed
# ✅ Chat applications

# For your agent:
# temperature=0 is CORRECT because:
# - User wants FACTS, not creative interpretations
# - Need consistent, reliable reports
# - Debugging is easier (reproducible outputs)
```

---

## Key Takeaways - How to Ace the Interview

1. **Understand WHY, not just WHAT**
   - Don't just say "I used LangGraph"
   - Say "I used LangGraph because X, Y, Z benefits"

2. **Be honest about limitations**
   - "My router is simple - it just counts"
   - "Here's how I would make it smarter..."
   - Shows growth mindset

3. **Think beyond the code**
   - Production deployment
   - Cost optimization
   - Error handling
   - Testing strategy

4. **Use analogies**
   - "Orchestrator is like a factory manager"
   - "Agent is like a research assistant with internet access"
   - Makes complex concepts clear

5. **Connect to real problems**
   - "ChatGPT can't tell you today's stock price"
   - "This agent solves that by..."

6. **Show you can extend it**
   - "Currently it does X"
   - "I could add Y by doing Z"

---

## Practice Exercise

Before the interview, be able to explain:

1. **In 30 seconds:** What your agent does
2. **In 2 minutes:** How it works (architecture)
3. **In 5 minutes:** Deep technical dive into any component
4. **In 1 minute:** What you'd improve next

Good luck! 🚀
