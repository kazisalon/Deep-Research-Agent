"""Cost tracking for API usage."""

from typing import Dict
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CostTracker:
    """Track API usage costs for the research agent."""
    
    # Official pricing as of Dec 2024
    # Tavily: https://tavily.com/pricing
    cost_per_search: float = 0.001  # $0.001 per search (paid tier)
    
    # Groq (Llama 3.3 70B Versatile): https://wow.groq.com/
    # Free tier: 30 requests/min, 14,400/day - NO CHARGE
    # Paid tier (if you exceed limits):
    cost_per_1k_input_tokens: float = 0.00059  # $0.59 per 1M tokens
    cost_per_1k_output_tokens: float = 0.00079  # $0.79 per 1M tokens
    
    total_cost: float = field(default=0.0, init=False)
    search_calls: int = field(default=0, init=False)
    llm_calls: int = field(default=0, init=False)
    input_tokens: int = field(default=0, init=False)
    output_tokens: int = field(default=0, init=False)
    
    session_start: datetime = field(default_factory=datetime.now, init=False)
    
    def track_search(self, num_results: int = 1) -> None:
        """Track a search API call."""
        self.search_calls += 1
        self.total_cost += self.cost_per_search * num_results
    
    def track_llm(self, input_tokens: int, output_tokens: int) -> None:
        """Track an LLM API call."""
        self.llm_calls += 1
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        
        input_cost = (input_tokens / 1000) * self.cost_per_1k_input_tokens
        output_cost = (output_tokens / 1000) * self.cost_per_1k_output_tokens
        
        self.total_cost += input_cost + output_cost
    
    def get_summary(self) -> Dict[str, any]:
        """Get a summary of tracked costs."""
        duration = (datetime.now() - self.session_start).total_seconds()
        
        return {
            "total_cost_usd": round(self.total_cost, 4),
            "search_calls": self.search_calls,
            "llm_calls": self.llm_calls,
            "total_tokens": self.input_tokens + self.output_tokens,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "session_duration_seconds": round(duration, 2),
        }
    
    def reset(self) -> None:
        """Reset all counters."""
        self.total_cost = 0.0
        self.search_calls = 0
        self.llm_calls = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.session_start = datetime.now()
