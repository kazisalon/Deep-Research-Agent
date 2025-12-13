"""
Deep Research Agent - Main Entry Point

A production-ready AI research assistant that can search the web,
gather information, and synthesize comprehensive reports.
"""

import sys
import os
from pathlib import Path

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        # Set console to UTF-8
        os.system('chcp 65001 >nul 2>&1')
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings
from src.utils.logger import setup_logger, get_logger
from src.utils.cost_tracker import CostTracker
from src.agent import create_research_agent


def main():
    """Main execution function."""
    
    # Setup logging
    setup_logger(
        name="deep_research_agent",
        level=settings.log_level
    )
    logger = get_logger()
    
    try:
        # Validate API keys
        logger.info("🔐 Validating API keys...")
        settings.validate_keys()
        
        # Initialize cost tracker
        cost_tracker = CostTracker(
            cost_per_search=settings.cost_per_search
        )
        
        # Create the agent
        logger.info("🚀 Initializing Deep Research Agent...")
        agent = create_research_agent(cost_tracker)
        
        # Define research query
        user_query = "What is the current stock price of NVIDIA and why is it moving today?"
        
        logger.info(f"📝 Research Query: {user_query}")
        
        # Initialize state
        initial_state = {
            "task": user_query,
            "search_results": [],
            "attempts": 0,
            "error": None,
            "final_report": None
        }
        
        # Run the agent
        logger.info("🏃 Starting research workflow...")
        print("\n" + "="*80)
        print("🔬 DEEP RESEARCH AGENT")
        print("="*80)
        print(f"Query: {user_query}\n")
        
        final_state = agent.invoke(initial_state)
        
        # Print cost summary
        if settings.track_costs:
            print("\n" + "="*80)
            print("💰 COST SUMMARY")
            print("="*80)
            summary = cost_tracker.get_summary()
            for key, value in summary.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
            print("="*80 + "\n")
        
        logger.info("✅ Research workflow completed successfully")
        
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        print("\nPlease:")
        print("1. Copy .env.example to .env")
        print("2. Add your API keys to the .env file")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
