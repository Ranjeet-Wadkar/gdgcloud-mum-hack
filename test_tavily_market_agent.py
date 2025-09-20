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
        # R

"""
Test script for the upgraded Tavily-powered Market Intelligence Agent
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def test_tavily_connection():
    """Test Tavily API connection."""
    try:
        from tavily import TavilyClient
        
        api_key = os.getenv('TAVILY_API_KEY')
        if not api_key or api_key == 'demo-key-placeholder':
            print("❌ TAVILY_API_KEY not configured")
            return False
        
        tavily_client = TavilyClient(api_key=api_key)
        response = tavily_client.search("test query", max_results=1)
        
        if response and 'results' in response:
            print("✅ Tavily API connection successful")
            return True
        else:
            print("❌ Tavily API response invalid")
            return False
            
    except Exception as e:
        print(f"❌ Tavily connection failed: {e}")
        return False

def test_market_agent():
    """Test the upgraded market agent with Tavily integration."""
    try:
        from agents.market_agent import run_market_agent
        
        # Sample research data
        research_data = {
            'innovations': ['Perovskite Solar Cells', 'Flexible Photovoltaics'],
            'application_domains': ['Renewable Energy', 'Solar Technology'],
            'readiness_level': 6,
            'key_findings': ['High efficiency potential', 'Cost reduction opportunities']
        }
        
        print("📊 Testing Market Agent with Tavily...")
        market_result = run_market_agent(research_data)
        
        print(f"   Status: {market_result['status']}")
        print(f"   Agent: {market_result['agent_name']}")
        
        output = market_result['output']
        print(f"   TAM: {output.get('TAM', 'N/A')}")
        print(f"   SAM: {output.get('SAM', 'N/A')}")
        print(f"   SOM: {output.get('SOM', 'N/A')}")
        
        trends = output.get('trends', [])
        print(f"   Trends: {len(trends)} found")
        for i, trend in enumerate(trends[:2], 1):
            if isinstance(trend, dict):
                print(f"     {i}. {trend.get('trend', 'Unknown')} - {trend.get('source', 'No source')}")
            else:
                print(f"     {i}. {trend}")
        
        competitors = output.get('competitors', [])
        print(f"   Competitors: {len(competitors)} found")
        for i, competitor in enumerate(competitors[:2], 1):
            if isinstance(competitor, dict):
                print(f"     {i}. {competitor.get('name', 'Unknown')} - {competitor.get('focus', 'Unknown focus')}")
            else:
                print(f"     {i}. {competitor}")
        
        funding = output.get('funding', [])
        print(f"   Funding: {len(funding)} found")
        for i, fund in enumerate(funding[:2], 1):
            if isinstance(fund, dict):
                print(f"     {i}. {fund.get('company', 'Unknown')} - {fund.get('amount', 'Unknown')}")
            else:
                print(f"     {i}. {fund}")
        
        print("✅ Market Agent test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Market Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_structured_output():
    """Test that the output maintains the expected JSON structure."""
    try:
        from agents.market_agent import run_market_agent
        
        research_data = {
            'innovations': ['AI-powered diagnostics'],
            'application_domains': ['Healthcare Technology'],
            'readiness_level': 5
        }
        
        print(" Testing structured output...")
        market_result = run_market_agent(research_data)
        output = market_result['output']
        
        # Check required keys
        required_keys = ['TAM', 'SAM', 'SOM', 'trends', 'competitors', 'market_summary']
        missing_keys = [key for key in required_keys if key not in output]
        
        if missing_keys:
            print(f"❌ Missing required keys: {missing_keys}")
            return False
        
        # Check data types
        if not isinstance(output['trends'], list):
            print("❌ 'trends' should be a list")
            return False
        
        if not isinstance(output['competitors'], list):
            print("❌ 'competitors' should be a list")
            return False
        
        print("✅ Structured output test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Structured output test failed: {e}")
        return False

def main():
    """Run all Tavily market agent tests."""
    print(" Testing Tavily-powered Market Intelligence Agent")
    print("=" * 60)
    
    tests = [
        ("Tavily Connection", test_tavily_connection),
        ("Market Agent", test_market_agent),
        ("Structured Output", test_structured_output)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print("\n" + "=" * 60)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print(" All Tavily market agent tests passed!")
        print("\nThe upgraded Market Intelligence Agent is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("\nMake sure to:")
        print("1. Set TAVILY_API_KEY in your .env file")
        print("2. Install tavily-python: pip install tavily-python")
        print("3. Check your internet connection")

if __name__ == "__main__":
    main()
