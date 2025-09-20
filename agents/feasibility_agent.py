"""
Feasibility Assessment Agent for the Research-to-Startup AI Agent Swarm.
Assesses technical feasibility, resource requirements, and development roadmap using Gemini AI.
"""

import json
from typing import Dict, List, Any
from utils.gemini_client import assess_feasibility_with_gemini

def assess_feasibility(research_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assess feasibility of commercializing the research using Gemini AI.
    
    Args:
        research_data: Output from research analysis agent
        market_data: Output from market intelligence agent
    
    Returns:
        Dictionary containing feasibility assessment results
    """
    # Use Gemini AI for feasibility assessment
    gemini_result = assess_feasibility_with_gemini(research_data, market_data)
    
    return {
        "roadmap": gemini_result.get("roadmap", []),
        "resources": gemini_result.get("resources", {}),
        "risks": gemini_result.get("risks", []),
        "feasibility_score": gemini_result.get("feasibility_score", 5),
        "feasibility_summary": f"Project feasibility score: {gemini_result.get('feasibility_score', 5)}/10 with {len(gemini_result.get('roadmap', []))} development phases."
    }

# Legacy functions removed - now using Gemini AI directly

def get_agent_voice_message(feasibility_data: Dict[str, Any]) -> str:
    """Generate human-readable voice message for visualization."""
    score = feasibility_data.get('feasibility_score', 0)
    resources = feasibility_data.get('resources', {})
    roadmap = feasibility_data.get('roadmap', [])
    
    message = f"⚙️ Feasibility Assessment Complete!\n\n"
    message += f"Project feasibility score: {score}/10. "
    message += f"Development timeline: {resources.get('time', 'N/A')} with {resources.get('team_size', 'N/A')} team. "
    message += f"Budget requirement: {resources.get('budget', 'N/A')}. "
    message += f"Roadmap includes {len(roadmap)} key milestones."
    
    return message

def run_feasibility_agent(research_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function to run the feasibility assessment agent.
    
    Args:
        research_data: Output from research analysis agent
        market_data: Output from market intelligence agent
    
    Returns:
        Complete feasibility assessment results with voice message
    """
    feasibility_result = assess_feasibility(research_data, market_data)
    voice_message = get_agent_voice_message(feasibility_result)
    
    return {
        "agent_name": "Feasibility Assessment Agent",
        "status": "completed",
        "output": feasibility_result,
        "voice_message": voice_message,
        "timestamp": "2024-01-01T10:10:00Z"
    }
