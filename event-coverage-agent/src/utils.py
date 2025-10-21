"""
Utility functions for the Event Coverage Agent
"""
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime


def load_json_file(file_path: str) -> dict | list:
    """Load and parse a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(data: dict | list, file_path: str) -> None:
    """Save data to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_data_path(filename: str) -> Path:
    """Get the path to a data file."""
    return Path(__file__).parent.parent / 'data' / filename


def get_config_path(filename: str) -> Path:
    """Get the path to a config file."""
    return Path(__file__).parent.parent / 'config' / filename


def extract_key_quotes(segments: List[Dict], criteria: Dict) -> List[Dict]:
    """
    Extract quotable segments based on importance and category.
    
    Args:
        segments: List of transcript segments
        criteria: Quote selection criteria from config
    """
    quotes = []
    
    min_words = criteria.get("min_words", 10)
    max_words = criteria.get("max_words", 50)
    importance = criteria.get("importance_threshold", "high")
    priority_categories = criteria.get("categories_priority", [])
    
    for segment in segments:
        # Check importance
        if segment.get("importance") != importance:
            continue
        
        # Check word count
        word_count = len(segment["text"].split())
        if word_count < min_words or word_count > max_words:
            continue
        
        # Prioritize certain categories
        if priority_categories and segment.get("category") in priority_categories:
            quotes.append({
                "speaker": segment["speaker"],
                "text": segment["text"],
                "timestamp": segment["timestamp"],
                "category": segment["category"]
            })
    
    return quotes


def identify_key_highlights(segments: List[Dict], keywords: List[str]) -> List[Dict]:
    """
    Identify key highlights from transcript segments.
    
    Args:
        segments: List of transcript segments
        keywords: List of keywords that indicate important highlights
    """
    highlights = []
    
    for segment in segments:
        text_lower = segment["text"].lower()
        
        # Check if segment contains highlight keywords
        if any(keyword in text_lower for keyword in keywords):
            highlights.append({
                "speaker": segment["speaker"],
                "text": segment["text"],
                "timestamp": segment["timestamp"],
                "category": segment.get("category", "general")
            })
    
    return highlights


def extract_statistics(text: str) -> List[str]:
    """Extract numerical statistics from text."""
    patterns = [
        r'\d+%',  # Percentages
        r'\d+[xX]',  # Multipliers (10x)
        r'\$\d+',  # Dollar amounts
        r'\d{1,3}(,\d{3})*',  # Numbers with commas
        r'\d+\s*(million|billion|thousand)',  # Large numbers
    ]
    
    stats = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        stats.extend(matches)
    
    return stats


def generate_hashtags(text: str, event_name: str, max_count: int = 3) -> List[str]:
    """Generate relevant hashtags from text and event name."""
    # Start with event-based hashtags
    hashtags = []
    
    # Extract potential hashtag words (capitalized words, key terms)
    words = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b', text)
    
    # Add event-specific hashtag
    event_tag = '#' + event_name.replace(' ', '')
    if event_tag not in hashtags:
        hashtags.append(event_tag)
    
    # Add topic hashtags
    topic_keywords = {
        'AI': '#AI',
        'Innovation': '#Innovation',
        'Launch': '#Launch',
        'Technology': '#Tech',
        'Product': '#Product',
        'Enterprise': '#Enterprise'
    }
    
    for keyword, tag in topic_keywords.items():
        if keyword.lower() in text.lower() and len(hashtags) < max_count:
            if tag not in hashtags:
                hashtags.append(tag)
    
    return hashtags[:max_count]


def format_quote_with_attribution(quote: Dict, style: str = "full") -> str:
    """Format a quote with proper attribution."""
    if style == "full":
        return f'"{quote["text"]}" - {quote["speaker"]}'
    elif style == "inline":
        return f'{quote["speaker"]} said, "{quote["text"]}"'
    else:
        return f'"{quote["text"]}"'


def categorize_segments_by_type(segments: List[Dict]) -> Dict[str, List[Dict]]:
    """Group segments by category."""
    categorized = {}
    
    for segment in segments:
        category = segment.get("category", "general")
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(segment)
    
    return categorized


def create_executive_summary(segments: List[Dict], max_sentences: int = 3) -> str:
    """Create a brief executive summary from key segments."""
    # Get high-importance segments
    important = [s for s in segments if s.get("importance") == "high"]
    
    # Prioritize announcement and vision categories
    priority_segments = [
        s for s in important 
        if s.get("category") in ["announcement", "vision", "product"]
    ]
    
    # Take the first few
    summary_segments = priority_segments[:max_sentences]
    
    # Extract just the key facts
    summary_points = []
    for segment in summary_segments:
        # Get first sentence or main point
        text = segment["text"]
        first_sentence = text.split('.')[0] + '.'
        summary_points.append(first_sentence)
    
    return " ".join(summary_points)


def extract_speaker_info(segments: List[Dict]) -> Dict[str, Dict]:
    """Extract unique speakers and their roles from segments."""
    speakers = {}
    
    for segment in segments:
        speaker_name = segment.get("speaker")
        if speaker_name and speaker_name not in speakers:
            speakers[speaker_name] = {
                "name": speaker_name,
                "quotes_count": 0,
                "categories": set()
            }
        
        if speaker_name:
            speakers[speaker_name]["quotes_count"] += 1
            speakers[speaker_name]["categories"].add(segment.get("category", "general"))
    
    # Convert sets to lists for JSON serialization
    for speaker in speakers.values():
        speaker["categories"] = list(speaker["categories"])
    
    return speakers
