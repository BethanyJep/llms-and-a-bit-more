"""
Test script to verify Azure OpenAI API integration
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def test_openai_setup():
    """Test if Azure OpenAI is properly configured."""
    print("=" * 60)
    print("🧪 Testing Azure OpenAI Integration")
    print("=" * 60)
    
    # Check 1: .env file exists
    print("\n✓ Step 1: Checking for .env file...")
    env_path = Path(__file__).parent / '.env'
    
    if not env_path.exists():
        print("❌ FAIL: .env file not found")
        print("\nTo fix this:")
        print("  1. Copy .env.example to .env:")
        print("     cp .env.example .env")
        print("  2. Edit .env and add your Azure OpenAI credentials")
        return False
    
    print(f"✅ .env file found at: {env_path}")
    
    # Load environment variables
    load_dotenv(dotenv_path=env_path)
    
    # Check 2: Environment variables
    print("\n✓ Step 2: Checking environment variables...")
    use_openai = os.environ.get("USE_OPENAI", "false").lower() == "true"
    
    if use_openai:
        print("📌 Using regular OpenAI API")
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            print("❌ FAIL: OPENAI_API_KEY not set in .env file")
            return False
        
        if not api_key.startswith("sk-"):
            print(f"⚠️  WARNING: API key doesn't start with 'sk-': {api_key[:10]}...")
            return False
        
        print(f"✅ OpenAI API Key: {api_key[:10]}...{api_key[-4:]}")
        endpoint = None
        deployment_name = "gpt-4o-mini"
        
    else:
        print("📌 Using Azure OpenAI API")
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
        api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        
        missing_vars = []
        if not api_key:
            missing_vars.append("AZURE_OPENAI_API_KEY")
        if not endpoint:
            missing_vars.append("AZURE_OPENAI_ENDPOINT")
        if not deployment_name:
            missing_vars.append("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        if missing_vars:
            print(f"❌ FAIL: Missing variables in .env file: {', '.join(missing_vars)}")
            print("\nTo fix this:")
            print("  1. Go to Azure Portal → Your OpenAI Resource")
            print("  2. Copy API Key and Endpoint from 'Keys and Endpoint'")
            print("  3. Add them to your .env file")
            return False
        
        print(f"✅ Azure OpenAI API Key: {api_key[:10]}...{api_key[-4:]}")
        print(f"✅ Azure Endpoint: {endpoint}")
        print(f"✅ Deployment Name: {deployment_name}")
        print(f"✅ API Version: {api_version}")
    
    # Check 3: Import OpenAI
    print("\n✓ Step 3: Importing OpenAI library...")
    try:
        if use_openai:
            from openai import OpenAI
        else:
            from openai import AzureOpenAI
        print("✅ OpenAI library imported successfully")
    except ImportError:
        print("❌ FAIL: OpenAI library not installed")
        print("\nTo fix this, run:")
        print("  pip install openai python-dotenv")
        return False
    
    # Check 4: Initialize client
    print("\n✓ Step 4: Initializing OpenAI client...")
    try:
        if use_openai:
            client = OpenAI(api_key=api_key)
        else:
            client = AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=endpoint
            )
        print("✅ Client initialized successfully")
    except Exception as e:
        print(f"❌ FAIL: Could not initialize client: {e}")
        return False
    
    # Check 5: Test API call
    print("\n✓ Step 5: Testing API connection...")
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "user", "content": "Say 'Hello from Event Coverage Agent!'"}
            ],
            max_tokens=20
        )
        
        message = response.choices[0].message.content
        print(f"✅ API test successful!")
        print(f"   Response: {message}")
        
    except Exception as e:
        print(f"❌ FAIL: API call failed: {e}")
        print("\nPossible issues:")
        if use_openai:
            print("  - Invalid OpenAI API key")
            print("  - No credits/quota remaining")
        else:
            print("  - Invalid Azure OpenAI API key or endpoint")
            print("  - Deployment name doesn't exist")
            print("  - API version incompatible")
        print("  - Network issues")
        return False
    
    # Check 6: Import AI generator
    print("\n✓ Step 6: Testing AI generator module...")
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from ai_generator import initialize_openai as init_ai
        init_ai()
        print("✅ AI generator module works!")
    except Exception as e:
        print(f"❌ FAIL: Could not import ai_generator: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 60)
    
    if use_openai:
        print("\nYou're using regular OpenAI API")
    else:
        print("\nYou're using Azure OpenAI API")
    
    print("\nYou're ready to use AI-powered content generation!")
    print("Run: python app.py")
    
    return True


if __name__ == "__main__":
    success = test_openai_setup()
    sys.exit(0 if success else 1)
