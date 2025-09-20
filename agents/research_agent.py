"""
Research Analysis Agent for the Research-to-Startup AI Agent Swarm.
Analyzes research papers and extracts key innovations, technical readiness, and applications using Gemini AI.
"""

import json
from typing import Dict, List, Any
from utils.gemini_client import analyze_research_with_gemini

def analyze_research_paper(text: str) -> Dict[str, Any]:
    """
    Analyze research paper and extract key information using Gemini AI.
    
    Args:
        text: Research paper text content
    
    Returns:
        Dictionary containing analysis results
    """
    # Use Gemini AI for analysis
    gemini_result = analyze_research_with_gemini(text)
    
    return {
        "innovations": gemini_result.get("innovations", []),
        "readiness_level": gemini_result.get("readiness_level", 0),
        "application_domains": gemini_result.get("application_domains", []),
        "technical_summary": gemini_result.get("technical_summary", ""),
        "analysis_summary": f"This paper introduces {len(gemini_result.get('innovations', []))} key innovations with TRL {gemini_result.get('readiness_level', 0)}, applicable to {len(gemini_result.get('application_domains', []))} domains."
    }

# Legacy functions removed - now using Gemini AI directly

def get_agent_voice_message(analysis_result: Dict[str, Any]) -> str:
    """Generate human-readable voice message for visualization."""
    innovations = analysis_result.get('innovations', [])
    readiness_level = analysis_result.get('readiness_level', 0)
    domains = analysis_result.get('application_domains', [])
    
    message = f"🔬 Research Analysis Complete!\n\n"
    message += f"This paper introduces {len(innovations)} key innovations with Technology Readiness Level {readiness_level}/9. "
    message += f"The research shows strong potential for applications in {', '.join(domains[:3])} industries. "
    message += f"Primary innovation: {innovations[0] if innovations else 'Multiple novel approaches'}."
    
    return message

def run_research_agent(text: str) -> Dict[str, Any]:
    """
    Main function to run the research analysis agent.
    
    Args:
        text: Research paper text content
    
    Returns:
        Complete analysis results with voice message
    """
    analysis_result = analyze_research_paper(text)
    voice_message = get_agent_voice_message(analysis_result)
    
    return {
        "agent_name": "Research Analysis Agent",
        "status": "completed",
        "output": analysis_result,
        "voice_message": voice_message,
        "timestamp": "2024-01-01T10:00:00Z"
    }
