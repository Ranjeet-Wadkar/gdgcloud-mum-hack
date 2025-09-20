"""
Verify Gemini API Key Setup
"""

import os
import google.generativeai as genai

def verify_gemini_setup():
    """Verify that Gemini API key is properly configured."""
    print("🔍 Verifying Gemini API Key Setup...")
    print("=" * 40)
    
    # Check for API key
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or api_key == 'demo-key-placeholder':
        print("❌ No valid API key found!")
        print("\nTo set up your API key:")
        print("1. Get your key from: https://makersuite.google.com/app/apikey")
        print("2. Set environment variable:")
        print("   Windows: $env:GEMINI_API_KEY='your-key'")
        print("   Linux/Mac: export GEMINI_API_KEY='your-key'")
        print("\nOr run in demo mode (no API key needed)")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Test API connection
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("🔄 Testing API connection...")
        response = model.generate_content("Hello, this is a test. Please respond with 'API working'.")
        
        if response.text:
            print("✅ API connection successful!")
            print(f"Response: {response.text}")
            return True
        else:
            print("❌ API connection failed - no response")
            return False
            
    except Exception as e:
        print(f"❌ API connection failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check if your API key is correct")
        print("2. Ensure you have internet connection")
        print("3. Verify your Google Cloud project has Gemini API enabled")
        return False

def main():
    """Main verification function."""
    print("🚀 Gemini API Key Verification")
    print("=" * 40)
    
    if verify_gemini_setup():
        print("\n🎉 Setup complete! You can now run the app with full Gemini integration.")
        print("Run: streamlit run app.py")
    else:
        print("\n⚠️ Setup incomplete. The app will run in demo mode.")
        print("Run: streamlit run app.py")

if __name__ == "__main__":
    main()
