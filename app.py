"""
Deep Research Agent - Clean Professional Web Interface
Simple, elegant UI with solid colors and Font Awesome icons
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings
from src.agent import create_research_agent, AgentState
from src.utils.cost_tracker import CostTracker
from src.utils.logger import get_logger

# Page config
st.set_page_config(
    page_title="Deep Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean Professional Theme
st.markdown("""
<style>
    /* Import Fonts and Icons */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Dark Background */
    .stApp {
        background: #0a0e27;
    }
    
    /* Reduce spacing */
    .block-container {
        padding-top: 2rem !important;
        max-width: 1200px;
    }
    
    /* Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 0 0 0.5rem 0;
    }
    
    .subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.6);
        margin-bottom: 2rem;
    }
    
    /* Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        transition: all 0.2s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Input */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 8px !important;
        color: white !important;
        font-size: 1rem !important;
        padding: 1rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: #667eea;
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-size: 1rem;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background: #5568d3;
        transform: translateY(-1px);
    }
    
    /* Example Buttons */
    div[data-testid="column"] .stButton>button {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: white;
        padding: 0.6rem 1rem;
        font-size: 0.9rem;
    }
    
    div[data-testid="column"] .stButton>button:hover {
        background: rgba(102, 126, 234, 0.2);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 15, 35, 0.95);
        border-right: 1px solid rgba(102, 126, 234, 0.15);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #667eea;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    /* Progress */
    .stProgress > div > div > div > div {
        background: #667eea;
    }
    
    /* Text */
    p, span, div, label {
        color: rgba(255, 255, 255, 0.9);
    }
    
    h1, h2, h3 {
        color: white;
    }
    
    /* Hide branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem 0;
    }
    
    .status-connected {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-missing {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Result card */
    .result-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin: 1rem 0;
        color: white;
        line-height: 1.7;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #10b981;
        padding: 0.6rem 1.5rem;
    }
    
    .stDownloadButton>button:hover {
        background: rgba(16, 185, 129, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_query' not in st.session_state:
    st.session_state.current_query = ""

# Header - Clean design
st.markdown('<div style="display: flex; align-items: center; gap: 1rem;"><span style="font-size: 2.5rem;">🔬</span><h1 class="main-header">Deep Research Agent</h1></div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Web Research with LangGraph + Groq</p>', unsafe_allow_html=True)

# Professional Sidebar
with st.sidebar:
    # Configuration Header
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 1.5rem 0; border-bottom: 1px solid rgba(102, 126, 234, 0.2);'>
        <h2 style='margin: 0; font-size: 1.5rem; font-weight: 700; color: white;'>⚙️ Configuration</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # API Connection Status
    st.markdown("""
    <div style='margin: 1.5rem 0 1rem 0;'>
        <div style='font-size: 0.9rem; font-weight: 600; color: rgba(255,255,255,0.7); margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;'>
            🔑 API Connections
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status Cards for APIs
    groq_status = "connected" if settings.groq_api_key else "disconnected"
    tavily_status = "connected" if settings.tavily_api_key else "disconnected"
    
    groq_color = "#10b981" if settings.groq_api_key else "#ef4444"
    tavily_color = "#10b981" if settings.tavily_api_key else "#ef4444"
    
    groq_bg = "rgba(16, 185, 129, 0.1)" if settings.groq_api_key else "rgba(239, 68, 68, 0.1)"
    tavily_bg = "rgba(16, 185, 129, 0.1)" if settings.tavily_api_key else "rgba(239, 68, 68, 0.1)"
    
    st.markdown(f"""
    <div style='margin-bottom: 0.5rem;'>
        <div style='background: {groq_bg}; border-left: 3px solid {groq_color}; padding: 0.75rem 1rem; border-radius: 6px;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='font-weight: 600; color: white; font-size: 0.9rem;'>⚡ Groq API</span>
                <span style='color: {groq_color}; font-weight: 700; font-size: 0.85rem;'>{'ACTIVE' if settings.groq_api_key else 'INACTIVE'}</span>
            </div>
        </div>
    </div>
    
    <div style='margin-bottom: 1rem;'>
        <div style='background: {tavily_bg}; border-left: 3px solid {tavily_color}; padding: 0.75rem 1rem; border-radius: 6px;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='font-weight: 600; color: white; font-size: 0.9rem;'>🔍 Tavily Search</span>
                <span style='color: {tavily_color}; font-weight: 700; font-size: 0.85rem;'>{'ACTIVE' if settings.tavily_api_key else 'INACTIVE'}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Divider
    st.markdown("<div style='height: 1px; background: rgba(102, 126, 234, 0.2); margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # Research Settings
    st.markdown("""
    <div style='margin: 1.5rem 0 1rem 0;'>
        <div style='font-size: 0.9rem; font-weight: 600; color: rgba(255,255,255,0.7); margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;'>
            🎛️ Research Settings
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    max_searches = st.slider(
        "Max Search Attempts", 
        min_value=1, 
        max_value=5, 
        value=settings.max_search_attempts,
        help="Number of web searches to perform"
    )
    max_results = st.slider(
        "Results per Search", 
        min_value=1, 
        max_value=5, 
        value=settings.max_search_results,
        help="Number of results to gather per search"
    )
    
    # Divider
    st.markdown("<div style='height: 1px; background: rgba(102, 126, 234, 0.2); margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown("""
    <div style='margin: 1.5rem 0 1rem 0;'>
        <div style='font-size: 0.9rem; font-weight: 600; color: rgba(255,255,255,0.7); margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;'>
            💻 Tech Stack
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='line-height: 2; color: rgba(255,255,255,0.8);'>
        <div style='margin-bottom: 0.5rem; display: flex; align-items: center;'>
            <span style='color: #667eea; margin-right: 0.5rem; font-size: 1.1rem;'>📊</span>
            <span style='font-size: 0.9rem;'>LangGraph</span>
        </div>
        <div style='margin-bottom: 0.5rem; display: flex; align-items: center;'>
            <span style='color: #667eea; margin-right: 0.5rem; font-size: 1.1rem;'>⚡</span>
            <span style='font-size: 0.9rem;'>Groq (Llama 3.3 70B)</span>
        </div>
        <div style='margin-bottom: 0.5rem; display: flex; align-items: center;'>
            <span style='color: #667eea; margin-right: 0.5rem; font-size: 1.1rem;'>🔍</span>
            <span style='font-size: 0.9rem;'>Tavily Search</span>
        </div>
        <div style='display: flex; align-items: center;'>
            <span style='color: #667eea; margin-right: 0.5rem; font-size: 1.1rem;'>🐍</span>
            <span style='font-size: 0.9rem;'>Python 3.13</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Session Statistics (if any history)
    if st.session_state.history:
        st.markdown("<div style='height: 1px; background: rgba(102, 126, 234, 0.2); margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='margin: 1.5rem 0 1rem 0;'>
            <div style='font-size: 0.9rem; font-weight: 600; color: rgba(255,255,255,0.7); margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;'>
                📊 Session Analytics
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        total_queries = len(st.session_state.history)
        total_cost = sum(h.get('cost', 0) for h in st.session_state.history)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Queries", total_queries, delta=None)
        with col2:
            st.metric("Total Cost", f"${total_cost:.4f}", delta=None)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Ask Your Research Question", unsafe_allow_html=True)
    query = st.text_area(
        "What would you like to research?",
        height=100,
        placeholder="Example: What is the current stock price of NVIDIA and why is it moving today?",
        label_visibility="collapsed"
    )
    research_button = st.button("🚀 Start Research", use_container_width=True, type="primary")

with col2:
    st.markdown("### 💡 Quick Examples", unsafe_allow_html=True)
    examples = [
        ("🏔️ Tourism trends in Nepal 2024", "Tourism trends in Nepal 2024"),
        ("🇳🇵 Current political situation in Nepal", "Current political situation in Nepal"),
        ("🧠 Latest AI breakthroughs in 2024", "Latest AI breakthroughs in 2024"),
        ("₿ Current Bitcoin price trends", "Current Bitcoin price trends"),
        ("🌍 Climate change latest news", "Climate change latest news")
    ]
    
    for label, text in examples:
        if st.button(label, key=text, use_container_width=True):
            st.session_state.current_query = text
            st.rerun()

# Use selected example
if st.session_state.current_query:
    query = st.session_state.current_query
    st.session_state.current_query = ""

# Research execution
if research_button and query:
    cost_tracker = CostTracker()
    logger = get_logger()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("⚙️ Initializing...")
        progress_bar.progress(10)
        
        agent = create_research_agent(cost_tracker)
        
        status_text.text("🔍 Searching the web...")
        progress_bar.progress(30)
        
        initial_state: AgentState = {
            "task": query,
            "search_results": [],
            "attempts": 0,
            "error": None,
            "final_report": None
        }
        
        result = agent.invoke(initial_state)
        progress_bar.progress(100)
        status_text.text("✅ Complete!")
        
        if result.get('error'):
            st.error(f"❌ Error: {result['error']}")
        else:
            st.divider()
            st.markdown("### Research Report", unsafe_allow_html=True)
            st.markdown(f'<div class="result-card">{result.get("final_report", "")}</div>', unsafe_allow_html=True)
            
            # Metrics
            st.divider()
            summary = cost_tracker.get_summary()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("💰 Cost", f"${summary['total_cost_usd']:.4f}")
            with col2:
                st.metric("🔍 Searches", summary['search_calls'])
            with col3:
                st.metric("🤖 LLM Calls", summary['llm_calls'])
            with col4:
                st.metric("🔢 Tokens", summary['total_tokens'])
            
            st.download_button(
                "📥 Download Report",
                result.get("final_report", ""),
                file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
            
            st.session_state.history.append({
                'timestamp': datetime.now().isoformat(),
                'query': query,
                'report': result.get("final_report", ""),
                'cost': summary['total_cost_usd']
            })
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# History
if st.session_state.history:
    st.divider()
    st.markdown("### Research History", unsafe_allow_html=True)
    
    for idx, item in enumerate(reversed(st.session_state.history[-5:])):
        with st.expander(f"🔍 {item['query'][:60]}... | {item['timestamp'][:10]}"):
            st.write(f"**Cost:** ${item['cost']:.4f}")
            st.markdown(item['report'])

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    Built with ❤️ using Python 3.13, LangGraph, Groq & Streamlit
</div>
""", unsafe_allow_html=True)
