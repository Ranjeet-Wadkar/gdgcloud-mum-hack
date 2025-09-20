"""
Centralized Gemini summarization utilities for Tavily search results.
"""

import json
from typing import Dict, List, Any
from utils.gemini_client import call_gemini

def summarize_search_results(query_type: str, search_results: List[Dict], sources: List[str]) -> Dict[str, Any]:
    """
    Use Gemini to summarize Tavily search results into structured data.
    
    Args:
        query_type: Type of query (market_size, competitors, trends, funding)
        search_results: Raw search results from Tavily
        sources: List of source URLs
    
    Returns:
        Structured summary dictionary
    """
    # Prepare content for Gemini
    content = f"Query Type: {query_type}\n\n"
    content += "Search Results:\n"
    for i, result in enumerate(search_results[:3], 1):  # Limit to top 3 results
        content += f"{i}. {result.get('title', 'No title')}\n"
        content += f"   {result.get('content', 'No content')}\n"
        content += f"   URL: {result.get('url', 'No URL')}\n\n"
    
    # Create specific prompts based on query type
    prompts = {
        "market_size": f"""
        Analyze the following search results about market size and provide a structured summary.
        
        {content}
        
        Extract and summarize:
        1. Total Addressable Market (TAM) - overall market size
        2. Serviceable Addressable Market (SAM) - realistic target market
        3. Serviceable Obtainable Market (SOM) - achievable market share
        
        Return as JSON with keys: TAM, SAM, SOM
        Include specific numbers, timeframes, and market segments where available.
        """,
        
        "competitors": f"""
        Analyze the following search results about competitors and provide a structured summary.
        
        {content}
        
        Extract and summarize:
        1. Top 3-5 competitors with their focus areas
        2. Market positioning and key differentiators
        
        Return as JSON with key "competitors" containing list of objects with:
        - name: company name
        - focus: their main focus area
        - source: source URL
        """,
        
        "trends": f"""
        Analyze the following search results about market trends and provide a structured summary.
        
        {content}
        
        Extract and summarize:
        1. Top 3-5 key market trends
        2. Growth drivers and market dynamics
        
        Return as JSON with key "trends" containing list of objects with:
        - trend: trend description
        - source: source URL
        """,
        
        "funding": f"""
        Analyze the following search results about funding and investments and provide a structured summary.
        
        {content}
        
        Extract and summarize:
        1. Recent funding rounds and investment amounts
        2. Key investors and investment trends
        
        Return as JSON with key "funding" containing list of objects with:
        - round: funding round type
        - company: company name
        - amount: funding amount
        - source: source URL
        """
    }
    
    prompt = prompts.get(query_type, f"""
    Analyze the following search results and provide a structured summary.
    
    {content}
    
    Return as JSON with relevant extracted information.
    """)
    
    try:
        response = call_gemini(prompt)
        
        # Try to extract JSON from response
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response
        
        result = json.loads(json_str)
        return result
    except Exception as e:
        print(f"Gemini summarization failed: {e}")
        # Return fallback structure
        return {query_type: "Analysis failed", "sources": sources}

def create_visualization_text(market_data: Dict[str, Any]) -> str:
    """
    Create visualization-friendly text from market data.
    
    Args:
        market_data: Market analysis results
    
    Returns:
        Formatted text for visualization
    """
    tam = market_data.get('TAM', 'N/A')
    sam = market_data.get('SAM', 'N/A')
    trends = market_data.get('trends', [])
    competitors = market_data.get('competitors', [])
    
    # Extract competitor names and sources
    competitor_info = []
    for competitor in competitors[:2]:  # Top 2 competitors
        if isinstance(competitor, dict):
            name = competitor.get('name', 'Unknown')
            source = competitor.get('source', '')
            competitor_info.append(f"{name} [{'link' if source else 'no source'}]")
        else:
            competitor_info.append(str(competitor))
    
    # Extract trend descriptions
    trend_descriptions = []
    for trend in trends[:2]:  # Top 2 trends
        if isinstance(trend, dict):
            trend_descriptions.append(trend.get('trend', 'Unknown trend'))
        else:
            trend_descriptions.append(str(trend))
    
    # Create visualization text
    text = f"The global market is projected at {tam}. "
    if sam != 'N/A':
        text += f"Target segment represents {sam}, "
    
    if competitor_info:
        text += f"with {', '.join(competitor_info)} leading. "
    
    if trend_descriptions:
        text += f"Key trends include {trend_descriptions[0]} and {trend_descriptions[1] if len(trend_descriptions) > 1 else 'sustainability'}."
    
    return text
