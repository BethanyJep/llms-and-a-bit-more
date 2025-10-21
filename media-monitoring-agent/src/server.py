"""
Media Monitoring & Sentiment Analysis Agent
MCP Server for reactive PR and brand monitoring
"""
import json
from datetime import datetime
from typing import List, Dict, Literal
from mcp.server.fastmcp import FastMCP
from pathlib import Path

from utils import (
    load_json_file,
    get_data_path,
    get_config_path,
    classify_sentiment,
    calculate_sentiment_stats,
    identify_trending_topics,
    cluster_negative_mentions
)

# Create MCP server for Media Monitoring
server = FastMCP("media_monitoring_agent")

# Load configuration and data
config = load_json_file(get_config_path('settings.json'))
sentiment_keywords = load_json_file(get_data_path('sentiment_keywords.json'))

# Configuration constants
NEGATIVE_THRESHOLD = config["negative_threshold"]
TOPIC_KEYWORDS = config["topic_keywords"]
RESPONSE_TEMPLATES = config["response_templates"]


def load_mock_mentions() -> List[Dict]:
    """Load mock mentions from JSON file."""
    return load_json_file(get_data_path('mock_mentions.json'))


@server.tool()
async def fetch_brand_mentions(
    brand_name: str = "TechCorp",
    platforms: str = "twitter,blog,news",
    time_range: str = "24h"
) -> str:
    """
    Fetch brand mentions across social media platforms and news sources.
    
    Args:
        brand_name: The brand to monitor (default: TechCorp)
        platforms: Comma-separated list of platforms (twitter,blog,news)
        time_range: Time range to search (24h, 7d, 30d)
    """
    platform_list = [p.strip() for p in platforms.split(",")]
    
    # Load mentions from data file
    all_mentions = load_mock_mentions()
    
    # Filter by platforms
    filtered_mentions = [
        m for m in all_mentions 
        if m["platform"] in platform_list
    ]
    
    # Add sentiment classification
    for mention in filtered_mentions:
        mention["sentiment"] = classify_sentiment(mention["text"], sentiment_keywords)
    
    result = {
        "status": "success",
        "brand": brand_name,
        "time_range": time_range,
        "platforms": platform_list,
        "mentions_found": len(filtered_mentions),
        "mentions": filtered_mentions
    }
    
    return json.dumps(result, indent=2)


@server.tool()
async def analyze_sentiment(mentions_json: str) -> str:
    """
    Analyze sentiment distribution from fetched mentions.
    
    Args:
        mentions_json: JSON string of mentions from fetch_brand_mentions
    """
    try:
        data = json.loads(mentions_json)
        mentions = data.get("mentions", [])
        
        # Ensure all mentions have sentiment
        for mention in mentions:
            if "sentiment" not in mention:
                mention["sentiment"] = classify_sentiment(mention["text"], sentiment_keywords)
        
        stats = calculate_sentiment_stats(mentions)
        
        # Platform breakdown
        platform_sentiments = {}
        for platform in set(m["platform"] for m in mentions):
            platform_mentions = [m for m in mentions if m["platform"] == platform]
            platform_sentiments[platform] = calculate_sentiment_stats(platform_mentions)
        
        result = {
            "status": "success",
            "overall_sentiment": stats,
            "by_platform": platform_sentiments,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@server.tool()
async def generate_morning_briefing(mentions_json: str, sentiment_json: str) -> str:
    """
    Generate a structured morning briefing report for the PR team.
    
    Args:
        mentions_json: JSON string of mentions from fetch_brand_mentions
        sentiment_json: JSON string of sentiment analysis
    """
    try:
        mentions_data = json.loads(mentions_json)
        sentiment_data = json.loads(sentiment_json)
        
        mentions = mentions_data.get("mentions", [])
        overall = sentiment_data.get("overall_sentiment", {})
        
        # Identify trending topics
        topics = identify_trending_topics(mentions, TOPIC_KEYWORDS)
        
        # Get top positive and negative mentions
        positive_mentions = sorted(
            [m for m in mentions if m.get("sentiment") == "positive"],
            key=lambda x: x.get("engagement", {}).get("likes", 0) + 
                         x.get("engagement", {}).get("retweets", 0),
            reverse=True
        )[:2]
        
        negative_mentions = [m for m in mentions if m.get("sentiment") == "negative"]
        
        # Build briefing
        briefing = {
            "report_type": "Morning Media Briefing",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "brand": mentions_data.get("brand", "TechCorp"),
            "summary": {
                "total_mentions": overall.get("total", 0),
                "sentiment_breakdown": {
                    "positive": f"{overall.get('positive', 0)}%",
                    "neutral": f"{overall.get('neutral', 0)}%",
                    "negative": f"{overall.get('negative', 0)}%"
                },
                "dominant_sentiment": max(
                    [("positive", overall.get("positive", 0)),
                     ("neutral", overall.get("neutral", 0)),
                     ("negative", overall.get("negative", 0))],
                    key=lambda x: x[1]
                )[0]
            },
            "trending_topics": topics,
            "highlights": {
                "top_positive_mentions": [
                    {
                        "platform": m["platform"],
                        "author": m["author"],
                        "text": m["text"][:100] + "..." if len(m["text"]) > 100 else m["text"],
                        "engagement": m["engagement"]
                    }
                    for m in positive_mentions
                ],
                "negative_clusters": cluster_negative_mentions(mentions) if negative_mentions else {}
            },
            "alert_status": "⚠️ ESCALATION NEEDED" if overall.get("negative", 0) >= NEGATIVE_THRESHOLD else "✅ Normal",
            "recommendations": []
        }
        
        # Add recommendations
        if overall.get("negative", 0) >= NEGATIVE_THRESHOLD:
            briefing["recommendations"].append(
                "High negative sentiment detected. Recommend immediate PR response."
            )
        
        if any("delivery" in topic.lower() for topic in topics):
            briefing["recommendations"].append(
                "Delivery concerns trending. Coordinate with logistics team."
            )
        
        if any("bug" in m["text"].lower() or "issue" in m["text"].lower() for m in mentions):
            briefing["recommendations"].append(
                "Technical issues reported. Notify product/engineering team."
            )
        
        if not briefing["recommendations"]:
            briefing["recommendations"].append(
                "Continue monitoring. Sentiment remains healthy."
            )
        
        return json.dumps(briefing, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@server.tool()
async def check_escalation_trigger(sentiment_json: str, threshold: int = None) -> str:
    """
    Check if negative sentiment exceeds threshold and needs escalation.
    
    Args:
        sentiment_json: JSON string of sentiment analysis
        threshold: Percentage threshold for negative sentiment (default from config)
    """
    if threshold is None:
        threshold = NEGATIVE_THRESHOLD
        
    try:
        sentiment_data = json.loads(sentiment_json)
        overall = sentiment_data.get("overall_sentiment", {})
        negative_pct = overall.get("negative", 0)
        
        needs_escalation = negative_pct >= threshold
        
        result = {
            "status": "success",
            "escalation_needed": needs_escalation,
            "negative_sentiment_percentage": negative_pct,
            "threshold": threshold,
            "severity": "HIGH" if negative_pct >= 50 else "MEDIUM" if needs_escalation else "LOW",
            "timestamp": datetime.now().isoformat()
        }
        
        if needs_escalation:
            result["action_required"] = [
                "Notify PR crisis management team",
                "Prepare official statement draft",
                "Monitor social channels continuously",
                "Schedule emergency stakeholder briefing"
            ]
        else:
            result["action_required"] = ["Continue standard monitoring"]
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@server.tool()
async def generate_response_draft(issue_description: str, tone: str = "professional") -> str:
    """
    Generate a draft PR response for identified issues.
    
    Args:
        issue_description: Description of the issue to address
        tone: Response tone (professional, empathetic, formal)
    """
    issue_lower = issue_description.lower()
    
    if "delivery" in issue_lower or "shipping" in issue_lower:
        template_type = "delivery"
    elif "bug" in issue_lower or "technical" in issue_lower or "issue" in issue_lower:
        template_type = "technical"
    else:
        template_type = "general"
    
    draft = RESPONSE_TEMPLATES[template_type].get(tone, RESPONSE_TEMPLATES[template_type]["professional"])
    
    result = {
        "status": "success",
        "issue_type": template_type,
        "tone": tone,
        "draft_response": draft,
        "suggested_channels": ["Twitter/X", "Official Blog", "Email to Affected Customers"],
        "review_required": True,
        "generated_at": datetime.now().isoformat()
    }
    
    return json.dumps(result, indent=2)


@server.tool()
async def run_full_monitoring_cycle(brand_name: str = "TechCorp") -> str:
    """
    Run a complete monitoring cycle: fetch → analyze → brief → check escalation.
    This is the main orchestration tool for the agent.
    
    Args:
        brand_name: The brand to monitor
    """
    print(f"🚀 Starting full monitoring cycle for {brand_name}...")
    
    # Step 1: Fetch mentions
    print("📡 Fetching brand mentions...")
    mentions_result = await fetch_brand_mentions(brand_name=brand_name)
    
    # Step 2: Analyze sentiment
    print("🧠 Analyzing sentiment...")
    sentiment_result = await analyze_sentiment(mentions_result)
    
    # Step 3: Generate briefing
    print("📊 Generating morning briefing...")
    briefing_result = await generate_morning_briefing(mentions_result, sentiment_result)
    
    # Step 4: Check escalation
    print("⚠️ Checking escalation triggers...")
    escalation_result = await check_escalation_trigger(sentiment_result)
    
    # Compile final report
    briefing_data = json.loads(briefing_result)
    escalation_data = json.loads(escalation_result)
    
    final_report = {
        "status": "success",
        "monitoring_cycle_complete": True,
        "timestamp": datetime.now().isoformat(),
        "briefing": briefing_data,
        "escalation": escalation_data
    }
    
    print("✅ Monitoring cycle complete!")
    
    return json.dumps(final_report, indent=2)


if __name__ == "__main__":
    # Run the server
    server.run()
