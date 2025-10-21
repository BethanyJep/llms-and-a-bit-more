"""
Test YouTube Integration
Quick test to verify YouTube transcript extraction works
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from youtube_processor import YouTubeProcessor


def test_youtube_url_extraction():
    """Test various YouTube URL formats."""
    print("Testing YouTube URL extraction...")
    
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "youtube.com/watch?v=dQw4w9WgXcQ"
    ]
    
    for url in test_urls:
        video_id = YouTubeProcessor.extract_video_id(url)
        status = "✓" if video_id == "dQw4w9WgXcQ" else "✗"
        print(f"{status} {url} -> {video_id}")
    
    print()


def test_youtube_processing():
    """Test full YouTube processing with a real video."""
    print("Testing YouTube processing with a real video...")
    print("-" * 60)
    
    # Using a popular TED talk with captions (adjust if needed)
    test_url = "https://www.youtube.com/watch?v=8jPQjjsBbIc"
    
    try:
        print(f"URL: {test_url}")
        print("Extracting video ID...")
        
        video_id = YouTubeProcessor.extract_video_id(test_url)
        print(f"✓ Video ID: {video_id}\n")
        
        print("Fetching video metadata...")
        metadata = YouTubeProcessor.get_video_metadata(video_id)
        print(f"✓ Title: {metadata['title']}")
        print(f"✓ Author: {metadata['author']}")
        print(f"✓ Length: {metadata['length']} seconds\n")
        
        print("Extracting transcript (this may take a moment)...")
        raw_transcript = YouTubeProcessor.get_transcript(video_id)
        print(f"✓ Transcript entries: {len(raw_transcript)}")
        print(f"✓ First entry: {raw_transcript[0]}\n")
        
        print("Segmenting transcript...")
        segments = YouTubeProcessor.segment_transcript(raw_transcript, segment_duration=120)
        print(f"✓ Total segments: {len(segments)}")
        print(f"✓ First segment: {segments[0]['text'][:100]}...\n")
        
        print("Processing full YouTube URL...")
        transcript_data = YouTubeProcessor.process_youtube_url(test_url)
        
        print("=" * 60)
        print("✅ YouTube Processing Successful!")
        print("=" * 60)
        print(f"Event Name: {transcript_data['event_name']}")
        print(f"Duration: {transcript_data['duration_formatted']}")
        print(f"Total Segments: {transcript_data['total_segments']}")
        print(f"Total Words: {transcript_data['total_words']}")
        print(f"\nFirst segment:")
        print(f"  Timestamp: {transcript_data['segments'][0]['timestamp']}")
        print(f"  Speaker: {transcript_data['segments'][0]['speaker']}")
        print(f"  Text: {transcript_data['segments'][0]['text'][:200]}...")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"\nNote: This might happen if:")
        print("  - The video has no captions")
        print("  - The video is private or restricted")
        print("  - Network connection issues")
        print("\nTry a different YouTube URL with captions enabled.")
        return False


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("YouTube Integration Test")
    print("=" * 60 + "\n")
    
    # Test URL extraction
    test_youtube_url_extraction()
    
    # Test full processing
    print("Note: The following test requires internet connection")
    print("and will attempt to process a real YouTube video.\n")
    
    input("Press Enter to continue with live test...")
    print()
    
    success = test_youtube_processing()
    
    if success:
        print("\n✅ All tests passed! YouTube integration is working.")
        print("\nYou can now:")
        print("1. Run 'python app.py' to start the web server")
        print("2. Open http://localhost:5001 in your browser")
        print("3. Paste any YouTube URL to generate PR content")
    else:
        print("\n⚠️  Test failed. Check the error message above.")
        print("Try with a different YouTube video that has captions.")
