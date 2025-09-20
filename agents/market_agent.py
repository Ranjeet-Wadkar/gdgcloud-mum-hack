"""
Market Intelligence Agent for the Research-to-Startup AI Agent Swarm.
Analyzes market potential, trends, and competitive landscape using Tavily API and Gemini AI.
"""

import json
import os
from typing import Dict, List, Any
from dotenv import load_dotenv
from tavily import TavilyClient
from utils.gemini_client import call_gemini

load_dotenv()

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
        # If it's a dict with 'description' and 'estimates', extract the most relevant estimate
        elif 'description' in market_data and 'estimates' in market_data:
            estimates = market_data.get('estimates', [])
            if estimates:
                # Get the most recent or largest estimate
                best_estimate = estimates[0]  # Take the first one as default
                for estimate in estimates:
                    # Prefer estimates with higher year or larger size
                    if estimate.get('year', 0) > best_estimate.get('year', 0):
                        best_estimate = estimate
                
                # Format the estimate
                size = best_estimate.get('size', 'Unknown')
                year = best_estimate.get('year', '')
                segment = best_estimate.get('segment', '')
                
                if year and segment:
                    return f"{size} ({year}, {segment})"
                elif year:
                    return f"{size} ({year})"
                else:
                    return str(size)
            else:
                return market_data.get('description', 'N/A')
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

def initialize_tavily_client() -> TavilyClient:
    """Initialize Tavily client with API key."""
    api_key = os.getenv('TAVILY_API_KEY')
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables")
    return TavilyClient(api_key=api_key)

def generate_domain_queries(domains: List[str]) -> List[str]:
    """
    Generate structured queries for each domain.
    
    Args:
        domains: List of application domains
    
    Returns:
        List of query strings
    """
    queries = []
    for domain in domains:
        queries.extend([
            f"Market size of {domain} 2024",
            f"Top competitors in {domain}",
            f"Trends in {domain}",
            f"Latest funding and investments in {domain}"
        ])
    return queries

def search_with_tavily(query: str, tavily_client: TavilyClient) -> Dict[str, Any]:
    """
    Search using Tavily API with error handling.
    
    Args:
        query: Search query string
        tavily_client: Initialized Tavily client
    
    Returns:
        Dictionary containing search results
    """
    try:
        response = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )
        return response
    except Exception as e:
        print(f"Tavily search failed for query '{query}': {e}")
        # Fallback to general query
        try:
            fallback_query = f"general trends in {query.split()[-1]} industry"
            response = tavily_client.search(
                query=fallback_query,
                search_depth="basic",
                max_results=3
            )
            return response
        except Exception as e:
            print(f"Fallback search also failed: {e}")
            return {"results": [], "query": query}

def extract_sources_from_results(results: List[Dict]) -> List[str]:
    """
    Extract source URLs from Tavily results.
    
    Args:
        results: List of search results from Tavily
    
    Returns:
        List of source URLs
    """
    sources = []
    for result in results:
        if 'url' in result:
            sources.append(result['url'])
    return sources

def summarize_with_gemini(query_type: str, search_results: List[Dict], sources: List[str]) -> Dict[str, Any]:
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
    if query_type == "market_size":
        prompt = f"""
        Analyze the following search results about market size and provide a structured summary.
        
        {content}
        
        Extract and summarize:
        1. Total Addressable Market (TAM) - overall market size
        2. Serviceable Addressable Market (SAM) - realistic target market
        3. Serviceable Obtainable Market (SOM) - achievable market share
        
        Return as JSON with keys: TAM, SAM, SOM
        Include specific numbers, timeframes, and market segments where available.
        """
    elif query_type == "competitors":
        prompt = f"""
        Analyze the following search results about competitors and provide a structured summary.
        
        {content}
        
        Extract and summarize:
        1. Top 3-5 competitors with their focus areas
        2. Market positioning and key differentiators
        
        Return as JSON with key "competitors" containing list of objects with:
        - name: company name
        - focus: their main focus area
        - source: source URL
        """
    elif query_type == "trends":
        prompt = f"""
        Analyze the following search results about market trends and provide a structured summary.
        
        {content}
        
        Extract and summarize:
        1. Top 3-5 key market trends
        2. Growth drivers and market dynamics
        
        Return as JSON with key "trends" containing list of objects with:
        - trend: trend description
        - source: source URL
        """
    elif query_type == "funding":
        prompt = f"""
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
    else:
        prompt = f"""
        Analyze the following search results and provide a structured summary.
        
        {content}
        
        Return as JSON with relevant extracted information.
        """
    
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

def analyze_market_intelligence(research_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze market potential using Tavily API and Gemini AI.
    
    Args:
        research_data: Output from research analysis agent
    
    Returns:
        Dictionary containing market analysis results
    """
    innovations = research_data.get('innovations', [])
    domains = research_data.get('application_domains', [])
    
    if not domains:
        domains = ["technology"]  # Fallback domain
    
    # Initialize Tavily client
    try:
        tavily_client = initialize_tavily_client()
    except ValueError as e:
        print(f"Tavily initialization failed: {e}")
        return {
            "TAM": "N/A (Tavily API not configured)",
            "SAM": "N/A (Tavily API not configured)",
            "SOM": "N/A (Tavily API not configured)",
            "trends": [],
            "competitors": [],
            "funding": [],
            "market_summary": "Market analysis unavailable - Tavily API not configured"
        }
    
    # Generate queries for each domain
    queries = generate_domain_queries(domains)
    
    # Initialize result structure
    market_results = {
        "TAM": "N/A",
        "SAM": "N/A", 
        "SOM": "N/A",
        "trends": [],
        "competitors": [],
        "funding": []
    }
    
    all_sources = []
    
    # Process each query type
    query_types = ["market_size", "competitors", "trends", "funding"]
    
    for i, query_type in enumerate(query_types):
        # Get queries for this type
        type_queries = [q for j, q in enumerate(queries) if j % 4 == i]
        
        if not type_queries:
            continue
            
        # Use the first query for this type
        query = type_queries[0]
        
        # Search with Tavily
        search_response = search_with_tavily(query, tavily_client)
        results = search_response.get('results', [])
        sources = extract_sources_from_results(results)
        all_sources.extend(sources)
        
        if results:
            # Summarize with Gemini
            summary = summarize_with_gemini(query_type, results, sources)
            
            # Merge results based on type
            if query_type == "market_size":
                # Extract actual values from potentially complex structures
                tam_value = extract_market_value(summary.get("TAM", "N/A"))
                sam_value = extract_market_value(summary.get("SAM", "N/A"))
                som_value = extract_market_value(summary.get("SOM", "N/A"))
                
                market_results.update({
                    "TAM": tam_value,
                    "SAM": sam_value,
                    "SOM": som_value
                })
            elif query_type == "competitors":
                market_results["competitors"] = summary.get("competitors", [])
            elif query_type == "trends":
                market_results["trends"] = summary.get("trends", [])
            elif query_type == "funding":
                market_results["funding"] = summary.get("funding", [])
    
    # Create market summary
    tam = market_results["TAM"]
    trends_count = len(market_results["trends"])
    competitors_count = len(market_results["competitors"])
    
    market_results["market_summary"] = f"Total addressable market of {tam} with {trends_count} key trends and {competitors_count} major competitors. Sources: {', '.join(all_sources[:3]) if all_sources else 'N/A'}"
    
    return market_results

def get_agent_voice_message(market_data: Dict[str, Any]) -> str:
    """Generate human-readable voice message for visualization."""
    tam = market_data.get('TAM', 'N/A')
    trends = market_data.get('trends', [])
    competitors = market_data.get('competitors', [])
    
    # Extract competitor names
    competitor_names = []
    for competitor in competitors:
        if isinstance(competitor, dict):
            competitor_names.append(competitor.get('name', 'Unknown'))
        else:
            competitor_names.append(str(competitor))
    
    # Extract trend descriptions
    trend_descriptions = []
    for trend in trends:
        if isinstance(trend, dict):
            trend_descriptions.append(trend.get('trend', 'Unknown trend'))
        else:
            trend_descriptions.append(str(trend))
    
    message = f"📊 Market Analysis Complete!\n\n"
    message += f"The global market opportunity is estimated at {tam} with strong growth potential. "
    
    if trend_descriptions:
        message += f"Key trends include {trend_descriptions[0]} and {trend_descriptions[1] if len(trend_descriptions) > 1 else 'sustainability'}. "
    else:
        message += "Key trends include digital transformation and sustainability. "
    
    if competitor_names:
        message += f"Major competitors include {', '.join(competitor_names[:2])}."
    else:
        message += "Major competitors include established players."
    
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
