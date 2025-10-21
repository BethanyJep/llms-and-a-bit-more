"""
Client to interact with the Media Monitoring Agent
Run this to see the agent in action!
"""
import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from server import (
    fetch_brand_mentions,
    analyze_sentiment,
    generate_morning_briefing,
    check_escalation_trigger,
    generate_response_draft,
    run_full_monitoring_cycle
)


async def demo_individual_tools():
    """Demo: Running individual tools step by step"""
    print("\n" + "="*60)
    print("🎯 DEMO: Individual Tool Execution")
    print("="*60 + "\n")
    
    # Step 1: Fetch mentions
    print("1️⃣ Fetching brand mentions...")
    mentions = await fetch_brand_mentions(brand_name="TechCorp", platforms="twitter,blog,news")
    mentions_data = json.loads(mentions)
    print(f"   Found {mentions_data['mentions_found']} mentions\n")
    
    # Step 2: Analyze sentiment
    print("2️⃣ Analyzing sentiment...")
    sentiment = await analyze_sentiment(mentions)
    sentiment_data = json.loads(sentiment)
    overall = sentiment_data['overall_sentiment']
    print(f"   Sentiment: {overall['positive']}% positive, {overall['negative']}% negative\n")
    
    # Step 3: Generate briefing
    print("3️⃣ Generating morning briefing...")
    briefing = await generate_morning_briefing(mentions, sentiment)
    briefing_data = json.loads(briefing)
    print(f"   Alert Status: {briefing_data['alert_status']}")
    print(f"   Trending Topics: {', '.join(briefing_data['trending_topics'])}\n")
    
    # Step 4: Check escalation
    print("4️⃣ Checking escalation triggers...")
    escalation = await check_escalation_trigger(sentiment)
    escalation_data = json.loads(escalation)
    print(f"   Escalation Needed: {escalation_data['escalation_needed']}")
    print(f"   Severity: {escalation_data['severity']}\n")
    
    # Step 5: Generate response draft (if needed)
    if escalation_data['escalation_needed']:
        print("5️⃣ Generating response draft for delivery issues...")
        response = await generate_response_draft(
            "Customer complaints about delivery delays",
            tone="empathetic"
        )
        response_data = json.loads(response)
        print(f"   Draft: {response_data['draft_response']}\n")


async def demo_full_cycle():
    """Demo: Running the complete monitoring cycle"""
    print("\n" + "="*60)
    print("🚀 DEMO: Full Monitoring Cycle")
    print("="*60 + "\n")
    
    result = await run_full_monitoring_cycle(brand_name="TechCorp")
    result_data = json.loads(result)
    
    # Display the morning briefing
    briefing = result_data['briefing']
    
    print("📨 MORNING MEDIA BRIEFING")
    print("-" * 60)
    print(f"Date: {briefing['date']}")
    print(f"Brand: {briefing['brand']}")
    print(f"\n📊 SUMMARY:")
    print(f"  Total Mentions: {briefing['summary']['total_mentions']}")
    print(f"  Positive: {briefing['summary']['sentiment_breakdown']['positive']}")
    print(f"  Neutral: {briefing['summary']['sentiment_breakdown']['neutral']}")
    print(f"  Negative: {briefing['summary']['sentiment_breakdown']['negative']}")
    print(f"  Dominant: {briefing['summary']['dominant_sentiment'].upper()}")
    
    print(f"\n🔥 TRENDING TOPICS:")
    for topic in briefing['trending_topics']:
        print(f"  • {topic}")
    
    print(f"\n✨ TOP POSITIVE MENTIONS:")
    for mention in briefing['highlights']['top_positive_mentions']:
        print(f"  • [{mention['platform']}] {mention['author']}")
        print(f"    \"{mention['text']}\"")
        print(f"    Engagement: {mention['engagement']}\n")
    
    if briefing['highlights']['negative_clusters']:
        print(f"⚠️ NEGATIVE CLUSTERS:")
        for cluster_name, mentions in briefing['highlights']['negative_clusters'].items():
            print(f"  • {cluster_name}: {len(mentions)} mention(s)")
    
    print(f"\n🎯 STATUS: {briefing['alert_status']}")
    
    print(f"\n💡 RECOMMENDATIONS:")
    for rec in briefing['recommendations']:
        print(f"  • {rec}")
    
    # Display escalation info
    escalation = result_data['escalation']
    print(f"\n🚨 ESCALATION CHECK:")
    print(f"  Severity: {escalation['severity']}")
    print(f"  Negative Sentiment: {escalation['negative_sentiment_percentage']}%")
    print(f"  Threshold: {escalation['threshold']}%")
    
    if escalation['escalation_needed']:
        print(f"\n  ⚠️ ACTIONS REQUIRED:")
        for action in escalation['action_required']:
            print(f"    • {action}")
    
    print("\n" + "="*60 + "\n")


async def main():
    """Run all demos"""
    print("\n🧠 MEDIA MONITORING & SENTIMENT ANALYSIS AGENT")
    print("Reactive PR Tool for Brand Monitoring\n")
    
    # Option 1: Run individual tools
    await demo_individual_tools()
    
    # Option 2: Run full cycle (typical daily use)
    await demo_full_cycle()
    
    print("✅ Demo complete! Agent is ready for production use.")


if __name__ == "__main__":
    asyncio.run(main())
