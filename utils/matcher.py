"""
Investor matching algorithm for the Research-to-Startup AI Agent Swarm.
Scores investors based on project attributes and returns ranked matches.
"""

import json
from typing import List, Dict, Any

def load_investors() -> List[Dict[str, Any]]:
    """Load investor data from JSON file."""
    try:
        with open('data/investors.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def calculate_match_score(project_attributes: Dict[str, Any], investor: Dict[str, Any]) -> float:
    """
    Calculate match score between project and investor.
    
    Scoring criteria:
    - +0.4 if focus matches project domain
    - +0.3 if stage fits roadmap
    - +0.2 if geo matches
    - +0.1 if ticket covers funding needs
    """
    score = 0.0
    
    # Focus matching (0.4 points)
    project_domains = project_attributes.get('application_domains', [])
    investor_focus = investor.get('focus', [])
    
    focus_matches = set(project_domains) & set(investor_focus)
    if focus_matches:
        score += 0.4 * (len(focus_matches) / len(investor_focus))
    
    # Stage matching (0.3 points)
    project_stage = project_attributes.get('readiness_level', 0)
    investor_stage = investor.get('stage', '')
    
    # Map TRL levels to funding stages
    if project_stage <= 3 and investor_stage == 'Seed':
        score += 0.3
    elif 4 <= project_stage <= 6 and investor_stage in ['Seed', 'Series A']:
        score += 0.3
    elif project_stage >= 7 and investor_stage in ['Series A', 'Series B']:
        score += 0.3
    
    # Geographic matching (0.2 points)
    project_geo = project_attributes.get('geo', 'Global')
    investor_geo = investor.get('geo', 'Global')
    
    if investor_geo == 'Global' or project_geo == investor_geo:
        score += 0.2
    
    # Ticket size matching (0.1 points)
    project_funding_needs = project_attributes.get('funding_needs', 0)
    investor_ticket = investor.get('ticket_size', '')
    
    if investor_ticket and project_funding_needs > 0:
        # Parse ticket size range
        ticket_range = parse_ticket_size(investor_ticket)
        if ticket_range and ticket_range[0] <= project_funding_needs <= ticket_range[1]:
            score += 0.1
    
    return min(score, 1.0)  # Cap at 1.0

def parse_ticket_size(ticket_str: str) -> tuple:
    """Parse ticket size string to get min/max values."""
    try:
        # Remove $ and k/M suffixes, convert to numbers
        clean_str = ticket_str.replace('$', '').replace('k', '000').replace('M', '000000')
        if '-' in clean_str:
            min_val, max_val = clean_str.split('-')
            return (int(min_val), int(max_val))
        else:
            val = int(clean_str)
            return (val, val)
    except:
        return None

def find_investor_matches(project_attributes: Dict[str, Any], top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Find top investor matches for a project.
    
    Args:
        project_attributes: Dictionary containing project information
        top_n: Number of top matches to return
    
    Returns:
        List of investor dictionaries with match scores
    """
    investors = load_investors()
    
    # Calculate scores for all investors
    scored_investors = []
    for investor in investors:
        score = calculate_match_score(project_attributes, investor)
        if score > 0:  # Only include investors with some match
            investor_copy = investor.copy()
            investor_copy['match_score'] = round(score, 2)
            scored_investors.append(investor_copy)
    
    # Sort by score (descending) and return top N
    scored_investors.sort(key=lambda x: x['match_score'], reverse=True)
    return scored_investors[:top_n]

def get_team_recommendations(project_attributes: Dict[str, Any]) -> List[str]:
    """
    Suggest optimal team composition based on project attributes.
    
    Args:
        project_attributes: Dictionary containing project information
    
    Returns:
        List of recommended team roles
    """
    base_roles = ["Technical Founder", "Business Strategist"]
    
    # Add domain-specific roles based on application domains
    domains = project_attributes.get('application_domains', [])
    
    if any(domain in ['Healthcare', 'Biotech', 'Pharma'] for domain in domains):
        base_roles.append("Domain Expert (Healthcare)")
    elif any(domain in ['Sustainability', 'CleanTech', 'Energy'] for domain in domains):
        base_roles.append("Domain Expert (Climate)")
    elif any(domain in ['FinTech', 'Blockchain'] for domain in domains):
        base_roles.append("Domain Expert (Finance)")
    elif any(domain in ['EdTech', 'Education'] for domain in domains):
        base_roles.append("Domain Expert (Education)")
    else:
        base_roles.append("Domain Expert")
    
    # Add roles based on technical complexity
    readiness_level = project_attributes.get('readiness_level', 0)
    if readiness_level <= 3:
        base_roles.append("Research Scientist")
    elif readiness_level <= 6:
        base_roles.append("Product Manager")
    else:
        base_roles.append("Operations Manager")
    
    return base_roles
