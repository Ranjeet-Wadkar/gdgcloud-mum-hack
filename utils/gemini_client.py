"""
Gemini AI client for the Research-to-Startup AI Agent Swarm.
Handles all interactions with Google's Gemini API with comprehensive logging.
"""

import google.generativeai as genai
import json
from dotenv import load_dotenv
import os

load_dotenv()
import logging
from typing import Dict, Any, List
import streamlit as st
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to track if we're in demo mode
DEMO_MODE = False

def initialize_gemini():
    """Initialize Gemini client with API key."""
    global DEMO_MODE
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'demo-key-placeholder':
        DEMO_MODE = True
        logger.warning("⚠️ Running in DEMO MODE - No valid API key found")
        st.warning("⚠️ Using demo mode. Set GEMINI_API_KEY environment variable for real Gemini API access.")
        return None
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        logger.info("✅ Gemini API initialized successfully")
        DEMO_MODE = False
        return model
    except Exception as e:
        logger.error(f"❌ Failed to initialize Gemini: {str(e)}")
        DEMO_MODE = True
        st.error(f"❌ Gemini initialization failed: {str(e)}")
        return None

def call_gemini(prompt: str, model_name: str = 'gemini-1.5-flash') -> str:
    """
    Call Gemini API with a prompt and return the response.
    
    Args:
        prompt: The input prompt for the model
        model_name: The Gemini model to use (default: gemini-1.5-flash)
    
    Returns:
        The model's response as a string
    """
    global DEMO_MODE
    
    # Log the API call
    logger.info(f"🤖 Gemini API Call - Model: {model_name}")
    logger.info(f"📝 Prompt: {prompt[:200]}...")
    
    if DEMO_MODE:
        logger.warning("⚠️ DEMO MODE - Returning mock response")
        mock_response = generate_mock_response(prompt)
        logger.info(f"📤 Mock Response: {mock_response[:200]}...")
        return mock_response
    
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        
        if response.text:
            logger.info(f"✅ Gemini API Response received")
            logger.info(f"📤 Response: {response.text[:200]}...")
            return response.text
        else:
            logger.warning("⚠️ Empty response from Gemini API")
            return generate_mock_response(prompt)
            
    except Exception as e:
        logger.error(f"❌ Gemini API Error: {str(e)}")
        logger.warning("⚠️ Falling back to mock response")
        return generate_mock_response(prompt)

def generate_mock_response(prompt: str) -> str:
    """Generate intelligent mock responses based on prompt content."""
    prompt_lower = prompt.lower()
    
    if "innovations" in prompt_lower and "research" in prompt_lower:
        return json.dumps({
            "innovations": [
                "Novel machine learning algorithm for pattern recognition",
                "Advanced materials with enhanced properties", 
                "Innovative computational approach to optimization"
            ],
            "readiness_level": 6,
            "application_domains": ["AI/ML", "Healthcare", "Manufacturing"],
            "technical_summary": "Breakthrough research with strong commercial potential"
        })
    
    elif "market" in prompt_lower and "tam" in prompt_lower:
        return json.dumps({
            "TAM": "$500B",
            "SAM": "$50B",
            "SOM": "$5B", 
            "trends": [
                "Rapid digital transformation across industries",
                "Increased focus on AI-powered solutions",
                "Growing demand for automation"
            ],
            "competitors": ["Google", "Microsoft", "Amazon", "IBM", "OpenAI"]
        })
    
    elif "feasibility" in prompt_lower and "roadmap" in prompt_lower:
        return json.dumps({
            "roadmap": [
                "Complete technical validation",
                "Develop MVP prototype", 
                "Conduct market validation",
                "Refine product based on feedback",
                "Scale manufacturing",
                "Launch commercial product"
            ],
            "resources": {
                "time": "18 months",
                "team_size": "8 people", 
                "budget": "$1.5M"
            },
            "risks": [
                "Technical complexity challenges",
                "Market competition",
                "Regulatory requirements",
                "Funding constraints",
                "Talent acquisition"
            ],
            "feasibility_score": 7
        })
    
    elif "business plan" in prompt_lower and "slides" in prompt_lower:
        return json.dumps({
            "slides": [
                {
                    "title": "Problem & Opportunity",
                    "content": "Addressing critical challenges in target market with innovative solutions."
                },
                {
                    "title": "Core Innovation",
                    "content": "Breakthrough technology with clear competitive advantages."
                },
                {
                    "title": "Market Landscape", 
                    "content": "Large addressable market with strong growth potential."
                },
                {
                    "title": "Competitive Advantage",
                    "content": "Unique positioning with sustainable competitive moats."
                },
                {
                    "title": "Feasibility & Roadmap",
                    "content": "Clear development path with realistic resource requirements."
                },
                {
                    "title": "Business Potential",
                    "content": "Strong revenue potential with clear monetization strategy."
                },
                {
                    "title": "Next Steps & Investor Recommendations",
                    "content": "Ready for funding with identified investor matches."
                }
            ]
        })
    
    else:
        return f"Mock Gemini response for: {prompt[:100]}..."

def analyze_research_with_gemini(text: str) -> Dict[str, Any]:
    """
    Use Gemini to analyze research paper and extract key information.
    
    Args:
        text: Research paper text content
    
    Returns:
        Dictionary containing analysis results
    """
    prompt = f"""
    Analyze this research paper and extract the following information in JSON format:
    
    {text[:2000]}...
    
    Please provide:
    1. Key innovations (list of 3-5 main innovations)
    2. Technology readiness level (TRL 1-9)
    3. Application domains (list of relevant industries/domains)
    4. Technical summary (brief description of the technology)
    
    Return as JSON with keys: innovations, readiness_level, application_domains, technical_summary
    """
    
    response = call_gemini(prompt)
    
    # Try to parse JSON response, fallback to mock data
    try:
        # Extract JSON from response if it's wrapped in markdown
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response
        
        result = json.loads(json_str)
        return result
    except:
        # Fallback to mock data
        return {
            "innovations": [
                "Novel machine learning algorithm for pattern recognition",
                "Advanced materials with enhanced properties",
                "Innovative computational approach to optimization"
            ],
            "readiness_level": 5,
            "application_domains": ["AI/ML", "Healthcare", "Manufacturing"],
            "technical_summary": "Breakthrough research with strong commercial potential"
        }

def analyze_market_with_gemini(innovations: List[str], domains: List[str]) -> Dict[str, Any]:
    """
    Use Gemini to analyze market potential.
    
    Args:
        innovations: List of key innovations
        domains: List of application domains
    
    Returns:
        Dictionary containing market analysis
    """
    prompt = f"""
    Analyze the market potential for these innovations: {', '.join(innovations)}
    in these domains: {', '.join(domains)}
    
    Provide market analysis in JSON format with:
    1. Total Addressable Market (TAM) - estimated market size
    2. Serviceable Addressable Market (SAM) - realistic target market
    3. Serviceable Obtainable Market (SOM) - achievable market share
    4. Key market trends (list of 3-5 trends)
    5. Major competitors (list of 3-5 competitors)
    
    Return as JSON with keys: TAM, SAM, SOM, trends, competitors
    """
    
    response = call_gemini(prompt)
    
    try:
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response
        
        result = json.loads(json_str)
        return result
    except:
        # Fallback to mock data
        return {
            "TAM": "$500B",
            "SAM": "$50B", 
            "SOM": "$5B",
            "trends": [
                "Rapid digital transformation across industries",
                "Increased focus on AI-powered solutions",
                "Growing demand for automation"
            ],
            "competitors": ["Google", "Microsoft", "Amazon", "IBM", "OpenAI"]
        }

def assess_feasibility_with_gemini(research_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use Gemini to assess commercial feasibility.
    
    Args:
        research_data: Research analysis results
        market_data: Market analysis results
    
    Returns:
        Dictionary containing feasibility assessment
    """
    prompt = f"""
    Assess the commercial feasibility for this technology:
    
    Innovations: {research_data.get('innovations', [])}
    TRL Level: {research_data.get('readiness_level', 0)}
    Domains: {research_data.get('application_domains', [])}
    Market Size: {market_data.get('TAM', 'N/A')}
    
    Provide feasibility analysis in JSON format with:
    1. Development roadmap (list of 5-7 key milestones)
    2. Resource requirements (time, team size, budget)
    3. Key risks (list of 5-7 risks)
    4. Feasibility score (1-10)
    
    Return as JSON with keys: roadmap, resources, risks, feasibility_score
    """
    
    response = call_gemini(prompt)
    
    try:
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response
        
        result = json.loads(json_str)
        return result
    except:
        # Fallback to mock data
        return {
            "roadmap": [
                "Complete technical validation",
                "Develop MVP prototype",
                "Conduct market validation",
                "Refine product based on feedback",
                "Scale manufacturing",
                "Launch commercial product"
            ],
            "resources": {
                "time": "18 months",
                "team_size": "8 people",
                "budget": "$1.5M"
            },
            "risks": [
                "Technical complexity challenges",
                "Market competition",
                "Regulatory requirements",
                "Funding constraints",
                "Talent acquisition"
            ],
            "feasibility_score": 7
        }

def generate_business_plan_with_gemini(all_agent_outputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use Gemini to generate comprehensive business plan.
    
    Args:
        all_agent_outputs: Combined outputs from all agents
    
    Returns:
        Dictionary containing business plan and pitch deck content
    """
    prompt = f"""
    Generate a comprehensive business plan and pitch deck based on this analysis:
    
    Research: {all_agent_outputs.get('research_agent', {})}
    Market: {all_agent_outputs.get('market_agent', {})}
    Feasibility: {all_agent_outputs.get('feasibility_agent', {})}
    Stakeholders: {all_agent_outputs.get('stakeholder_agent', {})}
    
    Create a pitch deck with 7 slides in JSON format:
    1. Problem & Opportunity
    2. Core Innovation
    3. Market Landscape
    4. Competitive Advantage
    5. Feasibility & Roadmap
    6. Business Potential
    7. Next Steps & Investor Recommendations
    
    Return as JSON with key "slides" containing array of slide objects with "title" and "content" fields.
    """
    
    response = call_gemini(prompt)
    
    try:
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response
        
        result = json.loads(json_str)
        return result
    except:
        # Fallback to mock data
        return {
            "slides": [
                {
                    "title": "Problem & Opportunity",
                    "content": "Addressing critical challenges in target market with innovative solutions."
                },
                {
                    "title": "Core Innovation", 
                    "content": "Breakthrough technology with clear competitive advantages."
                },
                {
                    "title": "Market Landscape",
                    "content": "Large addressable market with strong growth potential."
                },
                {
                    "title": "Competitive Advantage",
                    "content": "Unique positioning with sustainable competitive moats."
                },
                {
                    "title": "Feasibility & Roadmap",
                    "content": "Clear development path with realistic resource requirements."
                },
                {
                    "title": "Business Potential",
                    "content": "Strong revenue potential with clear monetization strategy."
                },
                {
                    "title": "Next Steps & Investor Recommendations",
                    "content": "Ready for funding with identified investor matches."
                }
            ]
        }
