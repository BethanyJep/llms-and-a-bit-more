"""
Event Coverage Agent
MCP Server for automated event transcription and content generation
"""
import json
import asyncio
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

# Import AI generation functions
from ai_generator import (
    initialize_openai,
    generate_press_quotes_ai,
    generate_social_posts_ai,
    generate_press_release_ai,
    generate_newsletter_ai
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
    Extract press-ready quotes from event transcript using AI.
    Uses OpenAI to identify the most impactful, quotable statements from speakers.
    """
    try:
        # Initialize OpenAI client
        try:
            initialize_openai()
        except ValueError as e:
            return json.dumps({
                "status": "error",
                "message": f"AI configuration error: {str(e)}\nPlease check your .env file."
            })
        
        transcript_data = load_event_transcript()
        metadata = transcript_data.get("event_metadata", {})
        
        # Use AI to extract quotes
        print("🤖 Using AI to extract press quotes...")
        ai_quotes = generate_press_quotes_ai(transcript_data)
        
        # Format quotes with proper attribution
        formatted_quotes = []
        for quote in ai_quotes:
            formatted_quotes.append({
                "quote": quote.get("text"),
                "speaker": quote.get("speaker"),
                "role": quote.get("role", "Speaker"),
                "timestamp": quote.get("timestamp", ""),
                "category": quote.get("category", "general"),
                "significance": quote.get("significance", ""),
                "formatted": f'"{quote.get("text")}" - {quote.get("speaker")}'
            })
        
        result = {
            "status": "success",
            "event_name": metadata.get("event_name"),
            "total_quotes": len(formatted_quotes),
            "quotes": formatted_quotes,
            "ai_generated": True,
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@server.tool()
async def generate_social_media_posts(platform: str = "twitter") -> str:
    """
    Generate platform-specific social media posts from event highlights using AI.
    
    Args:
        platform: Social media platform (twitter, linkedin, instagram)
    """
    try:
        # Initialize OpenAI client
        try:
            initialize_openai()
        except ValueError as e:
            return json.dumps({
                "status": "error",
                "message": f"AI configuration error: {str(e)}\nPlease check your .env file."
            })
        
        transcript_data = load_event_transcript()
        metadata = transcript_data.get("event_metadata", {})
        
        # Use AI to generate posts
        print(f"🤖 Using AI to generate {platform} posts...")
        ai_posts = generate_social_posts_ai(transcript_data, platform)
        
        result = {
            "status": "success",
            "platform": platform,
            "posts_generated": len(ai_posts),
            "posts": ai_posts,
            "ai_generated": True,
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@server.tool()
async def create_press_release() -> str:
    """
    Generate a complete press release from event transcript using AI.
    """
    try:
        # Initialize OpenAI client
        try:
            initialize_openai()
        except ValueError as e:
            return json.dumps({
                "status": "error",
                "message": f"AI configuration error: {str(e)}\nPlease check your .env file."
            })
        
        transcript_data = load_event_transcript()
        metadata = transcript_data.get("event_metadata", {})
        event_name = metadata.get("event_name", "Event")
        
        # Use AI to generate press release (company info extracted from transcript)
        print("🤖 Using AI to generate press release...")
        press_release = generate_press_release_ai(transcript_data)
        
        result = {
            "status": "success",
            "event_name": event_name,
            "press_release": press_release,
            "word_count": len(press_release.split()),
            "ai_generated": True,
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@server.tool()
async def generate_newsletter_recap() -> str:
    """
    Generate a post-event newsletter/email recap using AI.
    """
    try:
        # Initialize OpenAI client
        try:
            initialize_openai()
        except ValueError as e:
            return json.dumps({
                "status": "error",
                "message": f"AI configuration error: {str(e)}\nPlease check your .env file."
            })
        
        transcript_data = load_event_transcript()
        metadata = transcript_data.get("event_metadata", {})
        event_name = metadata.get("event_name", "Event")
        
        # Use AI to generate newsletter (company info extracted from transcript)
        print("🤖 Using AI to generate newsletter...")
        newsletter = generate_newsletter_ai(transcript_data)
        
        result = {
            "status": "success",
            "event_name": event_name,
            "newsletter": newsletter,
            "word_count": len(newsletter.split()),
            "ai_generated": True,
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@server.tool()
async def run_full_coverage_cycle(skip_transcript_processing: bool = False) -> str:
    """
    Run complete event coverage workflow with parallel processing for speed:
    1. Process transcript (optional, can be skipped if already processed)
    2. Generate all content in parallel (quotes, social, press release, newsletter)
    
    Args:
        skip_transcript_processing: If True, skip transcript processing and use current global state
    """
    print("🎤 Starting full event coverage cycle...")
    
    try:
        # Step 1: Process transcript (optional)
        if skip_transcript_processing:
            print(f"📝 Using already processed transcript: {CURRENT_TRANSCRIPT_FILE}")
            # Just load it for the result
            transcript_data = load_event_transcript()
            transcript_result = json.dumps({
                "status": "success",
                "event_name": transcript_data.get("event_metadata", {}).get("event_name"),
                "transcript_file": CURRENT_TRANSCRIPT_FILE
            })
        else:
            print("📝 Processing transcript...")
            transcript_result = await process_event_transcript()
        
        # Step 2-5: Generate all content in parallel for maximum speed
        print("� Generating all content in parallel...")
        
        # Run all AI generation tasks simultaneously
        quotes_task = extract_press_quotes()
        twitter_task = generate_social_media_posts("twitter")
        linkedin_task = generate_social_media_posts("linkedin")
        press_task = create_press_release()
        newsletter_task = generate_newsletter_recap()
        
        # Wait for all tasks to complete in parallel
        quotes_result, twitter_posts, linkedin_posts, press_release, newsletter = await asyncio.gather(
            quotes_task,
            twitter_task,
            linkedin_task,
            press_task,
            newsletter_task
        )
        
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
