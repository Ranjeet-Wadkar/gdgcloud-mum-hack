"""
Market Intelligence Agent for the Research-to-Startup AI Agent Swarm.
Analyzes market potential, trends, and competitive landscape using Gemini AI.
"""

import json
from typing import Dict, List, Any
from utils.gemini_client import analyze_market_with_gemini

def extract_market_value(market_data: Any) -> str:
    """
    Extract the actual market value from complex nested structures.
    
    Args:
        market_data: Can be a string, dict, or other type
    
    Returns:
        String representation of the market value
    """
    if isinstance(market_data, str):
        return market_data
    elif isinstance(market_data, dict):
        # If it's a dict with 'value' key, extract that
        if 'value' in market_data:
            return str(market_data['value'])
        # If it's a dict with multiple market segments, try to get the first one
        elif len(market_data) > 0:
            first_key = list(market_data.keys())[0]
            first_value = market_data[first_key]
            if isinstance(first_value, dict) and 'value' in first_value:
                return str(first_value['value'])
            else:
                return str(first_value)
        else:
            return "N/A"
    else:
        return str(market_data) if market_data is not None else "N/A"

def extract_competitor_names(competitors: List[Any]) -> List[str]:
    """
    Safely extract competitor names from a list that might contain strings or dictionaries.
    
    Args:
        competitors: List that might contain strings or dictionaries with competitor info
    
    Returns:
        List of competitor names as strings
    """
    competitor_names = []
    for competitor in competitors:
        if isinstance(competitor, str):
            competitor_names.append(competitor)
        elif isinstance(competitor, dict):
            # Try common keys for competitor names
            name = competitor.get('name') or competitor.get('company') or competitor.get('competitor')
            if name:
                competitor_names.append(str(name))
        else:
            # Convert any other type to string
            competitor_names.append(str(competitor))
    return competitor_names

def analyze_market_intelligence(research_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze market potential based on research innovations using Gemini AI.
    
    Args:
        research_data: Output from research analysis agent
    
    Returns:
        Dictionary containing market analysis results
    """
    innovations = research_data.get('innovations', [])
    domains = research_data.get('application_domains', [])
    
    # Use Gemini AI for market analysis
    gemini_result = analyze_market_with_gemini(innovations, domains)
    
    # Extract actual values from potentially complex structures
    tam_value = extract_market_value(gemini_result.get("TAM", "N/A"))
    sam_value = extract_market_value(gemini_result.get("SAM", "N/A"))
    som_value = extract_market_value(gemini_result.get("SOM", "N/A"))
    
    return {
        "TAM": tam_value,
        "SAM": sam_value,
        "SOM": som_value,
        "trends": gemini_result.get("trends", []),
        "competitors": gemini_result.get("competitors", []),
        "market_summary": f"Total addressable market of {tam_value} with {len(gemini_result.get('trends', []))} key trends and {len(gemini_result.get('competitors', []))} major competitors."
    }

# Legacy functions removed - now using Gemini AI directly

def get_agent_voice_message(market_data: Dict[str, Any]) -> str:
    """Generate human-readable voice message for visualization."""
    tam = market_data.get('TAM', 'N/A')
    trends = market_data.get('trends', [])
    competitors = market_data.get('competitors', [])
    
    # Safely extract competitor names
    competitor_names = extract_competitor_names(competitors)
    
    message = f"📊 Market Analysis Complete!\n\n"
    message += f"The global market opportunity is estimated at {tam} with strong growth potential. "
    message += f"Key trends include {trends[0] if trends else 'digital transformation'} and {trends[1] if len(trends) > 1 else 'sustainability'}. "
    message += f"Major competitors include {', '.join(competitor_names[:2]) if competitor_names else 'established players'}."
    
    return message

def run_market_agent(research_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function to run the market intelligence agent.
    
    Args:
        research_data: Output from research analysis agent
    
    Returns:
        Complete market analysis results with voice message
    """
    market_result = analyze_market_intelligence(research_data)
    voice_message = get_agent_voice_message(market_result)
    
    return {
        "agent_name": "Market Intelligence Agent",
        "status": "completed",
        "output": market_result,
        "voice_message": voice_message,
        "timestamp": "2024-01-01T10:05:00Z"
    }
