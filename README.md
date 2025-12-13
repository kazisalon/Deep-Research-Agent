# Deep Research Agent 🔬

A production-ready AI research assistant that autonomously searches the web, gathers information, and synthesizes comprehensive reports using LangGraph and Gemini AI.

## 🌟 Features

- **Autonomous Research**: Automatically searches the web and gathers current information
- **Smart Orchestration**: Uses LangGraph for reliable workflow management
- **Cost Tracking**: Monitors API usage and costs
- **Error Handling**: Robust retry logic and graceful degradation
- **Professional Structure**: Modular, scalable, and maintainable codebase
- **Comprehensive Logging**: Debug and monitor agent behavior
- **Type Safety**: Full type hints for better IDE support

## 🏗️ Architecture

```
┌─────────────┐
│ User Query  │
└──────┬──────┘
       ↓
  ┌─────────────┐
  │ Search Node │ ← Tavily Web Search
  └──────┬──────┘
         ↓
  ┌─────────────┐
  │   Router    │ ← Decide: Continue or Write?
  └──────┬──────┘
         │
    ┌────┴────┐
    ↓         ↓
 [Loop]   ┌─────────────┐
          │ Writer Node │ ← Gemini AI Synthesis
          └──────┬──────┘
                 ↓
            [Final Report]
```

## 📁 Project Structure

```
Deep-Research-Agent/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration management
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── state.py         # Agent state definition
│   │   ├── nodes.py         # Worker nodes (Search, Writer)
│   │   ├── routers.py       # Decision logic
│   │   └── graph.py         # LangGraph workflow
│   ├── tools/
│   │   ├── __init__.py
│   │   └── search.py        # Tavily search wrapper
│   └── utils/
│       ├── __init__.py
│       ├── logger.py        # Logging setup
│       └── cost_tracker.py  # API cost tracking
├── .env.example             # Environment template
├── .gitignore
├── requirements.txt
├── main.py                  # Entry point
└── README.md
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+ (Recommended: 3.11 or 3.12)
- Tavily API key ([Get it here](https://tavily.com))
- Google AI API key ([Get it here](https://aistudio.google.com/apikey))

### 2. Installation

```bash
# Clone or navigate to the project
cd Deep-Research-Agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# TAVILY_API_KEY=your_actual_key_here
# GOOGLE_API_KEY=your_actual_key_here
```

### 4. Run the Agent

```bash
python main.py
```

## 🔧 Configuration Options

Edit `.env` to customize:

| Variable | Description | Default |
|----------|-------------|---------|
| `TAVILY_API_KEY` | Tavily search API key | Required |
| `GOOGLE_API_KEY` | Google AI API key | Required |
| `MODEL_NAME` | Gemini model to use | gemini-1.5-flash |
| `MODEL_TEMPERATURE` | Creativity level (0-1) | 0 |
| `MAX_SEARCH_ATTEMPTS` | Max search iterations | 3 |
| `MAX_SEARCH_RESULTS` | Results per search | 3 |
| `LOG_LEVEL` | Logging verbosity | INFO |
| `TRACK_COSTS` | Enable cost tracking | true |

## 💡 Usage Examples

### Customize the Query

Edit `main.py`:

```python
user_query = "What are the latest breakthroughs in quantum computing?"
```

### Adjust Search Depth

In `.env`:

```bash
MAX_SEARCH_ATTEMPTS=5  # Do 5 searches before writing
```

### Change the Model

In `.env`:

```bash
MODEL_NAME=gemini-1.5-pro  # Use Pro model for better quality
```

## 🧪 Testing

Create a test file:

```python
# test_basic.py
from src.agent.routers import should_continue_search

def test_router():
    state = {"attempts": 0, "error": None}
    assert should_continue_search(state) == "search"
    
    state = {"attempts": 3, "error": None}
    assert should_continue_search(state) == "writer"
```

Run tests:

```bash
pytest test_basic.py
```

## 📊 Cost Tracking

The agent automatically tracks:
- Number of search API calls
- Number of LLM API calls
- Estimated token usage
- Total cost in USD

Example output:

```
💰 COST SUMMARY
================================================================================
  Total Cost Usd: 0.0023
  Search Calls: 3
  Llm Calls: 1
  Total Tokens: 2847
  Session Duration Seconds: 5.43
================================================================================
```

## 🔍 How It Works

### 1. State Management

The agent maintains shared state across all nodes:

```python
{
    "task": "User's research query",
    "search_results": ["result 1", "result 2", ...],  # Accumulates
    "attempts": 2,
    "error": None,
    "final_report": "Generated report text"
}
```

### 2. Search Node

- Calls Tavily API to search the web
- Implements retry logic (3 attempts with exponential backoff)
- Tracks API costs
- Handles errors gracefully

### 3. Router (Decision Maker)

- Currently: Simple counter-based logic
- Decides if more searches are needed
- Can be upgraded to LLM-based quality evaluation

### 4. Writer Node

- Synthesizes all search results
- Uses Gemini to generate comprehensive report
- Includes source citations
- Formats output professionally

## 🎯 Extending the Agent

### Add Advanced Routing

Replace simple counter logic with LLM-based evaluation:

```python
# In src/agent/routers.py
def smart_router(state: AgentState) -> Literal["search", "writer"]:
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    
    prompt = f"""
    Task: {state['task']}
    Data collected: {len(state['search_results'])} results
    
    Is this enough to write a comprehensive answer?
    Reply: SEARCH or WRITE
    """
    
    decision = model.invoke(prompt)
    return "search" if "SEARCH" in decision.content else "writer"
```

### Add Caching

```python
# In src/tools/search.py
import hashlib
import json

class SearchTool:
    def __init__(self):
        self.cache = {}
    
    def search(self, query: str):
        cache_key = hashlib.md5(query.encode()).hexdigest()
        
        if cache_key in self.cache:
            logger.info("Cache hit!")
            return self.cache[cache_key]
        
        results = self.tavily.invoke(query)
        self.cache[cache_key] = results
        return results
```

### Add Multiple Tools

Create new nodes for different data sources:

```python
# src/agent/nodes.py
class DatabaseNode:
    def __call__(self, state):
        # Query internal database
        ...

class CalculatorNode:
    def __call__(self, state):
        # Perform calculations
        ...
```

## 🐛 Troubleshooting

### Python Version Issues

If you see `TypeError: unhashable type: 'list'`:

```bash
# Upgrade to Python 3.10+
python --version  # Check current version

# Create new venv with Python 3.11
python3.11 -m venv venv
```

### API Key Errors

```bash
# Verify .env file exists
ls -la .env

# Check if keys are set
cat .env | grep API_KEY
```

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear cache
pip cache purge
```

## 📚 Learn More

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Tavily API Docs](https://docs.tavily.com/)
- [Google AI Studio](https://aistudio.google.com/)

## 🤝 Contributing

Improvements welcome! Consider adding:
- Unit tests
- FastAPI wrapper for REST API
- Redis caching layer
- Multi-agent collaboration
- Streaming responses
- Cost optimization strategies

## 📄 License

MIT License - Feel free to use in your projects!

---

**Built with ❤️ using LangGraph, Gemini AI, and Tavily Search**
