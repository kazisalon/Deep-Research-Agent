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

# Premium Theme with #2e79a7
st.markdown("""
<style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Premium Dark Background with Texture */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #0f1629 100%);
        background-attachment: fixed;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(46, 121, 167, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(46, 121, 167, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Reduce top spacing */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px;
    }
    
    /* Premium Header */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 10px rgba(46, 121, 167, 0.3);
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.65);
        margin-bottom: 3rem;
        font-weight: 400;
        letter-spacing: 0.02em;
    }
    
    /* Premium Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 1px solid rgba(46, 121, 167, 0.15);
        padding: 2rem;
        box-shadow: 
            0 8px 32px 0 rgba(0, 0, 0, 0.4),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(46, 121, 167, 0.3);
        box-shadow: 
            0 12px 48px 0 rgba(46, 121, 167, 0.15),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Premium Input Styling */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1.5px solid rgba(46, 121, 167, 0.25) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 1rem !important;
        padding: 1.25rem !important;
        transition: all 0.3s ease !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #2e79a7 !important;
        box-shadow: 
            0 0 0 3px rgba(46, 121, 167, 0.15) !important,
            inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        background: rgba(255, 255, 255, 0.06) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.35) !important;
    }
    
    /* Premium Primary Button */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #2e79a7 0%, #1e5c7a 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.875rem 2.5rem;
        border-radius: 10px;
        font-size: 1.05rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 4px 14px rgba(46, 121, 167, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button[kind="primary"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .stButton>button[kind="primary"]:hover::before {
        left: 100%;
    }
    
    .stButton>button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 6px 20px rgba(46, 121, 167, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        background: linear-gradient(135deg, #3589b8 0%, #2e79a7 100%);
    }
    
    .stButton>button[kind="primary"]:active {
        transform: translateY(0);
    }
    
    /* Example Buttons - Premium Style */
    div[data-testid="column"] .stButton>button {
        background: rgba(46, 121, 167, 0.08);
        border: 1px solid rgba(46, 121, 167, 0.25);
        color: rgba(255, 255, 255, 0.9);
        padding: 0.75rem 1.25rem;
        font-size: 0.95rem;
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    
    div[data-testid="column"] .stButton>button:hover {
        background: rgba(46, 121, 167, 0.15);
        border-color: rgba(46, 121, 167, 0.4);
        transform: translateX(4px);
        box-shadow: 
            0 4px 12px rgba(46, 121, 167, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Sidebar - Premium Dark */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 14, 35, 0.98) 0%, rgba(15, 22, 41, 0.98) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(46, 121, 167, 0.15);
        box-shadow: 2px 0 30px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar Text */
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: rgba(255, 255, 255, 0.95);
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: rgba(255, 255, 255, 0.8);
    }
    
    /* Premium Metrics */
    [data-testid="stMetricValue"] {
        color: #2e79a7;
        font-size: 1.75rem;
        font-weight: 700;
        text-shadow: 0 2px 8px rgba(46, 121, 167, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.7);
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* Premium Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #2e79a7 0%, #1e5c7a 100%);
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(46, 121, 167, 0.4);
    }
    
    .stProgress > div > div > div {
        background: rgba(46, 121, 167, 0.1);
        border-radius: 10px;
    }
    
    /* Premium Expander */
    .streamlit-expanderHeader {
        background: rgba(46, 121, 167, 0.08);
        border-radius: 10px;
        color: white;
        font-weight: 600;
        border: 1px solid rgba(46, 121, 167, 0.2);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(46, 121, 167, 0.12);
        border-color: rgba(46, 121, 167, 0.3);
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 0 0 10px 10px;
        border: 1px solid rgba(46, 121, 167, 0.1);
        border-top: none;
    }
    
    /* Result Card - Premium */
    .result-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(46, 121, 167, 0.2);
        margin: 1.5rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.8;
    }
    
    /* Download Button */
    .stDownloadButton>button {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #10b981;
        border-radius: 10px;
        padding: 0.75rem 1.75rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        background: rgba(16, 185, 129, 0.25);
        border-color: rgba(16, 185, 129, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
    }
    
    /* Premium Slider */
    .stSlider > div > div > div {
        background: rgba(46, 121, 167, 0.15);
    }
    
    .stSlider > div > div > div > div {
        background: #2e79a7;
        box-shadow: 0 2px 8px rgba(46, 121, 167, 0.4);
    }
    
    /* Premium Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(46, 121, 167, 0.3), 
            transparent
        );
        margin: 2rem 0;
    }
    
    /* Text Colors */
    p, span, div, label {
        color: rgba(255, 255, 255, 0.9);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: white;
        font-weight: 600;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.02);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(46, 121, 167, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(46, 121, 167, 0.5);
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
