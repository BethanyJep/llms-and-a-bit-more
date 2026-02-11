"""
Utility functions for the Media Monitoring Agent
"""
import json
from pathlib import Path
from typing import List, Dict, Literal


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


def classify_sentiment(text: str, keywords: dict) -> Literal["positive", "neutral", "negative"]:
    """Classify sentiment based on keyword analysis."""
    text_lower = text.lower()
    
    positive_keywords = keywords.get("positive_keywords", [])
    negative_keywords = keywords.get("negative_keywords", [])
    
    positive_score = sum(1 for keyword in positive_keywords if keyword in text_lower)
    negative_score = sum(1 for keyword in negative_keywords if keyword in text_lower)
    
    if negative_score > positive_score:
        return "negative"
    elif positive_score > negative_score:
        return "positive"
    else:
        return "neutral"


def calculate_sentiment_stats(mentions: List[Dict]) -> Dict:
    """Calculate sentiment statistics."""
    total = len(mentions)
    if total == 0:
        return {"positive": 0, "neutral": 0, "negative": 0, "total": 0}
    
    sentiments = [m.get("sentiment", "neutral") for m in mentions]
    positive_count = sentiments.count("positive")
    neutral_count = sentiments.count("neutral")
    negative_count = sentiments.count("negative")
    
    return {
        "positive": round((positive_count / total) * 100, 1),
        "neutral": round((neutral_count / total) * 100, 1),
        "negative": round((negative_count / total) * 100, 1),
        "total": total,
        "counts": {
            "positive": positive_count,
            "neutral": neutral_count,
            "negative": negative_count
        }
    }


def identify_trending_topics(mentions: List[Dict], topic_keywords: dict) -> List[str]:
    """Identify trending topics from mentions."""
    topics = []
    
    for topic_name, keywords in topic_keywords.items():
        count = sum(1 for m in mentions 
                   if any(kw in m["text"].lower() for kw in keywords))
        if count > 0:
            topics.append(f"{topic_name} ({count} mentions)")
    
    return topics[:3]  # Top 3


def cluster_negative_mentions(mentions: List[Dict]) -> Dict[str, List[Dict]]:
    """Group negative mentions by theme."""
    negative = [m for m in mentions if m.get("sentiment") == "negative"]
    
    clusters = {
        "Delivery Issues": [],
        "Product Quality": [],
        "Customer Support": [],
        "Technical Problems": []
    }
    
    for mention in negative:
        text_lower = mention["text"].lower()
        if any(kw in text_lower for kw in ["delivery", "shipping", "waiting"]):
            clusters["Delivery Issues"].append(mention)
        elif any(kw in text_lower for kw in ["bugs", "issues", "problems", "update"]):
            clusters["Technical Problems"].append(mention)
        elif any(kw in text_lower for kw in ["support", "service", "help"]):
            clusters["Customer Support"].append(mention)
        else:
            clusters["Product Quality"].append(mention)
    
    return {k: v for k, v in clusters.items() if v}
