"""
Stakeholder & Investor Matching Agent for the Research-to-Startup AI Agent Swarm.
Matches projects with suitable investors and recommends team composition.
"""

import json
from typing import Dict, List, Any
from utils.matcher import find_investor_matches, get_team_recommendations

def match_stakeholders(research_data: Dict[str, Any], market_data: Dict[str, Any], feasibility_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Match project with suitable investors and recommend team composition.
    
    Args:
        research_data: Output from research analysis agent
        market_data: Output from market intelligence agent
        feasibility_data: Output from feasibility assessment agent
    
    Returns:
        Dictionary containing stakeholder matching results
    """
    # Prepare project attributes for matching
    project_attributes = {
        'application_domains': research_data.get('application_domains', []),
        'readiness_level': research_data.get('readiness_level', 0),
        'funding_needs': feasibility_data.get('resources', {}).get('funding_needs', 0),
        'geo': 'Global'  # Default to global, could be extracted from research
    }
    
    # Find investor matches
    investor_matches = find_investor_matches(project_attributes, top_n=5)
    
    # Get team recommendations
    team_roles = get_team_recommendations(project_attributes)
    
    # Calculate match statistics
    total_investors = len(investor_matches)
    high_matches = len([inv for inv in investor_matches if inv.get('match_score', 0) >= 0.7])
    
    return {
        "team_roles": team_roles,
        "investor_matches": investor_matches,
        "match_statistics": {
            "total_matches": total_investors,
            "high_confidence_matches": high_matches,
            "average_match_score": sum(inv.get('match_score', 0) for inv in investor_matches) / max(total_investors, 1)
        },
        "stakeholder_summary": f"Found {total_investors} potential investors with {high_matches} high-confidence matches. Recommended team: {len(team_roles)} key roles."
    }

def get_agent_voice_message(stakeholder_data: Dict[str, Any]) -> str:
    """Generate human-readable voice message for visualization."""
    investor_matches = stakeholder_data.get('investor_matches', [])
    team_roles = stakeholder_data.get('team_roles', [])
    stats = stakeholder_data.get('match_statistics', {})
    
    message = f"🤝 Stakeholder Matching Complete!\n\n"
    
    if investor_matches:
        top_investor = investor_matches[0]
        message += f"Top investor match: {top_investor.get('name', 'Unknown')} with {top_investor.get('match_score', 0)*100:.0f}% fit. "
        message += f"Found {stats.get('total_matches', 0)} total matches including {stats.get('high_confidence_matches', 0)} high-confidence options. "
    else:
        message += "No immediate investor matches found, but project shows potential for future funding rounds. "
    
    message += f"Recommended team composition: {', '.join(team_roles[:3])} and {len(team_roles)-3} additional roles."
    
    return message

def run_stakeholder_agent(research_data: Dict[str, Any], market_data: Dict[str, Any], feasibility_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function to run the stakeholder matching agent.
    
    Args:
        research_data: Output from research analysis agent
        market_data: Output from market intelligence agent
        feasibility_data: Output from feasibility assessment agent
    
    Returns:
        Complete stakeholder matching results with voice message
    """
    stakeholder_result = match_stakeholders(research_data, market_data, feasibility_data)
    voice_message = get_agent_voice_message(stakeholder_result)
    
    return {
        "agent_name": "Stakeholder & Investor Matching Agent",
        "status": "completed",
        "output": stakeholder_result,
        "voice_message": voice_message,
        "timestamp": "2024-01-01T10:15:00Z"
    }
