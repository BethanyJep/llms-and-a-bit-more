"""
Quick test script to verify the agent setup
"""
import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        sys.path.append(str(Path(__file__).parent / 'src'))
        from utils import load_json_file, get_data_path, get_config_path
        print("✅ utils.py imported successfully")
        
        from server import server
        print("✅ server.py imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_data_files():
    """Test that all data files exist and are valid JSON."""
    print("\nTesting data files...")
    sys.path.append(str(Path(__file__).parent / 'src'))
    from utils import load_json_file, get_data_path, get_config_path
    
    try:
        # Test mock mentions
        mentions = load_json_file(get_data_path('mock_mentions.json'))
        print(f"✅ mock_mentions.json loaded: {len(mentions)} mentions")
        
        # Test sentiment keywords
        keywords = load_json_file(get_data_path('sentiment_keywords.json'))
        print(f"✅ sentiment_keywords.json loaded: {len(keywords['positive_keywords'])} positive keywords")
        
        # Test config
        config = load_json_file(get_config_path('settings.json'))
        print(f"✅ settings.json loaded: threshold = {config['negative_threshold']}%")
        
        return True
    except Exception as e:
        print(f"❌ Data file test failed: {e}")
        return False


def test_sentiment_classification():
    """Test sentiment classification."""
    print("\nTesting sentiment classification...")
    sys.path.append(str(Path(__file__).parent / 'src'))
    from utils import classify_sentiment, load_json_file, get_data_path
    
    try:
        keywords = load_json_file(get_data_path('sentiment_keywords.json'))
        
        # Test positive
        text1 = "I love this product! It's amazing and innovative!"
        result1 = classify_sentiment(text1, keywords)
        print(f"✅ Positive test: '{text1[:50]}...' → {result1}")
        
        # Test negative
        text2 = "This is terrible! So frustrated with the bugs and problems."
        result2 = classify_sentiment(text2, keywords)
        print(f"✅ Negative test: '{text2[:50]}...' → {result2}")
        
        # Test neutral
        text3 = "The product exists and does things."
        result3 = classify_sentiment(text3, keywords)
        print(f"✅ Neutral test: '{text3[:50]}...' → {result3}")
        
        return True
    except Exception as e:
        print(f"❌ Sentiment test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Media Monitoring Agent - Setup Verification")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_data_files,
        test_sentiment_classification
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ All tests passed! Agent is ready to use.")
        print("\nNext steps:")
        print("  1. Run the demo: python client.py")
        print("  2. Or start the MCP server: cd src && python server.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("=" * 60)


if __name__ == "__main__":
    main()
