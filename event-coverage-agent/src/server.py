"""
Event Coverage Agent
MCP Server for automated event transcription and content generation
"""
import json
from datetime import datetime
from typing import List, Dict
from mcp.server.fastmcp import FastMCP

from utils import (
    load_json_file,
    get_data_path,
    get_config_path,
    extract_key_quotes,
    identify_key_highlights,
    extract_statistics,
    generate_hashtags,
    format_quote_with_attribution,
    categorize_segments_by_type,
    create_executive_summary,
    extract_speaker_info
)

# Create MCP server
server = FastMCP("event_coverage_agent")

# Load configuration
templates = load_json_file(get_config_path('content_templates.json'))
settings = load_json_file(get_config_path('settings.json'))

# Configuration constants
COMPANY_INFO = settings["company_info"]
MEDIA_CONTACT = settings["media_contact"]
QUOTE_CRITERIA = templates["quote_selection_criteria"]
HIGHLIGHT_KEYWORDS = templates["highlight_keywords"]

# Global state for current transcript file
CURRENT_TRANSCRIPT_FILE = "mock_transcript.json"


def set_transcript_file(event_file: str):
    """Set the current transcript file to use."""
    global CURRENT_TRANSCRIPT_FILE
    CURRENT_TRANSCRIPT_FILE = event_file


def load_event_transcript(event_file: str = None) -> Dict:
    """Load event transcript from JSON file."""
    if event_file is None:
        event_file = CURRENT_TRANSCRIPT_FILE
    return load_json_file(get_data_path(event_file))


@server.tool()
async def process_event_transcript(event_file: str = "mock_transcript.json") -> str:
    """
    Process event audio transcript and extract structured data.
    In production, this would integrate with speech-to-text services.
    
    Args:
        event_file: Name of the transcript JSON file in data folder
    """
    try:
        # Set the global transcript file so other tools use it too
        set_transcript_file(event_file)
        
        transcript_data = load_event_transcript(event_file)
        
        metadata = transcript_data.get("event_metadata", {})
        segments = transcript_data.get("transcript_segments", [])
        
        # Extract key information
        speakers = extract_speaker_info(segments)
        categorized = categorize_segments_by_type(segments)
        
        result = {
            "status": "success",
            "event_name": metadata.get("event_name"),
            "date": metadata.get("date"),
            "duration_minutes": metadata.get("duration_minutes"),
            "total_segments": len(segments),
            "speakers": speakers,
            "categories": {cat: len(segs) for cat, segs in categorized.items()},
            "transcript_processed": True,
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@server.tool()
async def extract_press_quotes() -> str:
    """
    Extract press-ready quotes from event transcript.
    Selects the most impactful, quotable statements from speakers.
    """
    try:
        transcript_data = load_event_transcript()
        segments = transcript_data.get("transcript_segments", [])
        metadata = transcript_data.get("event_metadata", {})
        
        # Extract key quotes
        quotes = extract_key_quotes(segments, QUOTE_CRITERIA)
        
        # Format quotes with proper attribution
        formatted_quotes = []
        for quote in quotes:
            # Find speaker role from metadata
            speaker_role = "Speaker"
            for speaker_info in metadata.get("speakers", []):
                if speaker_info["name"] == quote["speaker"]:
                    speaker_role = speaker_info["role"]
                    break
            
            formatted_quotes.append({
                "quote": quote["text"],
                "speaker": quote["speaker"],
                "role": speaker_role,
                "timestamp": quote["timestamp"],
                "category": quote["category"],
                "formatted": f'"{quote["text"]}" - {quote["speaker"]}, {speaker_role}'
            })
        
        result = {
            "status": "success",
            "event_name": metadata.get("event_name"),
            "total_quotes": len(formatted_quotes),
            "quotes": formatted_quotes,
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@server.tool()
async def generate_social_media_posts(platform: str = "twitter") -> str:
    """
    Generate platform-specific social media posts from event highlights.
    
    Args:
        platform: Social media platform (twitter, linkedin, instagram)
    """
    try:
        transcript_data = load_event_transcript()
        segments = transcript_data.get("transcript_segments", [])
        metadata = transcript_data.get("event_metadata", {})
        event_name = metadata.get("event_name", "Event")
        
        # Identify highlights
        highlights = identify_key_highlights(segments, HIGHLIGHT_KEYWORDS)
        
        # Get platform specifications
        platform_specs = templates["social_media"].get(platform, templates["social_media"]["twitter"])
        
        posts = []
        
        if platform == "twitter":
            # Generate concise Twitter posts
            for i, highlight in enumerate(highlights[:5]):  # Max 5 posts
                # Extract key point
                text = highlight["text"]
                
                # Check for statistics
                stats = extract_statistics(text)
                
                # Generate hashtags
                hashtags = generate_hashtags(text, event_name, 3)
                
                # Create tweet (under 280 chars)
                if stats:
                    tweet = f"🚀 {text[:200]}... {' '.join(hashtags)}"
                else:
                    tweet = f"💡 {text[:220]} {' '.join(hashtags)}"
                
                # Ensure under limit
                if len(tweet) > 280:
                    tweet = tweet[:270] + "... " + hashtags[-1]
                
                posts.append({
                    "platform": "twitter",
                    "content": tweet,
                    "character_count": len(tweet),
                    "hashtags": hashtags,
                    "source_timestamp": highlight["timestamp"]
                })
        
        elif platform == "linkedin":
            # Generate professional LinkedIn posts
            exec_summary = create_executive_summary(segments, 3)
            
            # Get key quotes
            quotes = extract_key_quotes(segments, QUOTE_CRITERIA)[:2]
            
            # Create LinkedIn post
            post_content = f"🎉 Highlights from {event_name}\n\n"
            post_content += f"{exec_summary}\n\n"
            post_content += "Key Takeaways:\n"
            
            for i, highlight in enumerate(highlights[:3]):
                post_content += f"• {highlight['text'].split('.')[0]}\n"
            
            if quotes:
                post_content += f"\n💬 {format_quote_with_attribution(quotes[0], 'full')}\n"
            
            post_content += f"\n{' '.join(generate_hashtags(exec_summary, event_name, 3))}"
            
            posts.append({
                "platform": "linkedin",
                "content": post_content,
                "character_count": len(post_content),
                "style": "professional"
            })
        
        elif platform == "instagram":
            # Generate visual-friendly Instagram captions
            exec_summary = create_executive_summary(segments, 2)
            
            caption = f"✨ {event_name} ✨\n\n"
            caption += f"{exec_summary}\n\n"
            caption += "Swipe to see the highlights! 👉\n\n"
            caption += ' '.join(generate_hashtags(exec_summary, event_name, 5))
            
            posts.append({
                "platform": "instagram",
                "content": caption,
                "character_count": len(caption),
                "style": "visual-friendly",
                "note": "Pair with event photos/graphics"
            })
        
        result = {
            "status": "success",
            "platform": platform,
            "posts_generated": len(posts),
            "posts": posts,
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@server.tool()
async def create_press_release() -> str:
    """
    Generate a complete press release from event transcript.
    """
    try:
        transcript_data = load_event_transcript()
        segments = transcript_data.get("transcript_segments", [])
        metadata = transcript_data.get("event_metadata", {})
        event_name = metadata.get("event_name", "Event")
        
        # Get key elements
        announcements = [s for s in segments if s.get("category") == "announcement"]
        quotes = extract_key_quotes(segments, QUOTE_CRITERIA)
        highlights = identify_key_highlights(segments, HIGHLIGHT_KEYWORDS)
        
        # Build press release
        press_release = f"FOR IMMEDIATE RELEASE\n\n"
        press_release += f"{event_name}\n"
        press_release += f"{COMPANY_INFO['tagline']}\n\n"
        
        # Date and location
        press_release += f"{metadata.get('date')} - "
        
        # Main announcement
        if announcements:
            main_announcement = announcements[0]["text"]
            press_release += f"{COMPANY_INFO['name']} today {main_announcement}\n\n"
        
        # CEO quote
        if quotes:
            ceo_quote = quotes[0]
            press_release += f'"{ceo_quote["text"]}" said {ceo_quote["speaker"]}.\n\n'
        
        # Key highlights
        press_release += "Event Highlights:\n"
        for i, highlight in enumerate(highlights[:4], 1):
            press_release += f"• {highlight['text'].split('.')[0]}\n"
        
        press_release += "\n"
        
        # Additional quotes
        if len(quotes) > 1:
            press_release += "Industry Response:\n"
            for quote in quotes[1:3]:
                press_release += f'"{quote["text"]}" - {quote["speaker"]}\n\n'
        
        # About company
        press_release += f"About {COMPANY_INFO['name']}:\n"
        press_release += f"{COMPANY_INFO['description']}\n\n"
        
        # Media contact
        press_release += "Media Contact:\n"
        press_release += f"{MEDIA_CONTACT['name']}, {MEDIA_CONTACT['title']}\n"
        press_release += f"{MEDIA_CONTACT['email']}\n"
        press_release += f"{MEDIA_CONTACT['phone']}\n"
        
        result = {
            "status": "success",
            "event_name": event_name,
            "press_release": press_release,
            "word_count": len(press_release.split()),
            "quotes_included": len(quotes),
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@server.tool()
async def generate_newsletter_recap() -> str:
    """
    Generate a post-event newsletter/email recap.
    """
    try:
        transcript_data = load_event_transcript()
        segments = transcript_data.get("transcript_segments", [])
        metadata = transcript_data.get("event_metadata", {})
        event_name = metadata.get("event_name", "Event")
        
        # Get key content
        exec_summary = create_executive_summary(segments, 4)
        quotes = extract_key_quotes(segments, QUOTE_CRITERIA)
        highlights = identify_key_highlights(segments, HIGHLIGHT_KEYWORDS)
        categorized = categorize_segments_by_type(segments)
        
        # Build newsletter
        newsletter = f"📧 {event_name} - Post-Event Recap\n\n"
        newsletter += "=" * 60 + "\n\n"
        
        # Header
        newsletter += f"Dear Subscriber,\n\n"
        newsletter += f"Thank you for your interest in {event_name}. "
        newsletter += "Here's your comprehensive recap of this exciting event.\n\n"
        
        # Executive Summary
        newsletter += "📊 EXECUTIVE SUMMARY\n"
        newsletter += "-" * 60 + "\n"
        newsletter += f"{exec_summary}\n\n"
        
        # Key Highlights
        newsletter += "✨ KEY HIGHLIGHTS\n"
        newsletter += "-" * 60 + "\n"
        for i, highlight in enumerate(highlights[:5], 1):
            newsletter += f"{i}. {highlight['text']}\n"
            newsletter += f"   - {highlight['speaker']} at {highlight['timestamp']}\n\n"
        
        # Memorable Quotes
        newsletter += "💬 MEMORABLE QUOTES\n"
        newsletter += "-" * 60 + "\n"
        for quote in quotes[:3]:
            newsletter += f'"{quote["text"]}"\n'
            newsletter += f"   - {quote['speaker']}\n\n"
        
        # By Category
        newsletter += "📁 TOPICS COVERED\n"
        newsletter += "-" * 60 + "\n"
        for category, segs in categorized.items():
            newsletter += f"• {category.title()}: {len(segs)} segments\n"
        newsletter += "\n"
        
        # Next Steps
        newsletter += "🚀 NEXT STEPS\n"
        newsletter += "-" * 60 + "\n"
        newsletter += f"• Visit {COMPANY_INFO['website']} for more information\n"
        newsletter += f"• Follow us on Twitter: {COMPANY_INFO['social_handles']['twitter']}\n"
        newsletter += f"• Contact us: {MEDIA_CONTACT['email']}\n\n"
        
        # Footer
        newsletter += "-" * 60 + "\n"
        newsletter += f"© 2025 {COMPANY_INFO['name']}. All rights reserved.\n"
        newsletter += "This is an automated recap generated from event transcription.\n"
        
        result = {
            "status": "success",
            "event_name": event_name,
            "newsletter": newsletter,
            "sections": ["summary", "highlights", "quotes", "topics", "next_steps"],
            "word_count": len(newsletter.split()),
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@server.tool()
async def run_full_coverage_cycle() -> str:
    """
    Run complete event coverage workflow:
    1. Process transcript
    2. Extract quotes
    3. Generate social posts
    4. Create press release
    5. Generate newsletter
    """
    print("🎤 Starting full event coverage cycle...")
    
    try:
        # Step 1: Process transcript
        print("📝 Processing transcript...")
        transcript_result = await process_event_transcript()
        
        # Step 2: Extract quotes
        print("💬 Extracting press quotes...")
        quotes_result = await extract_press_quotes()
        
        # Step 3: Generate social posts
        print("📱 Generating social media posts...")
        twitter_posts = await generate_social_media_posts("twitter")
        linkedin_posts = await generate_social_media_posts("linkedin")
        
        # Step 4: Create press release
        print("📰 Creating press release...")
        press_release = await create_press_release()
        
        # Step 5: Generate newsletter
        print("📧 Generating newsletter recap...")
        newsletter = await generate_newsletter_recap()
        
        # Compile results
        final_result = {
            "status": "success",
            "coverage_complete": True,
            "timestamp": datetime.now().isoformat(),
            "outputs": {
                "transcript_analysis": json.loads(transcript_result),
                "press_quotes": json.loads(quotes_result),
                "social_media": {
                    "twitter": json.loads(twitter_posts),
                    "linkedin": json.loads(linkedin_posts)
                },
                "press_release": json.loads(press_release),
                "newsletter": json.loads(newsletter)
            }
        }
        
        print("✅ Full coverage cycle complete!")
        
        return json.dumps(final_result, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


if __name__ == "__main__":
    # Run the server
    server.run()
