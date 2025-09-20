"""
Pitch deck generation utilities for the Research-to-Startup AI Agent Swarm.
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
from typing import Dict, List, Any

def create_pitch_deck(agent_outputs: Dict[str, Any], output_path: str = "pitch_deck.pdf") -> str:
    """
    Generate a PDF pitch deck from agent outputs.
    
    Args:
        agent_outputs: Dictionary containing outputs from all agents
        output_path: Path to save the PDF file
    
    Returns:
        Path to the generated PDF file
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        leftIndent=20
    )
    
    # Title slide
    story.append(Paragraph("Research-to-Startup Pitch Deck", title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Transforming Research into Investment Opportunities", body_style))
    story.append(PageBreak())
    
    # Extract data from agent outputs
    research_data = agent_outputs.get('research_agent', {})
    market_data = agent_outputs.get('market_agent', {})
    feasibility_data = agent_outputs.get('feasibility_agent', {})
    stakeholder_data = agent_outputs.get('stakeholder_agent', {})
    business_plan_data = agent_outputs.get('business_plan_agent', {})
    
    # Slide 1: Problem & Opportunity
    story.append(Paragraph("1. Problem & Opportunity", heading_style))
    story.append(Spacer(1, 10))
    
    innovations = research_data.get('innovations', [])
    if innovations:
        story.append(Paragraph("Key Innovations:", body_style))
        for innovation in innovations[:3]:  # Top 3 innovations
            story.append(Paragraph(f"• {innovation}", body_style))
    
    application_domains = research_data.get('application_domains', [])
    if application_domains:
        story.append(Paragraph(f"Target Domains: {', '.join(application_domains)}", body_style))
    
    story.append(PageBreak())
    
    # Slide 2: Core Innovation
    story.append(Paragraph("2. Core Innovation", heading_style))
    story.append(Spacer(1, 10))
    
    readiness_level = research_data.get('readiness_level', 0)
    story.append(Paragraph(f"Technology Readiness Level: {readiness_level}/9", body_style))
    
    if innovations:
        story.append(Paragraph("Primary Innovation:", body_style))
        story.append(Paragraph(innovations[0], body_style))
    
    story.append(PageBreak())
    
    # Slide 3: Market Landscape
    story.append(Paragraph("3. Market Landscape", heading_style))
    story.append(Spacer(1, 10))
    
    tam = market_data.get('TAM', 'N/A')
    sam = market_data.get('SAM', 'N/A')
    som = market_data.get('SOM', 'N/A')
    
    story.append(Paragraph(f"Total Addressable Market (TAM): {tam}", body_style))
    story.append(Paragraph(f"Serviceable Addressable Market (SAM): {sam}", body_style))
    story.append(Paragraph(f"Serviceable Obtainable Market (SOM): {som}", body_style))
    
    trends = market_data.get('trends', [])
    if trends:
        story.append(Paragraph("Market Trends:", body_style))
        for trend in trends[:3]:
            story.append(Paragraph(f"• {trend}", body_style))
    
    story.append(PageBreak())
    
    # Slide 4: Competitive Advantage
    story.append(Paragraph("4. Competitive Advantage", heading_style))
    story.append(Spacer(1, 10))
    
    competitors = market_data.get('competitors', [])
    if competitors:
        story.append(Paragraph("Key Competitors:", body_style))
        for competitor in competitors[:3]:
            story.append(Paragraph(f"• {competitor}", body_style))
    
    story.append(Paragraph("Our Differentiators:", body_style))
    story.append(Paragraph("• Novel research-based approach", body_style))
    story.append(Paragraph("• Strong technical foundation", body_style))
    story.append(Paragraph("• Clear market opportunity", body_style))
    
    story.append(PageBreak())
    
    # Slide 5: Feasibility & Roadmap
    story.append(Paragraph("5. Feasibility & Roadmap", heading_style))
    story.append(Spacer(1, 10))
    
    roadmap = feasibility_data.get('roadmap', [])
    if roadmap:
        story.append(Paragraph("Development Roadmap:", body_style))
        for i, milestone in enumerate(roadmap, 1):
            story.append(Paragraph(f"{i}. {milestone}", body_style))
    
    resources = feasibility_data.get('resources', {})
    if resources:
        story.append(Paragraph(f"Resource Requirements:", body_style))
        story.append(Paragraph(f"• Time: {resources.get('time', 'N/A')}", body_style))
        story.append(Paragraph(f"• Team Size: {resources.get('team_size', 'N/A')}", body_style))
        story.append(Paragraph(f"• Budget: {resources.get('budget', 'N/A')}", body_style))
    
    story.append(PageBreak())
    
    # Slide 6: Business Potential
    story.append(Paragraph("6. Business Potential", heading_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Market Opportunity:", body_style))
    story.append(Paragraph(f"• Large addressable market ({tam})", body_style))
    story.append(Paragraph(f"• Growing market trends", body_style))
    story.append(Paragraph(f"• Clear monetization path", body_style))
    
    risks = feasibility_data.get('risks', [])
    if risks:
        story.append(Paragraph("Key Risks:", body_style))
        for risk in risks[:3]:
            story.append(Paragraph(f"• {risk}", body_style))
    
    story.append(PageBreak())
    
    # Slide 7: Next Steps & Investor Recommendations
    story.append(Paragraph("7. Next Steps & Investor Recommendations", heading_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Immediate Next Steps:", body_style))
    story.append(Paragraph("• Finalize technical prototype", body_style))
    story.append(Paragraph("• Conduct market validation", body_style))
    story.append(Paragraph("• Build founding team", body_style))
    story.append(Paragraph("• Secure initial funding", body_style))
    
    investor_matches = stakeholder_data.get('investor_matches', [])
    if investor_matches:
        story.append(Paragraph("Recommended Investors:", body_style))
        for i, investor in enumerate(investor_matches[:3], 1):
            name = investor.get('name', 'Unknown')
            score = investor.get('match_score', 0)
            stage = investor.get('stage', 'Unknown')
            ticket = investor.get('ticket_size', 'Unknown')
            story.append(Paragraph(f"{i}. {name} ({score*100:.0f}% match) - {stage} stage, {ticket}", body_style))
    
    # Build PDF
    doc.build(story)
    return output_path

def generate_deck_summary(agent_outputs: Dict[str, Any]) -> str:
    """
    Generate a text summary of the pitch deck for preview.
    
    Args:
        agent_outputs: Dictionary containing outputs from all agents
    
    Returns:
        Text summary of the pitch deck
    """
    research_data = agent_outputs.get('research_agent', {})
    market_data = agent_outputs.get('market_agent', {})
    stakeholder_data = agent_outputs.get('stakeholder_agent', {})
    
    summary = "## Pitch Deck Summary\n\n"
    
    # Key innovations
    innovations = research_data.get('innovations', [])
    if innovations:
        summary += f"**Key Innovation:** {innovations[0]}\n\n"
    
    # Market size
    tam = market_data.get('TAM', 'N/A')
    summary += f"**Market Size:** {tam}\n\n"
    
    # Top investor match
    investor_matches = stakeholder_data.get('investor_matches', [])
    if investor_matches:
        top_investor = investor_matches[0]
        summary += f"**Top Investor Match:** {top_investor.get('name', 'Unknown')} ({top_investor.get('match_score', 0)*100:.0f}% match)\n\n"
    
    # Team recommendations
    team_roles = stakeholder_data.get('team_roles', [])
    if team_roles:
        summary += f"**Recommended Team:** {', '.join(team_roles)}\n\n"
    
    return summary
