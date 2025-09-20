"""
Test script to verify Gemini API connection and logging.
"""

from dotenv import load_dotenv
import os

load_dotenv()
# import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.gemini_client import initialize_gemini, call_gemini, DEMO_MODE

def test_gemini_connection():
    """Test Gemini API connection and logging."""
    print("🧪 Testing Gemini API Connection")
    print("=" * 50)
    
    # Test 1: Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    print(f"API Key found: {'Yes' if api_key and api_key != 'demo-key-placeholder' else 'No'}")
    print(f"API Key value: {api_key[:10] + '...' if api_key else 'None'}")
    
    # Test 2: Initialize Gemini
    print("\n🔄 Initializing Gemini...")
    model = initialize_gemini()
    # model = "gemini-1.5-pro-latest"
    print(f"Model initialized: {'Yes' if model else 'No'}")
    print ("model: ", model)
    print(f"Demo mode: {'Yes' if DEMO_MODE else 'No'}")
    
    # Test 3: Make API call
    print("\n🤖 Making test API call...")
    test_prompt = "Analyze this research paper and extract key innovations: 'This paper presents a novel machine learning approach for medical diagnosis.'"
    
    response = call_gemini(test_prompt)
    print(f"Response received: {'Yes' if response else 'No'}")
    print(f"Response length: {len(response)} characters")
    print(f"Response preview: {response[:200]}...")
    
    # Test 4: Check if response is dynamic
    print("\n🔄 Testing response variability...")
    response2 = call_gemini("Different prompt about AI in healthcare")
    print(f"Different response: {'Yes' if response != response2 else 'No'}")
    
    # Test 5: JSON parsing
    print("\n📋 Testing JSON parsing...")
    try:
        import json
        parsed = json.loads(response)
        print(f"JSON parsing: {'Success' if parsed else 'Failed'}")
        if parsed:
            print(f"Keys found: {list(parsed.keys())}")
    except:
        print("JSON parsing: Failed")
    
    print("\n" + "=" * 50)
    if DEMO_MODE:
        print("⚠️ Running in DEMO MODE - Set GEMINI_API_KEY for real API calls")
    else:
        print("✅ Gemini API connection working!")
    
    return not DEMO_MODE

if __name__ == "__main__":
    test_gemini_connection()

# import google.generativeai as genai
# import os

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # List available models
# for m in genai.list_models():
#     print(m.name, "→ supports:", m.supported_generation_methods)


