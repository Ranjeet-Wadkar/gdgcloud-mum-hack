"""
Business Plan Generator Agent for the Research-to-Startup AI Agent Swarm.
Generates comprehensive pitch deck content from all previous agent outputs using Gemini AI.
"""

import json
from typing import Dict, List, Any
from utils.gemini_client import generate_business_plan_with_gemini

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

def generate_business_plan(research_data: Dict[str, Any], market_data: Dict[str, Any], 
                          feasibility_data: Dict[str, Any], stakeholder_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate comprehensive business plan and pitch deck content using Gemini AI.
    
    Args:
        research_data: Output from research analysis agent
        market_data: Output from market intelligence agent
        feasibility_data: Output from feasibility assessment agent
        stakeholder_data: Output from stakeholder matching agent
    
    Returns:
        Dictionary containing business plan and pitch deck content
    """
    # Prepare all agent outputs for Gemini
    all_agent_outputs = {
        'research_agent': research_data,
        'market_agent': market_data,
        'feasibility_agent': feasibility_data,
        'stakeholder_agent': stakeholder_data
    }
    
    # Use Gemini AI for business plan generation
    gemini_result = generate_business_plan_with_gemini(all_agent_outputs)
    
    # Create executive summary
    executive_summary = f"""
    Executive Summary:
    Our research presents {len(research_data.get('innovations', []))} breakthrough innovations 
    in {', '.join(research_data.get('application_domains', [])[:2])} with a total addressable market 
    of {market_data.get('TAM', 'N/A')}. Technology readiness level: {research_data.get('readiness_level', 0)}/9.
    """
    
    # Create key metrics
    key_metrics = {
        "TAM": market_data.get('TAM', 'N/A'),
        "SAM": market_data.get('SAM', 'N/A'),
        "SOM": market_data.get('SOM', 'N/A'),
        "TRL": research_data.get('readiness_level', 0),
        "Innovations": len(research_data.get('innovations', [])),
        "Domains": len(research_data.get('application_domains', []))
    }
    
    return {
        "slides": gemini_result.get("slides", []),
        "executive_summary": executive_summary,
        "key_metrics": key_metrics,
        "business_plan_summary": f"Generated comprehensive business plan with {len(gemini_result.get('slides', []))} pitch deck slides using Gemini AI."
    }

def create_pitch_deck_slides(research_data: Dict[str, Any], market_data: Dict[str, Any], 
                            feasibility_data: Dict[str, Any], stakeholder_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """Create structured pitch deck slides."""
    
    # Extract key data
    innovations = research_data.get('innovations', [])
    readiness_level = research_data.get('readiness_level', 0)
    domains = research_data.get('application_domains', [])
    tam = market_data.get('TAM', 'N/A')
    sam = market_data.get('SAM', 'N/A')
    som = market_data.get('SOM', 'N/A')
    trends = market_data.get('trends', [])
    competitors = market_data.get('competitors', [])
    roadmap = feasibility_data.get('roadmap', [])
    resources = feasibility_data.get('resources', {})
    risks = feasibility_data.get('risks', [])
    investor_matches = stakeholder_data.get('investor_matches', [])
    team_roles = stakeholder_data.get('team_roles', [])
    
    # Safely extract competitor names
    competitor_names = extract_competitor_names(competitors)
    
    slides = []
    
    # Slide 1: Problem & Opportunity
    slides.append({
        "title": "Problem & Opportunity",
        "content": f"""
        <h3>The Challenge</h3>
        <p>Current solutions in {', '.join(domains[:2])} face significant limitations in efficiency, scalability, and cost-effectiveness.</p>
        
        <h3>Our Opportunity</h3>
        <p>Our research introduces {len(innovations)} breakthrough innovations that address these critical gaps:</p>
        <ul>
            <li>{innovations[0] if innovations else 'Novel technical approach'}</li>
            <li>{innovations[1] if len(innovations) > 1 else 'Advanced methodology'}</li>
            <li>{innovations[2] if len(innovations) > 2 else 'Innovative solution'}</li>
        </ul>
        
        <h3>Market Size</h3>
        <p>Total Addressable Market: {tam}</p>
        <p>Serviceable Addressable Market: {sam}</p>
        <p>Serviceable Obtainable Market: {som}</p>
        """
    })
    
    # Slide 2: Core Innovation
    slides.append({
        "title": "Core Innovation",
        "content": f"""
        <h3>Technology Overview</h3>
        <p>Technology Readiness Level: {readiness_level}/9</p>
        <p>Primary Innovation: {innovations[0] if innovations else 'Breakthrough research methodology'}</p>
        
        <h3>Key Differentiators</h3>
        <ul>
            <li>Novel approach to {domains[0] if domains else 'target domain'}</li>
            <li>Superior performance compared to existing solutions</li>
            <li>Scalable and cost-effective implementation</li>
            <li>Strong intellectual property potential</li>
        </ul>
        
        <h3>Technical Advantages</h3>
        <p>Our solution offers significant improvements in efficiency, accuracy, and scalability over current market offerings.</p>
        """
    })
    
    # Slide 3: Market Landscape
    slides.append({
        "title": "Market Landscape",
        "content": f"""
        <h3>Market Opportunity</h3>
        <p>Total Addressable Market: {tam}</p>
        <p>Serviceable Addressable Market: {sam}</p>
        <p>Serviceable Obtainable Market: {som}</p>
        
        <h3>Key Market Trends</h3>
        <ul>
            {''.join([f'<li>{trend}</li>' for trend in trends[:4]])}
        </ul>
        
        <h3>Competitive Landscape</h3>
        <p>Major competitors: {', '.join(competitor_names[:3]) if competitor_names else 'Established market players'}</p>
        <p>Our competitive advantage: Research-driven innovation with clear technical differentiation</p>
        """
    })
    
    # Slide 4: Competitive Advantage
    slides.append({
        "title": "Competitive Advantage",
        "content": f"""
        <h3>Our Unique Value Proposition</h3>
        <ul>
            <li>Research-backed innovation with proven technical feasibility</li>
            <li>Clear path to commercialization with TRL {readiness_level}</li>
            <li>Strong market opportunity in {', '.join(domains[:2])}</li>
            <li>Experienced team with domain expertise</li>
        </ul>
        
        <h3>Competitive Moat</h3>
        <ul>
            <li>Intellectual property and technical know-how</li>
            <li>First-mover advantage in emerging market</li>
            <li>Strategic partnerships and collaborations</li>
            <li>Continuous innovation and R&D capabilities</li>
        </ul>
        
        <h3>Market Positioning</h3>
        <p>We position ourselves as the innovative leader in {domains[0] if domains else 'our target market'}, offering superior technology and market potential.</p>
        """
    })
    
    # Slide 5: Feasibility & Roadmap
    slides.append({
        "title": "Feasibility & Roadmap",
        "content": f"""
        <h3>Development Roadmap</h3>
        <ol>
            {''.join([f'<li>{milestone}</li>' for milestone in roadmap[:6]])}
        </ol>
        
        <h3>Resource Requirements</h3>
        <ul>
            <li>Timeline: {resources.get('time', 'N/A')}</li>
            <li>Team Size: {resources.get('team_size', 'N/A')}</li>
            <li>Budget: {resources.get('budget', 'N/A')}</li>
        </ul>
        
        <h3>Key Milestones</h3>
        <ul>
            <li>Technical validation and prototype development</li>
            <li>Market validation and user testing</li>
            <li>Product launch and initial market entry</li>
            <li>Scale and expansion</li>
        </ul>
        """
    })
    
    # Slide 6: Business Potential
    slides.append({
        "title": "Business Potential",
        "content": f"""
        <h3>Revenue Potential</h3>
        <p>Target market size: {som} with significant growth potential</p>
        <p>Revenue model: Technology licensing, product sales, and service offerings</p>
        
        <h3>Key Success Factors</h3>
        <ul>
            <li>Strong technical foundation and innovation</li>
            <li>Large and growing market opportunity</li>
            <li>Experienced team and strategic partnerships</li>
            <li>Clear path to profitability</li>
        </ul>
        
        <h3>Risk Mitigation</h3>
        <ul>
            {''.join([f'<li>{risk}</li>' for risk in risks[:4]])}
        </ul>
        """
    })
    
    # Slide 7: Next Steps & Investor Recommendations
    slides.append({
        "title": "Next Steps & Investor Recommendations",
        "content": f"""
        <h3>Immediate Next Steps</h3>
        <ul>
            <li>Secure initial funding for development</li>
            <li>Build core team with {', '.join(team_roles[:3])}</li>
            <li>Develop MVP and conduct market validation</li>
            <li>Establish strategic partnerships</li>
        </ul>
        
        <h3>Recommended Investors</h3>
        <ul>
            {''.join([f'<li>{inv.get("name", "Unknown")} - {inv.get("match_score", 0)*100:.0f}% match ({inv.get("stage", "Unknown")} stage)</li>' for inv in investor_matches[:3]])}
        </ul>
        
        <h3>Call to Action</h3>
        <p>We are seeking {resources.get('budget', 'funding')} to accelerate development and capture market opportunity. Join us in transforming research into commercial success.</p>
        """
    })
    
    return slides

def create_executive_summary(research_data: Dict[str, Any], market_data: Dict[str, Any], 
                           feasibility_data: Dict[str, Any], stakeholder_data: Dict[str, Any]) -> str:
    """Create executive summary of the business plan."""
    
    innovations = research_data.get('innovations', [])
    domains = research_data.get('application_domains', [])
    tam = market_data.get('TAM', 'N/A')
    feasibility_score = feasibility_data.get('feasibility_score', 0)
    investor_matches = stakeholder_data.get('investor_matches', [])
    
    summary = f"""
    <h3>Executive Summary</h3>
    <p>Our research introduces {len(innovations)} breakthrough innovations with strong commercial potential in {', '.join(domains[:2])}.</p>
    
    <p>Key innovations include {innovations[0] if innovations else 'novel technical approaches'} that address critical market needs. 
    We have identified {len(investor_matches)} potential investors with strong alignment to our project.</p>
    
    <p>We are seeking funding to accelerate development and capture this significant market opportunity, 
    with a clear path to commercialization and strong competitive advantages.</p>
    """
    
    return summary

def create_key_metrics(research_data: Dict[str, Any], market_data: Dict[str, Any], 
                      feasibility_data: Dict[str, Any], stakeholder_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create key business metrics."""
    
    return {
        "market_size": market_data.get('TAM', 'N/A'),
        "feasibility_score": feasibility_data.get('feasibility_score', 0),
        "technology_readiness": research_data.get('readiness_level', 0),
        "investor_matches": len(stakeholder_data.get('investor_matches', [])),
        "development_timeline": feasibility_data.get('resources', {}).get('time', 'N/A'),
        "funding_requirement": feasibility_data.get('resources', {}).get('budget', 'N/A'),
        "team_size": feasibility_data.get('resources', {}).get('team_size', 'N/A')
    }

def get_agent_voice_message(business_plan_data: Dict[str, Any]) -> str:
    """Generate human-readable voice message for visualization."""
    slides = business_plan_data.get('slides', [])
    metrics = business_plan_data.get('key_metrics', {})
    
    message = f"📋 Business Plan Generation Complete!\n\n"
    message += f"Generated comprehensive pitch deck with {len(slides)} slides covering all key aspects. "
    message += f"Market opportunity: {metrics.get('market_size', 'N/A')} with {metrics.get('feasibility_score', 0)}/10 feasibility score. "
    message += f"Ready for investor presentations and funding discussions."
    
    return message

def run_business_plan_agent(research_data: Dict[str, Any], market_data: Dict[str, Any], 
                           feasibility_data: Dict[str, Any], stakeholder_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function to run the business plan generator agent.
    
    Args:
        research_data: Output from research analysis agent
        market_data: Output from market intelligence agent
        feasibility_data: Output from feasibility assessment agent
        stakeholder_data: Output from stakeholder matching agent
    
    Returns:
        Complete business plan results with voice message
    """
    business_plan_result = generate_business_plan(research_data, market_data, feasibility_data, stakeholder_data)
    voice_message = get_agent_voice_message(business_plan_result)
    
    return {
        "agent_name": "Business Plan Generator Agent",
        "status": "completed",
        "output": business_plan_result,
        "voice_message": voice_message,
        "timestamp": "2024-01-01T10:20:00Z"
    }
