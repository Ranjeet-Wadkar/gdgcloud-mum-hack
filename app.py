"""
Research-to-Startup AI Agent Swarm - Main Streamlit Application
Transforms research papers into investor-ready pitch decks using a sequential multi-agent pipeline.
"""

import streamlit as st
import json
import time
import logging
from typing import Dict, Any
import os
from datetime import datetime

# Import agents
from agents.research_agent import run_research_agent
from agents.market_agent import run_market_agent
from agents.feasibility_agent import run_feasibility_agent
from agents.stakeholder_agent import run_stakeholder_agent
from agents.business_plan_agent import run_business_plan_agent

# Import utilities
from utils.parser import extract_text_from_pdf, clean_text, validate_text_input
from utils.deck_generator import create_pitch_deck, generate_deck_summary
from utils.gemini_client import initialize_gemini

# Page configuration
st.set_page_config(
    page_title="Research-to-Startup AI Agent Swarm",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .agent-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .agent-completed {
        border-left-color: #2ca02c;
        background-color: #f0fff4;
    }
    .agent-processing {
        border-left-color: #ff7f0e;
        background-color: #fff8f0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .slide-preview {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'agent_outputs' not in st.session_state:
        st.session_state.agent_outputs = {}
    if 'research_text' not in st.session_state:
        st.session_state.research_text = ""
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    if 'ai_logs' not in st.session_state:
        st.session_state.ai_logs = []
    if 'gemini_mode' not in st.session_state:
        st.session_state.gemini_mode = "demo"

def display_header():
    """Display application header."""
    st.title("🚀 Research-to-Startup AI Agent Swarm")
    st.markdown("Transform research papers into investor-ready pitch decks using AI agents")
    
    # Display Gemini mode status
    if st.session_state.gemini_mode == "demo":
        st.warning("⚠️ Running in Demo Mode - Set GEMINI_API_KEY for real AI analysis")
    else:
        st.success("✅ Gemini AI Active - Real AI analysis enabled")
    
    st.markdown("---")

def display_ai_logs():
    """Display AI agent logs in a collapsible section."""
    if st.session_state.ai_logs:
        with st.expander("🤖 AI Agent Logs (Click to view)", expanded=False):
            for log in st.session_state.ai_logs:
                if log['type'] == 'call':
                    st.markdown(f"**🔵 {log['agent']} - API Call**")
                    st.code(f"Prompt: {log['prompt'][:200]}...", language='text')
                elif log['type'] == 'response':
                    st.markdown(f"**🟢 {log['agent']} - Response**")
                    st.code(f"Response: {log['response'][:200]}...", language='json')
                elif log['type'] == 'error':
                    st.markdown(f"**🔴 {log['agent']} - Error**")
                    st.error(log['error'])
                st.markdown("---")

def add_ai_log(agent_name: str, log_type: str, content: str, error: str = None):
    """Add a log entry to the AI logs."""
    log_entry = {
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'agent': agent_name,
        'type': log_type,
        'prompt': content if log_type == 'call' else None,
        'response': content if log_type == 'response' else None,
        'error': error if log_type == 'error' else None
    }
    st.session_state.ai_logs.append(log_entry)

def step1_upload_research():
    """Step 1: Upload and process research paper."""
    st.header("📄 Step 1: Upload Research Paper")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Upload Your Research Paper")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a PDF file or paste text directly",
            type=['pdf'],
            help="Upload a research paper in PDF format"
        )
        
        # Text input as alternative
        st.markdown("### Or Paste Text Directly")
        text_input = st.text_area(
            "Paste your research paper text here",
            height=200,
            placeholder="Paste the content of your research paper here..."
        )
        
        # Process input
        if uploaded_file is not None:
            try:
                with st.spinner("Extracting text from PDF..."):
                    research_text = extract_text_from_pdf(uploaded_file)
                    research_text = clean_text(research_text)
                    st.session_state.research_text = research_text
                    st.success("✅ PDF processed successfully!")
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")
                return False
                
        elif text_input:
            if validate_text_input(text_input):
                st.session_state.research_text = clean_text(text_input)
                st.success("✅ Text input validated!")
            else:
                st.error("❌ Text input is too short. Please provide more content.")
                return False
        else:
            st.info("👆 Please upload a PDF file or paste text to continue")
            return False
    
    with col2:
        st.markdown("### Instructions")
        st.markdown("""
        **Supported formats:**
        - PDF files
        - Plain text
        
        **What we analyze:**
        - Key innovations
        - Technical readiness
        - Market potential
        - Commercial feasibility
        - Investor matching
        """)
        
        if st.session_state.research_text:
            st.markdown("### Text Preview")
            preview_text = st.session_state.research_text[:500] + "..." if len(st.session_state.research_text) > 500 else st.session_state.research_text
            st.text_area("Extracted text preview:", preview_text, height=200, disabled=True)
    
    # Continue button
    if st.session_state.research_text:
        if st.button("🚀 Start AI Agent Analysis", type="primary", use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()
    
    return False

def step2_agent_visualization():
    """Step 2: Visualize AI agent processing."""
    st.header("🤖 Step 2: AI Agent Swarm Processing")
    
    # Agent definitions
    agents = [
        {"name": "Research Analysis Agent", "icon": "🔬", "description": "Extracting innovations and technical readiness"},
        {"name": "Market Intelligence Agent", "icon": "📊", "description": "Analyzing market potential and trends"},
        {"name": "Feasibility Assessment Agent", "icon": "⚙️", "description": "Evaluating commercial feasibility"},
        {"name": "Stakeholder Matching Agent", "icon": "🤝", "description": "Finding investors and team recommendations"},
        {"name": "Business Plan Generator Agent", "icon": "📋", "description": "Creating pitch deck and business plan"}
    ]
    
    # Display agent status
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Agent Swarm Status")
        
        # Process agents sequentially
        if not st.session_state.processing_complete:
            for i, agent in enumerate(agents):
                agent_key = f"agent_{i}"
                
                # Determine agent status
                if agent_key in st.session_state.agent_outputs:
                    status_class = "agent-completed"
                    status_icon = "✅"
                elif i == len([k for k in st.session_state.agent_outputs.keys() if k.startswith("agent_")]):
                    status_class = "agent-processing"
                    status_icon = "⚡"
                else:
                    status_class = "agent-card"
                    status_icon = "⏳"
                
                # Display agent card
                st.markdown(f"""
                <div class="agent-card {status_class}">
                    <h4>{status_icon} {agent['icon']} {agent['name']}</h4>
                    <p>{agent['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Process agents if not complete
        if not st.session_state.processing_complete:
            with st.spinner("Processing agents..."):
                # Run agents sequentially
                if "agent_0" not in st.session_state.agent_outputs:
                    # Research Agent
                    add_ai_log("Research Agent", "call", f"Analyzing research text: {st.session_state.research_text[:100]}...")
                    result = run_research_agent(st.session_state.research_text)
                    add_ai_log("Research Agent", "response", str(result))
                    st.session_state.agent_outputs["agent_0"] = result
                    time.sleep(1)  # Simulate processing time
                    st.rerun()
                
                elif "agent_1" not in st.session_state.agent_outputs:
                    # Market Agent
                    research_data = st.session_state.agent_outputs["agent_0"]["output"]
                    add_ai_log("Market Agent", "call", f"Analyzing market for innovations: {research_data.get('innovations', [])}")
                    result = run_market_agent(research_data)
                    add_ai_log("Market Agent", "response", str(result))
                    st.session_state.agent_outputs["agent_1"] = result
                    time.sleep(1)
                    st.rerun()
                
                elif "agent_2" not in st.session_state.agent_outputs:
                    # Feasibility Agent
                    research_data = st.session_state.agent_outputs["agent_0"]["output"]
                    market_data = st.session_state.agent_outputs["agent_1"]["output"]
                    add_ai_log("Feasibility Agent", "call", f"Assessing feasibility for TRL {research_data.get('readiness_level', 0)}")
                    result = run_feasibility_agent(research_data, market_data)
                    add_ai_log("Feasibility Agent", "response", str(result))
                    st.session_state.agent_outputs["agent_2"] = result
                    time.sleep(1)
                    st.rerun()
                
                elif "agent_3" not in st.session_state.agent_outputs:
                    # Stakeholder Agent
                    research_data = st.session_state.agent_outputs["agent_0"]["output"]
                    market_data = st.session_state.agent_outputs["agent_1"]["output"]
                    feasibility_data = st.session_state.agent_outputs["agent_2"]["output"]
                    add_ai_log("Stakeholder Agent", "call", f"Matching stakeholders for domains: {research_data.get('application_domains', [])}")
                    result = run_stakeholder_agent(research_data, market_data, feasibility_data)
                    add_ai_log("Stakeholder Agent", "response", str(result))
                    st.session_state.agent_outputs["agent_3"] = result
                    time.sleep(1)
                    st.rerun()
                
                elif "agent_4" not in st.session_state.agent_outputs:
                    # Business Plan Agent
                    research_data = st.session_state.agent_outputs["agent_0"]["output"]
                    market_data = st.session_state.agent_outputs["agent_1"]["output"]
                    feasibility_data = st.session_state.agent_outputs["agent_2"]["output"]
                    stakeholder_data = st.session_state.agent_outputs["agent_3"]["output"]
                    add_ai_log("Business Plan Agent", "call", "Generating comprehensive business plan and pitch deck")
                    result = run_business_plan_agent(research_data, market_data, feasibility_data, stakeholder_data)
                    add_ai_log("Business Plan Agent", "response", str(result))
                    st.session_state.agent_outputs["agent_4"] = result
                    st.session_state.processing_complete = True
                    st.rerun()
    
    with col2:
        st.markdown("### Agent Messages")
        
        # Display agent voice messages
        for i, agent in enumerate(agents):
            agent_key = f"agent_{i}"
            if agent_key in st.session_state.agent_outputs:
                agent_data = st.session_state.agent_outputs[agent_key]
                voice_message = agent_data.get("voice_message", "")
                
                st.markdown(f"""
                <div class="metric-card">
                    <h5>{agent['icon']} {agent['name']}</h5>
                    <p>{voice_message}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Display AI logs
    display_ai_logs()
    
    # Continue to insights
    if st.session_state.processing_complete:
        if st.button("📊 View Insights & Generate Pitch Deck", type="primary", use_container_width=True):
            st.session_state.current_step = 3
            st.rerun()

def step3_insights_review():
    """Step 3: Review insights and generate pitch deck."""
    st.header("📊 Step 3: Insights Review & Pitch Deck Generation")
    
    if not st.session_state.processing_complete:
        st.error("Please complete agent processing first.")
        return
    
    # Extract agent outputs
    research_data = st.session_state.agent_outputs["agent_0"]["output"]
    market_data = st.session_state.agent_outputs["agent_1"]["output"]
    feasibility_data = st.session_state.agent_outputs["agent_2"]["output"]
    stakeholder_data = st.session_state.agent_outputs["agent_3"]["output"]
    business_plan_data = st.session_state.agent_outputs["agent_4"]["output"]
    
    # Create tabs for different insights
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔬 Research", "📊 Market", "⚙️ Feasibility", "🤝 Stakeholders", "📋 Pitch Deck"])
    
    with tab1:
        st.markdown("### Research Analysis Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Key Innovations")
            innovations = research_data.get('innovations', [])
            for i, innovation in enumerate(innovations, 1):
                st.markdown(f"{i}. {innovation}")
        
        with col2:
            st.markdown("#### Technical Readiness")
            readiness_level = research_data.get('readiness_level', 0)
            st.metric("Technology Readiness Level", f"{readiness_level}/9")
            
            st.markdown("#### Application Domains")
            domains = research_data.get('application_domains', [])
            for domain in domains:
                st.markdown(f"• {domain}")
    
    with tab2:
        st.markdown("### Market Intelligence Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Addressable Market", market_data.get('TAM', 'N/A'))
        with col2:
            st.metric("Serviceable Addressable Market", market_data.get('SAM', 'N/A'))
        with col3:
            st.metric("Serviceable Obtainable Market", market_data.get('SOM', 'N/A'))
        
        st.markdown("#### Market Trends")
        trends = market_data.get('trends', [])
        for trend in trends:
            st.markdown(f"• {trend}")
        
        st.markdown("#### Key Competitors")
        competitors = market_data.get('competitors', [])
        for competitor in competitors:
            st.markdown(f"• {competitor}")
    
    with tab3:
        st.markdown("### Feasibility Assessment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            feasibility_score = feasibility_data.get('feasibility_score', 0)
            st.metric("Feasibility Score", f"{feasibility_score}/10")
            
            st.markdown("#### Resource Requirements")
            resources = feasibility_data.get('resources', {})
            st.markdown(f"**Timeline:** {resources.get('time', 'N/A')}")
            st.markdown(f"**Team Size:** {resources.get('team_size', 'N/A')}")
            st.markdown(f"**Budget:** {resources.get('budget', 'N/A')}")
        
        with col2:
            st.markdown("#### Development Roadmap")
            roadmap = feasibility_data.get('roadmap', [])
            for i, milestone in enumerate(roadmap, 1):
                st.markdown(f"{i}. {milestone}")
            
            st.markdown("#### Key Risks")
            risks = feasibility_data.get('risks', [])
            for risk in risks[:5]:  # Show top 5 risks
                st.markdown(f"• {risk}")
    
    with tab4:
        st.markdown("### Stakeholder & Investor Matching")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Recommended Team")
            team_roles = stakeholder_data.get('team_roles', [])
            for role in team_roles:
                st.markdown(f"• {role}")
        
        with col2:
            st.markdown("#### Top Investor Matches")
            investor_matches = stakeholder_data.get('investor_matches', [])
            for i, investor in enumerate(investor_matches[:3], 1):
                name = investor.get('name', 'Unknown')
                score = investor.get('match_score', 0)
                stage = investor.get('stage', 'Unknown')
                st.markdown(f"{i}. **{name}** ({score*100:.0f}% match) - {stage}")
    
    with tab5:
        st.markdown("### Pitch Deck Preview")
        
        # Generate deck summary
        all_outputs = {
            'research_agent': research_data,
            'market_agent': market_data,
            'feasibility_agent': feasibility_data,
            'stakeholder_agent': stakeholder_data,
            'business_plan_agent': business_plan_data
        }
        
        deck_summary = generate_deck_summary(all_outputs)
        st.markdown(deck_summary)
        
        # Show first few slides
        slides = business_plan_data.get('slides', [])
        if slides:
            st.markdown("#### Sample Slides")
            for i, slide in enumerate(slides[:3], 1):  # Show first 3 slides
                st.markdown(f"""
                <div class="slide-preview">
                    <h4>Slide {i}: {slide['title']}</h4>
                    {slide['content']}
                </div>
                """, unsafe_allow_html=True)
        
        # Download button
        if st.button("📥 Download Full Pitch Deck (PDF)", type="primary"):
            with st.spinner("Generating PDF..."):
                try:
                    pdf_path = create_pitch_deck(all_outputs)
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="Download PDF",
                            data=pdf_file.read(),
                            file_name="pitch_deck.pdf",
                            mime="application/pdf"
                        )
                    st.success("✅ Pitch deck generated successfully!")
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Back to Agent Processing"):
            st.session_state.current_step = 2
            st.rerun()
    
    with col3:
        if st.button("🔄 Start New Analysis", type="primary"):
            # Reset session state
            st.session_state.current_step = 1
            st.session_state.agent_outputs = {}
            st.session_state.research_text = ""
            st.session_state.processing_complete = False
            st.rerun()

def main():
    """Main application function."""
    initialize_session_state()
    display_header()
    
    # Initialize Gemini
    try:
        model = initialize_gemini()
        if model:
            st.session_state.gemini_mode = "production"
            st.success("✅ Gemini AI initialized successfully!")
        else:
            st.session_state.gemini_mode = "demo"
            st.warning("⚠️ Running in demo mode. Set GEMINI_API_KEY for full AI features.")
            st.info("Get your API key from: https://makersuite.google.com/app/apikey")
    except Exception as e:
        st.session_state.gemini_mode = "demo"
        st.warning(f"⚠️ Running in demo mode. Set GEMINI_API_KEY for full AI features.")
        st.info("Get your API key from: https://makersuite.google.com/app/apikey")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### Progress")
        steps = ["Upload Research", "Agent Processing", "Insights & Deck"]
        for i, step in enumerate(steps, 1):
            if i < st.session_state.current_step:
                st.markdown(f"✅ {step}")
            elif i == st.session_state.current_step:
                st.markdown(f"🔄 {step}")
            else:
                st.markdown(f"⏳ {step}")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This AI Agent Swarm transforms research papers into investor-ready pitch decks through a sequential multi-agent pipeline.
        
        **Agents:**
        1. 🔬 Research Analysis
        2. 📊 Market Intelligence  
        3. ⚙️ Feasibility Assessment
        4. 🤝 Stakeholder Matching
        5. 📋 Business Plan Generator
        """)
    
    # Main content based on current step
    if st.session_state.current_step == 1:
        step1_upload_research()
    elif st.session_state.current_step == 2:
        step2_agent_visualization()
    elif st.session_state.current_step == 3:
        step3_insights_review()

if __name__ == "__main__":
    main()
