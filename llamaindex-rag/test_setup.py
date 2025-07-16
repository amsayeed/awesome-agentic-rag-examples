"""
Quick test to verify the setup is working correctly
"""

import os
from dotenv import load_dotenv

def test_setup():
    """Test if everything is configured correctly"""
    print("🔍 Testing LlamaIndex Agentic RAG Setup...\n")
    
    # Check Python version
    import sys
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Check if .env exists
    if os.path.exists('.env'):
        print("✓ .env file found")
        load_dotenv()
        
        # Check API key
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            print("✓ OpenAI API key is set")
        else:
            print("✗ OpenAI API key not set properly")
            print("  Please edit .env and add your actual API key")
    else:
        print("✗ .env file not found")
        print("  Please copy .env.example to .env and add your API key")
        return False
    
    # Check required packages
    required_packages = [
        "llama_index",
        "streamlit",
        "faiss",
        "dotenv"
    ]
    
    print("\nChecking packages:")
    all_good = True
    for package in required_packages:
        try:
            if package == "faiss":
                import faiss
            elif package == "dotenv":
                import dotenv
            else:
                __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            all_good = False
    
    if all_good and api_key and api_key != "your_openai_api_key_here":
        print("\n🎉 Everything looks good! You can now run:")
        print("   python agentic_rag_demo.py")
        print("   or")
        print("   streamlit run streamlit_app.py")
    else:
        print("\n⚠️  Please fix the issues above before running the demo")
    
    return all_good

if __name__ == "__main__":
    test_setup()