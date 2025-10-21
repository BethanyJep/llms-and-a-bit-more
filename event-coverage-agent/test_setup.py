"""
Quick test script to verify the Event Coverage Agent setup
"""
import sys
from pathlib import Path


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        sys.path.append(str(Path(__file__).parent / 'src'))
        from utils import (
            load_json_file, 
            extract_key_quotes,
            generate_hashtags
        )
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
        # Test transcript
        transcript = load_json_file(get_data_path('mock_transcript.json'))
        print(f"✅ mock_transcript.json loaded: {len(transcript['transcript_segments'])} segments")
        
        # Test templates
        templates = load_json_file(get_config_path('content_templates.json'))
        print(f"✅ content_templates.json loaded: {len(templates)} sections")
        
        # Test settings
        settings = load_json_file(get_config_path('settings.json'))
        print(f"✅ settings.json loaded: {settings['company_info']['name']}")
        
        return True
    except Exception as e:
        print(f"❌ Data file test failed: {e}")
        return False


def test_quote_extraction():
    """Test quote extraction functionality."""
    print("\nTesting quote extraction...")
    sys.path.append(str(Path(__file__).parent / 'src'))
    from utils import extract_key_quotes, load_json_file, get_data_path, get_config_path
    
    try:
        transcript = load_json_file(get_data_path('mock_transcript.json'))
        templates = load_json_file(get_config_path('content_templates.json'))
        
        segments = transcript['transcript_segments']
        criteria = templates['quote_selection_criteria']
        
        quotes = extract_key_quotes(segments, criteria)
        print(f"✅ Extracted {len(quotes)} press-ready quotes")
        
        if quotes:
            print(f"   Sample: \"{quotes[0]['text'][:60]}...\"")
        
        return True
    except Exception as e:
        print(f"❌ Quote extraction test failed: {e}")
        return False


def test_hashtag_generation():
    """Test hashtag generation."""
    print("\nTesting hashtag generation...")
    sys.path.append(str(Path(__file__).parent / 'src'))
    from utils import generate_hashtags
    
    try:
        text = "Today we're launching our innovative AI platform for enterprises"
        hashtags = generate_hashtags(text, "TechCorp Launch", 3)
        print(f"✅ Generated hashtags: {' '.join(hashtags)}")
        
        return True
    except Exception as e:
        print(f"❌ Hashtag generation test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("🧪 Event Coverage Agent - Setup Verification")
    print("=" * 70)
    
    tests = [
        test_imports,
        test_data_files,
        test_quote_extraction,
        test_hashtag_generation
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 70)
    if all(results):
        print("✅ All tests passed! Agent is ready to use.")
        print("\nNext steps:")
        print("  1. Run the demo: python client.py")
        print("  2. Or start the MCP server: cd src && python server.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("=" * 70)


if __name__ == "__main__":
    main()
