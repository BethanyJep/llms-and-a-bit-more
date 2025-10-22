"""
AI-powered content generation using Azure OpenAI
"""
import os
import json
from typing import List, Dict
from pathlib import Path
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Global client instance
client = None
deployment_name = None
use_azure = True


def initialize_openai():
    """Initialize OpenAI client with credentials from .env file."""
    global client, deployment_name, use_azure
    
    # Check if we should use regular OpenAI or Azure OpenAI
    use_openai = os.environ.get("USE_OPENAI", "false").lower() == "true"
    
    if use_openai:
        # Use regular OpenAI
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in .env file. "
                "Please add it to your .env file or set USE_OPENAI=false to use Azure OpenAI."
            )
        
        client = OpenAI(api_key=api_key)
        deployment_name = "gpt-4o-mini"  # Use model name directly for OpenAI
        use_azure = False
        print("✅ Using OpenAI API")
        
    else:
        # Use Azure OpenAI (default)
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        # Validate required variables
        missing_vars = []
        if not api_key:
            missing_vars.append("AZURE_OPENAI_API_KEY")
        if not endpoint:
            missing_vars.append("AZURE_OPENAI_ENDPOINT")
        if not deployment_name:
            missing_vars.append("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables in .env file: {', '.join(missing_vars)}\n"
                "Please copy .env.example to .env and fill in your Azure OpenAI credentials."
            )
        
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
        use_azure = True
        print(f"✅ Using Azure OpenAI - Endpoint: {endpoint}")
        print(f"   Deployment: {deployment_name}")
    
    return client


def generate_press_quotes_ai(transcript_data: Dict) -> List[Dict]:
    """
    Use AI to extract the most impactful press quotes from the transcript.
    
    Args:
        transcript_data: Full transcript with metadata and segments
    
    Returns:
        List of formatted quotes with speaker attribution
    """
    if client is None:
        initialize_openai()
    
    event_name = transcript_data.get("event_metadata", {}).get("event_name", "the event")
    segments = transcript_data.get("transcript_segments", [])
    
    # Optimize: Sample key segments for faster processing
    total_segments = len(segments)
    if total_segments > 30:
        # Sample evenly throughout transcript to capture key moments
        step = max(1, total_segments // 30)
        sampled_segments = segments[::step][:30]
    else:
        sampled_segments = segments
    
    # Create a condensed transcript for the AI
    transcript_text = "\n\n".join([
        f"[{seg['timestamp']}] {seg['speaker']}: {seg['text']}"
        for seg in sampled_segments
    ])
    
    prompt = f"""Analyze this event transcript and extract 5-8 of the most impactful, quotable statements that would work well in a press release.

Event: {event_name}

Transcript:
{transcript_text}

For each quote, provide:
1. The exact quote text (should be impactful and newsworthy)
2. The speaker's name
3. Why this quote is significant
4. The category (announcement/insight/vision/technical)

Return a JSON array of quotes in this format:
[
  {{
    "text": "exact quote text",
    "speaker": "speaker name",
    "significance": "why this matters",
    "category": "category",
    "timestamp": "timestamp from transcript"
  }}
]
"""
    
    response = client.chat.completions.create(
        model=deployment_name,  # Use deployment name from .env
        messages=[
            {"role": "system", "content": "You are an expert PR specialist who extracts compelling quotes from event transcripts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    
    result = json.loads(response.choices[0].message.content)
    return result.get("quotes", [])


def generate_social_posts_ai(transcript_data: Dict, platform: str) -> List[Dict]:
    """
    Use AI to generate engaging social media posts for the specified platform.
    
    Args:
        transcript_data: Full transcript with metadata and segments
        platform: Social media platform (twitter, linkedin, instagram)
    
    Returns:
        List of platform-optimized social media posts
    """
    if client is None:
        initialize_openai()
    
    event_name = transcript_data.get("event_metadata", {}).get("event_name", "the event")
    segments = transcript_data.get("transcript_segments", [])
    
    # Create a condensed transcript
    transcript_text = "\n\n".join([
        f"{seg['speaker']}: {seg['text']}"
        for seg in segments[:20]  # Use first 20 segments to stay within token limits
    ])
    
    platform_specs = {
        "twitter": {
            "char_limit": 280,
            "count": 5,
            "style": "concise, engaging, use emojis, 2-3 hashtags",
            "format": "Thread-worthy tweets highlighting key points"
        },
        "linkedin": {
            "char_limit": 3000,
            "count": 2,
            "style": "professional, thought-leadership, industry insights",
            "format": "Long-form posts with bullet points and professional tone"
        },
        "instagram": {
            "char_limit": 2200,
            "count": 2,
            "style": "visual-friendly, storytelling, 5-8 hashtags",
            "format": "Caption for carousel post with engaging narrative"
        }
    }
    
    spec = platform_specs.get(platform, platform_specs["twitter"])
    
    prompt = f"""Create {spec['count']} engaging {platform} posts based on this event transcript.

Event: {event_name}

Transcript Summary:
{transcript_text}

Requirements:
- Style: {spec['style']}
- Character limit: {spec['char_limit']}
- Format: {spec['format']}
- Extract the most interesting, shareable insights
- Make it authentic and engaging for {platform} audience

Return a JSON array of posts:
[
  {{
    "content": "full post text",
    "hashtags": ["hashtag1", "hashtag2"],
    "hook": "what makes this post engaging",
    "character_count": 123
  }}
]
"""
    
    response = client.chat.completions.create(
        model=deployment_name,  # Use deployment name from .env
        messages=[
            {"role": "system", "content": f"You are a social media expert specializing in {platform} content strategy."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        response_format={"type": "json_object"}
    )
    
    result = json.loads(response.choices[0].message.content)
    posts = result.get("posts", [])
    
    # Add platform metadata
    for post in posts:
        post["platform"] = platform
    
    return posts


def generate_press_release_ai(transcript_data: Dict, company_info: Dict = None, media_contact: Dict = None) -> str:
    """
    Use AI to generate a complete press release from the event transcript.
    
    Args:
        transcript_data: Full transcript with metadata and segments
        company_info: Optional company information (will be extracted from transcript if not provided)
        media_contact: Optional media contact details (will be omitted if not provided)
    
    Returns:
        Formatted press release text
    """
    if client is None:
        initialize_openai()
    
    event_name = transcript_data.get("event_metadata", {}).get("event_name", "Event")
    event_date = transcript_data.get("event_metadata", {}).get("date", "")
    segments = transcript_data.get("transcript_segments", [])
    
    # Optimize: Sample key segments for faster processing
    total_segments = len(segments)
    if total_segments > 35:
        step = max(1, total_segments // 35)
        sampled_segments = segments[::step][:35]
    else:
        sampled_segments = segments
    
    # Create condensed transcript
    transcript_text = "\n\n".join([
        f"{seg['speaker']}: {seg['text']}"
        for seg in sampled_segments
    ])
    
    prompt = f"""Write a professional press release based on this event transcript.

Event: {event_name}
Date: {event_date}

Transcript:
{transcript_text}

Press Release Requirements:
1. Start with "FOR IMMEDIATE RELEASE"
2. Compelling headline based on the event
3. Strong opening paragraph with the main news
4. 2-3 compelling quotes from speakers (use exact quotes from transcript)
5. Key highlights and announcements from the event
6. Brief context about the event/organization (extract from transcript, don't make up information)
7. Professional closing

IMPORTANT:
- Extract company/organization names directly from the transcript
- Do NOT include made-up company history or descriptions
- Focus on the actual event content and announcements
- Only include information that is present in the transcript
- If media contact info is needed, indicate "For media inquiries, please contact [organization]"

Format it professionally with proper spacing and structure."""
    
    response = client.chat.completions.create(
        model=deployment_name,  # Use deployment name from .env
        messages=[
            {"role": "system", "content": "You are an expert PR professional who writes compelling press releases."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    return response.choices[0].message.content


def generate_newsletter_ai(transcript_data: Dict, company_info: Dict = None, media_contact: Dict = None) -> str:
    """
    Use AI to generate an engaging newsletter recap of the event.
    
    Args:
        transcript_data: Full transcript with metadata and segments
        company_info: Optional company information (will be extracted from transcript if not provided)
        media_contact: Optional media contact details (will be omitted if not provided)
    
    Returns:
        Formatted newsletter text
    """
    if client is None:
        initialize_openai()
    
    event_name = transcript_data.get("event_metadata", {}).get("event_name", "Event")
    segments = transcript_data.get("transcript_segments", [])
    
    # Optimize: Sample key segments for faster processing
    total_segments = len(segments)
    if total_segments > 35:
        step = max(1, total_segments // 35)
        sampled_segments = segments[::step][:35]
    else:
        sampled_segments = segments
    
    # Create summary of transcript
    transcript_text = "\n\n".join([
        f"{seg['speaker']}: {seg['text']}"
        for seg in sampled_segments
    ])
    
    prompt = f"""Create an engaging post-event newsletter recap based on this event transcript.

Event: {event_name}

Transcript:
{transcript_text}

Newsletter Structure:
1. Warm greeting header
2. Executive summary (2-3 paragraphs)
3. Key highlights section (5-7 bullet points)
4. 2-3 memorable quotes with attribution
5. Topics covered
6. Next steps/call to action (based on content)
7. Professional closing

IMPORTANT:
- Extract organization/company names directly from the transcript
- Do NOT include made-up company history, descriptions, or contact information
- Focus on the actual event content and key takeaways
- Only include information that is present in the transcript
- Make it conversational and engaging for subscribers

Make it conversational, engaging, and valuable for subscribers."""
    
    response = client.chat.completions.create(
        model=deployment_name,  # Use deployment name from .env
        messages=[
            {"role": "system", "content": "You are an expert email marketer who creates engaging newsletter content."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=2000
    )
    
    return response.choices[0].message.content
