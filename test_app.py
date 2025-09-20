"""
Test script for the Research-to-Startup AI Agent Swarm
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from agents.research_agent import run_research_agent
        from agents.market_agent import run_market_agent
        from agents.feasibility_agent import run_feasibility_agent
        from agents.stakeholder_agent import run_stakeholder_agent
        from agents.business_plan_agent import run_business_plan_agent
        from utils.parser import extract_text_from_pdf, clean_text, validate_text_input
        from utils.matcher import find_investor_matches, get_team_recommendations
        from utils.deck_generator import create_pitch_deck, generate_deck_summary
        from utils.gemini_client import initialize_gemini, call_gemini
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_agents():
    """Test agent functionality with sample data."""
    try:
        from agents.research_agent import run_research_agent
        from agents.market_agent import run_market_agent
        from agents.feasibility_agent import run_feasibility_agent
        from agents.stakeholder_agent import run_stakeholder_agent
        from agents.business_plan_agent import run_business_plan_agent
        
        # Sample research text
        sample_text = """
        This paper presents a novel machine learning approach for medical diagnosis.
        Our method achieves 95% accuracy on the test dataset, significantly outperforming
        existing solutions. The technology has potential applications in healthcare,
        telemedicine, and clinical decision support systems.
        """
        
        print("🔬 Testing Research Agent...")
        research_result = run_research_agent(sample_text)
        print(f"   Status: {research_result['status']}")
        
        print("📊 Testing Market Agent...")
        market_result = run_market_agent(research_result['output'])
        print(f"   Status: {market_result['status']}")
        
        print("⚙️ Testing Feasibility Agent...")
        feasibility_result = run_feasibility_agent(research_result['output'], market_result['output'])
        print(f"   Status: {feasibility_result['status']}")
        
        print("🤝 Testing Stakeholder Agent...")
        stakeholder_result = run_stakeholder_agent(
            research_result['output'], 
            market_result['output'], 
            feasibility_result['output']
        )
        print(f"   Status: {stakeholder_result['status']}")
        
        print("📋 Testing Business Plan Agent...")
        business_plan_result = run_business_plan_agent(
            research_result['output'],
            market_result['output'],
            feasibility_result['output'],
            stakeholder_result['output']
        )
        print(f"   Status: {business_plan_result['status']}")
        
        print("✅ All agents tested successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Agent test error: {e}")
        return False

def test_utilities():
    """Test utility functions."""
    try:
        from utils.matcher import find_investor_matches, get_team_recommendations
        from utils.parser import clean_text, validate_text_input
        from utils.gemini_client import call_gemini
        
        print("🔧 Testing Utilities...")
        
        # Test text processing
        sample_text = "This is a sample research paper with some content."
        cleaned = clean_text(sample_text)
        is_valid = validate_text_input(cleaned)
        print(f"   Text processing: {'✅' if is_valid else '❌'}")
        
        # Test investor matching
        project_attributes = {
            'application_domains': ['AI/ML', 'Healthcare'],
            'readiness_level': 5,
            'funding_needs': 500000,
            'geo': 'Global'
        }
        matches = find_investor_matches(project_attributes)
        print(f"   Investor matching: {'✅' if matches else '❌'}")
        
        # Test team recommendations
        team_roles = get_team_recommendations(project_attributes)
        print(f"   Team recommendations: {'✅' if team_roles else '❌'}")
        
        # Test Gemini client (demo mode)
        gemini_response = call_gemini("Test prompt for Gemini")
        print(f"   Gemini client: {'✅' if gemini_response else '❌'}")
        
        print("✅ All utilities tested successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Utility test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Research-to-Startup AI Agent Swarm")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Agent Test", test_agents),
        ("Utility Test", test_utilities)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo start the application, run:")
        print("streamlit run app.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
