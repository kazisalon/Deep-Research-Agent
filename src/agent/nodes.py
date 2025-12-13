"""Worker nodes for the research agent."""

import os
from typing import Dict, Any

from config.settings import settings
from src.utils.logger import get_logger
from src.utils.cost_tracker import CostTracker
from src.tools.search import SearchTool
from .state import AgentState

# Set environment variables for APIs
os.environ["TAVILY_API_KEY"] = settings.tavily_api_key

logger = get_logger()


class SearchNode:
    """Node responsible for web search operations."""
    
    def __init__(self, cost_tracker: CostTracker):
        self.search_tool = SearchTool()
        self.cost_tracker = cost_tracker
    
    def __call__(self, state: AgentState) -> Dict[str, Any]:
        """
        Execute web search for the given task.
        
        Args:
            state: Current agent state
            
        Returns:
            State update with search results
        """
        try:
            logger.info(f"🔎 Search attempt #{state['attempts'] + 1}: {state['task']}")
            
            # Perform search
            results = self.search_tool.search(state['task'])
            
            # Track cost
            if settings.track_costs:
                self.cost_tracker.track_search(num_results=len(results))
            
            # Extract content
            content = [res.get('content', '') for res in results if res.get('content')]
            
            if not content:
                logger.warning("No search results found")
                return {
                    "search_results": ["No results found"],
                    "attempts": state['attempts'] + 1,
                    "error": "No search results"
                }
            
            logger.info(f"✅ Found {len(content)} results")
            
            return {
                "search_results": content,
                "attempts": state['attempts'] + 1,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"❌ Search failed: {str(e)}")
            return {
                "search_results": [f"Search error: {str(e)}"],
                "attempts": state['attempts'] + 1,
                "error": str(e)
            }


class WriterNode:
    """Node responsible for synthesizing research reports."""
    
    def __init__(self, cost_tracker: CostTracker):
        from openai import OpenAI
        
        # Initialize Groq client (OpenAI-compatible)
        self.client = OpenAI(
            api_key=settings.groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        self.cost_tracker = cost_tracker
    
    def __call__(self, state: AgentState) -> Dict[str, Any]:
        """
        Generate a research report from search results.
        
        Args:
            state: Current agent state
            
        Returns:
            State update with final report
        """
        try:
            logger.info("✍️ Generating research report...")
            
            # Combine all search results
            context = "\n\n---\n\n".join(state['search_results'])
            
            # Build prompt
            prompt = self._build_prompt(state['task'], context)
            
            # Generate report using Groq
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Groq's best model
                messages=[
                    {"role": "system", "content": "You are a Senior Research Analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.model_temperature,
                max_tokens=2000
            )
            
            report_content = response.choices[0].message.content
            
            # Track cost
            if settings.track_costs:
                input_tokens = response.usage.prompt_tokens
                output_tokens = response.usage.completion_tokens
                self.cost_tracker.track_llm(input_tokens, output_tokens)
            
            logger.info("✅ Report generated successfully")
            
            # Print the report
            self._print_report(report_content)
            
            return {
                "final_report": report_content,
                "error": None
            }
            
        except Exception as e:
            import traceback
            logger.error(f"❌ Report generation failed: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return {
                "final_report": f"Error generating report: {str(e)}",
                "error": str(e)
            }
    
    def _build_prompt(self, task: str, context: str) -> str:
        """Build the prompt for report generation."""
        return f"""You are a Senior Research Analyst with expertise in synthesizing information.

Your task is to write a comprehensive, factual research report based ONLY on the context provided.

User Query: {task}

Context from web sources:
{context}

Instructions:
1. Answer the user's query directly and comprehensively
2. Focus on facts, data, and numbers
3. Cite sources using [Source 1], [Source 2], etc.
4. Organize information logically with clear sections
5. If information is incomplete, state what's missing
6. Be concise but thorough
7. Use professional language

Write the research report now:
"""
    
    def _print_report(self, report: str) -> None:
        """Print the report with formatting."""
        print("\n" + "="*80)
        print("📊 RESEARCH REPORT")
        print("="*80 + "\n")
        print(report)
        print("\n" + "="*80 + "\n")
