#!/usr/bin/env python3
"""
Quick test to verify the YouTube transcript fix works
"""
import asyncio
import sys
import json
sys.path.insert(0, 'src')

from server import extract_press_quotes, set_transcript_file
from dotenv import load_dotenv

load_dotenv()

async def test_youtube_content_generation():
    """Test that AI can generate content from YouTube transcript."""
    
    print("=" * 60)
    print("🧪 Testing YouTube Content Generation Fix")
    print("=" * 60)
    
    # Set transcript file to YouTube video (not mock)
    print("\n1️⃣ Setting transcript file to youtube_transcript.json...")
    set_transcript_file('youtube_transcript.json')
    print("   ✅ Transcript file set")
    
    # Generate quotes from YouTube video
    print("\n2️⃣ Generating press quotes from YouTube video...")
    result = await extract_press_quotes()
    data = json.loads(result)
    
    print(f"\n3️⃣ Results:")
    print(f"   Status: {data.get('status')}")
    
    if data.get('status') == 'error':
        print(f"   ❌ ERROR: {data.get('message')}")
        return False
    
    print(f"   ✅ Total quotes: {data.get('total_quotes')}")
    print(f"   ✅ AI Generated: {data.get('ai_generated')}")
    
    if data.get('quotes'):
        print(f"\n📝 Sample Quote:")
        quote = data['quotes'][0]
        print(f"   Speaker: {quote.get('speaker')}")
        print(f"   Quote: {quote.get('quote')[:150]}...")
        print(f"   Context: {quote.get('context', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("✅ TEST PASSED - YouTube content generation works!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    success = loop.run_until_complete(test_youtube_content_generation())
    loop.close()
    
    sys.exit(0 if success else 1)
