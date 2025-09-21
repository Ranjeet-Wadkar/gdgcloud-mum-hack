"""
Enhanced Pitch deck generation utilities for the Research-to-Startup AI Agent Swarm.
Uses ReportLab's BaseDocTemplate for professional, colorful, and presentable pitch decks.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether, NextPageTemplate
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import io
import os
from typing import Dict, List, Any

class PitchDeckTemplate(BaseDocTemplate):
    """Custom BaseDocTemplate for creating beautiful pitch decks."""
    
    def __init__(self, filename, **kwargs):
        super().__init__(filename, pagesize=A4, **kwargs)
        self._define_page_templates()
        self._define_styles()
    
    def _define_page_templates(self):
        """Define different page templates for various slide types."""
        # Main content frame
        main_frame = Frame(
            1*inch, 1.5*inch, 6.5*inch, 9*inch,
            leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0,
            id='main'
        )
        
        # Title slide frame (centered)
        title_frame = Frame(
            0.5*inch, 2*inch, 7*inch, 8*inch,
            leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0,
            id='title'
        )
        
        # Chart frame (for data visualization slides)
        chart_frame = Frame(
            0.5*inch, 1*inch, 7*inch, 7*inch,
            leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0,
            id='chart'
        )
        
        # Define page templates
        main_template = PageTemplate(
            id='Main', 
            frames=[main_frame], 
            onPage=self._add_header_footer
        )
        
        title_template = PageTemplate(
            id='Title', 
            frames=[title_frame], 
            onPage=self._add_title_footer
        )
        
        chart_template = PageTemplate(
            id='Chart', 
            frames=[chart_frame], 
            onPage=self._add_chart_footer
        )
        
        self.addPageTemplates([main_template, title_template, chart_template])
    
    def _define_styles(self):
        """Define custom styles for the pitch deck."""
        self.styles = getSampleStyleSheet()
        
        # Title slide style
        self.styles.add(ParagraphStyle(
            name='TitleSlide',
            parent=self.styles['Title'],
            fontSize=36,
            spaceAfter=30,
            textColor=colors.HexColor('#1a365d'),  # Dark blue
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=18,
            spaceAfter=20,
            textColor=colors.HexColor('#2d3748'),  # Gray
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Slide title style
        self.styles.add(ParagraphStyle(
            name='SlideTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            spaceAfter=20,
            textColor=colors.HexColor('#1a365d'),
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=colors.HexColor('#e2e8f0'),
            borderPadding=10,
            backColor=colors.HexColor('#f7fafc')
        ))
        
        # Section heading style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=20,
            spaceAfter=15,
            textColor=colors.HexColor('#2b6cb0'),  # Blue
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBodyText',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#2d3748'),
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leftIndent=0
        ))
        
        # Bullet point style
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.HexColor('#2d3748'),
            alignment=TA_LEFT,
            fontName='Helvetica',
            leftIndent=20,
            bulletIndent=10
        ))
        
        # Highlight style
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['Normal'],
            fontSize=16,
            spaceAfter=15,
            textColor=colors.HexColor('#e53e3e'),  # Red
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#fed7d7'),
            borderWidth=1,
            borderColor=colors.HexColor('#feb2b2'),
            borderPadding=8
        ))
    
    def _add_header_footer(self, canvas, doc):
        """Add header and footer to main content pages."""
        canvas.saveState()
        
        # Header background
        canvas.setFillColor(colors.HexColor('#1a365d'))
        canvas.rect(0, 10.5*inch, 8.5*inch, 0.5*inch, fill=1, stroke=0)
        
        # Header text
        canvas.setFillColor(colors.white)
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(1*inch, 10.7*inch, "Resa Paper to Pitch")
        
        # Footer
        canvas.setFillColor(colors.HexColor('#718096'))
        canvas.setFont('Helvetica', 10)
        canvas.drawString(1*inch, 0.5*inch, f"Page {doc.page}")
        canvas.drawRightString(7.5*inch, 0.5*inch, "Pitch Deck 2024")
        
        canvas.restoreState()
    
    def _add_title_footer(self, canvas, doc):
        """Add footer to title pages."""
        canvas.saveState()
        canvas.setFillColor(colors.HexColor('#718096'))
        canvas.setFont('Helvetica', 10)
        canvas.drawString(1*inch, 0.5*inch, f"Page {doc.page}")
        canvas.restoreState()
    
    def _add_chart_footer(self, canvas, doc):
        """Add footer to chart pages."""
        canvas.saveState()
        canvas.setFillColor(colors.HexColor('#718096'))
        canvas.setFont('Helvetica', 10)
        canvas.drawString(1*inch, 0.5*inch, f"Page {doc.page}")
        canvas.restoreState()


def create_pitch_deck(agent_outputs: Dict[str, Any], output_path: str = "pitch_deck.pdf") -> str:
    """
    Generate a beautiful PDF pitch deck from agent outputs using BaseDocTemplate.
    
    Args:
        agent_outputs: Dictionary containing outputs from all agents
        output_path: Path to save the PDF file
    
    Returns:
        Path to the generated PDF file
    """
    doc = PitchDeckTemplate(output_path)
    story = []
    
    # Extract data from agent outputs
    research_data = agent_outputs.get('research_agent', {})
    market_data = agent_outputs.get('market_agent', {})
    feasibility_data = agent_outputs.get('feasibility_agent', {})
    stakeholder_data = agent_outputs.get('stakeholder_agent', {})
    business_plan_data = agent_outputs.get('business_plan_agent', {})
    
    # Slide 1: Title Slide
    story.append(NextPageTemplate('Title'))
    story.append(PageBreak())
    story.append(Paragraph("Resa", doc.styles['TitleSlide']))
    story.append(Paragraph("Paper to Pitch", doc.styles['TitleSlide']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Transforming Research into Investment Opportunities", doc.styles['Subtitle']))
    story.append(Spacer(1, 1*inch))
    
    # Add key metrics in a table
    innovations = research_data.get('innovations', [])
    tam = market_data.get('TAM', 'N/A')
    feasibility_score = feasibility_data.get('feasibility_score', 0)
    
    metrics_data = [
        ['Key Innovation', 'Market Size', 'Feasibility Score'],
        [innovations[0][:50] + '...' if innovations else 'N/A', tam, f"{feasibility_score}/10"]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2d3748')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
    ]))
    story.append(metrics_table)
    
    # Slide 2: Problem & Opportunity
    story.append(NextPageTemplate('Main'))
    story.append(PageBreak())
    story.append(Paragraph("1. Problem & Opportunity", doc.styles['SlideTitle']))
    story.append(Spacer(1, 0.3*inch))
    
    # Problem statement
    story.append(Paragraph("The Challenge", doc.styles['SectionHeading']))
    story.append(Paragraph(
        "Research innovations often remain confined to academic papers, missing the opportunity to create real-world impact and commercial value. Our AI Agent Swarm bridges this gap by transforming cutting-edge research into investor-ready business opportunities.",
        doc.styles['CustomBodyText']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # Key innovations
    if innovations:
        story.append(Paragraph("Key Innovations Identified:", doc.styles['SectionHeading']))
        for i, innovation in enumerate(innovations[:3], 1):
            story.append(Paragraph(f"{i}. {innovation}", doc.styles['BulletPoint']))
    
    # Application domains
    application_domains = research_data.get('application_domains', [])
    if application_domains:
        story.append(Paragraph("Target Application Domains:", doc.styles['SectionHeading']))
        for domain in application_domains:
            story.append(Paragraph(f"• {domain}", doc.styles['BulletPoint']))
    
    # Slide 3: Core Innovation & Technology
    story.append(PageBreak())
    story.append(Paragraph("2. Core Innovation & Technology", doc.styles['SlideTitle']))
    story.append(Spacer(1, 0.3*inch))
    
    # Technology readiness
    readiness_level = research_data.get('readiness_level', 0)
    story.append(Paragraph("Technology Readiness Assessment", doc.styles['SectionHeading']))
    
    # Create a visual TRL indicator
    trl_data = [
        ['TRL Level', 'Description', 'Status'],
        ['1-3', 'Basic Research', '✅ Completed' if readiness_level >= 3 else '⏳ In Progress'],
        ['4-6', 'Technology Development', '✅ Completed' if readiness_level >= 6 else '⏳ In Progress'],
        ['7-9', 'System Integration & Deployment', '✅ Completed' if readiness_level >= 9 else '⏳ In Progress']
    ]
    
    trl_table = Table(trl_data, colWidths=[1.5*inch, 3*inch, 1.5*inch])
    trl_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#38a169')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fff4')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2d3748')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#c6f6d5')),
    ]))
    story.append(trl_table)
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Current TRL Level: <b>{readiness_level}/9</b>", doc.styles['Highlight']))
    
    # Slide 4: Market Landscape
    story.append(PageBreak())
    story.append(Paragraph("3. Market Landscape & Opportunity", doc.styles['SlideTitle']))
    story.append(Spacer(1, 0.3*inch))
    
    # Market size metrics
    tam = market_data.get('TAM', 'N/A')
    sam = market_data.get('SAM', 'N/A')
    som = market_data.get('SOM', 'N/A')
    
    market_data_table = [
        ['Market Segment', 'Size', 'Description'],
        ['Total Addressable Market (TAM)', tam, 'Total market demand'],
        ['Serviceable Addressable Market (SAM)', sam, 'Realistic market opportunity'],
        ['Serviceable Obtainable Market (SOM)', som, 'Achievable market share']
    ]
    
    market_table = Table(market_data_table, colWidths=[2.5*inch, 1.5*inch, 2.5*inch])
    market_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#805ad5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#faf5ff')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2d3748')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d6bcfa')),
    ]))
    story.append(market_table)
    
    # Market trends
    trends = market_data.get('trends', [])
    if trends:
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("Key Market Trends:", doc.styles['SectionHeading']))
        for trend in trends[:3]:
            story.append(Paragraph(f"• {trend}", doc.styles['BulletPoint']))
    
    # Slide 5: Competitive Analysis
    story.append(PageBreak())
    story.append(Paragraph("4. Competitive Analysis", doc.styles['SlideTitle']))
    story.append(Spacer(1, 0.3*inch))
    
    competitors = market_data.get('competitors', [])
    if competitors:
        story.append(Paragraph("Key Competitors:", doc.styles['SectionHeading']))
        competitor_data = [['Competitor', 'Strengths', 'Weaknesses']]
        for competitor in competitors[:3]:
            competitor_data.append([competitor, 'Market presence', 'Limited innovation'])
        
        competitor_table = Table(competitor_data, colWidths=[2*inch, 2*inch, 2*inch])
        competitor_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d69e2e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fffbeb')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2d3748')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#f6e05e')),
        ]))
        story.append(competitor_table)
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Our Competitive Advantages:", doc.styles['SectionHeading']))
    story.append(Paragraph("• Novel research-based approach with AI-powered analysis", doc.styles['BulletPoint']))
    story.append(Paragraph("• Strong technical foundation and proven methodology", doc.styles['BulletPoint']))
    story.append(Paragraph("• Clear market opportunity with validated demand", doc.styles['BulletPoint']))
    story.append(Paragraph("• Automated pipeline reducing time-to-market", doc.styles['BulletPoint']))
    
    # Slide 6: Feasibility & Roadmap
    story.append(PageBreak())
    story.append(Paragraph("5. Feasibility & Development Roadmap", doc.styles['SlideTitle']))
    story.append(Spacer(1, 0.3*inch))
    
    # Feasibility score
    feasibility_score = feasibility_data.get('feasibility_score', 0)
    story.append(Paragraph(f"Feasibility Score: {feasibility_score}/10", doc.styles['Highlight']))
    story.append(Spacer(1, 0.2*inch))
    
    # Development roadmap
    roadmap = feasibility_data.get('roadmap', [])
    if roadmap:
        story.append(Paragraph("Development Roadmap:", doc.styles['SectionHeading']))
        roadmap_data = [['Phase', 'Timeline', 'Key Milestones']]
        for i, milestone in enumerate(roadmap, 1):
            phase = f"Phase {i}"
            timeline = f"Q{i}" if i <= 4 else "Q4+"
            roadmap_data.append([phase, timeline, milestone])
        
        roadmap_table = Table(roadmap_data, colWidths=[1.5*inch, 1*inch, 4*inch])
        roadmap_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e53e3e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fed7d7')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2d3748')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#feb2b2')),
        ]))
        story.append(roadmap_table)
    
    # Resource requirements
    resources = feasibility_data.get('resources', {})
    if resources:
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("Resource Requirements:", doc.styles['SectionHeading']))
        story.append(Paragraph(f"• Timeline: {resources.get('time', 'N/A')}", doc.styles['BulletPoint']))
        story.append(Paragraph(f"• Team Size: {resources.get('team_size', 'N/A')}", doc.styles['BulletPoint']))
        story.append(Paragraph(f"• Budget: {resources.get('budget', 'N/A')}", doc.styles['BulletPoint']))
    
    # Slide 7: Business Model & Revenue
    story.append(PageBreak())
    story.append(Paragraph("6. Business Model & Revenue Potential", doc.styles['SlideTitle']))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Revenue Streams:", doc.styles['SectionHeading']))
    story.append(Paragraph("• SaaS Platform Licensing - Recurring subscription model", doc.styles['BulletPoint']))
    story.append(Paragraph("• Custom Analysis Services - Project-based consulting", doc.styles['BulletPoint']))
    story.append(Paragraph("• API Access - Pay-per-use data analysis", doc.styles['BulletPoint']))
    story.append(Paragraph("• Training & Certification - Educational programs", doc.styles['BulletPoint']))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Market Opportunity:", doc.styles['SectionHeading']))
    story.append(Paragraph(f"• Large addressable market ({tam})", doc.styles['BulletPoint']))
    story.append(Paragraph("• Growing market trends and demand", doc.styles['BulletPoint']))
    story.append(Paragraph("• Clear monetization path with multiple revenue streams", doc.styles['BulletPoint']))
    story.append(Paragraph("• Scalable technology platform", doc.styles['BulletPoint']))
    
    # Key risks
    risks = feasibility_data.get('risks', [])
    if risks:
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("Key Risks & Mitigation:", doc.styles['SectionHeading']))
        for risk in risks[:3]:
            story.append(Paragraph(f"• {risk}", doc.styles['BulletPoint']))
    
    # Slide 8: Team & Next Steps
    story.append(PageBreak())
    story.append(Paragraph("7. Team & Next Steps", doc.styles['SlideTitle']))
    story.append(Spacer(1, 0.3*inch))
    
    # Team recommendations
    team_roles = stakeholder_data.get('team_roles', [])
    if team_roles:
        story.append(Paragraph("Recommended Team Structure:", doc.styles['SectionHeading']))
        for role in team_roles:
            story.append(Paragraph(f"• {role}", doc.styles['BulletPoint']))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Immediate Next Steps:", doc.styles['SectionHeading']))
    story.append(Paragraph("• Finalize technical prototype and validation", doc.styles['BulletPoint']))
    story.append(Paragraph("• Conduct comprehensive market validation", doc.styles['BulletPoint']))
    story.append(Paragraph("• Build core founding team with key expertise", doc.styles['BulletPoint']))
    story.append(Paragraph("• Secure initial funding for development", doc.styles['BulletPoint']))
    story.append(Paragraph("• Establish strategic partnerships", doc.styles['BulletPoint']))
    
    # Slide 9: Investor Recommendations
    story.append(PageBreak())
    story.append(Paragraph("8. Investor Recommendations", doc.styles['SlideTitle']))
    story.append(Spacer(1, 0.3*inch))
    
    investor_matches = stakeholder_data.get('investor_matches', [])
    if investor_matches:
        story.append(Paragraph("Top Investor Matches:", doc.styles['SectionHeading']))
        
        investor_data = [['Investor', 'Match Score', 'Stage', 'Ticket Size', 'Focus Area']]
        for investor in investor_matches[:5]:
            name = investor.get('name', 'Unknown')
            score = investor.get('match_score', 0)
            stage = investor.get('stage', 'Unknown')
            ticket = investor.get('ticket_size', 'Unknown')
            focus = investor.get('focus_area', 'General')
            
            investor_data.append([
                name,
                f"{score*100:.0f}%",
                stage,
                ticket,
                focus
            ])
        
        investor_table = Table(investor_data, colWidths=[1.8*inch, 1*inch, 1.2*inch, 1.2*inch, 1.3*inch])
        investor_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d3748')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2d3748')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        story.append(investor_table)
    
    # Slide 10: Thank You
    story.append(NextPageTemplate('Title'))
    story.append(PageBreak())
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Thank You!", doc.styles['TitleSlide']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Questions & Discussion", doc.styles['Subtitle']))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("Contact: resa@ai.com", doc.styles['BodyText']))
    story.append(Paragraph("Website: www.resa.ai", doc.styles['BodyText']))
    
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
