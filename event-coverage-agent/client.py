"""
Client to interact with the Event Coverage Agent
Run this to see the agent in action!
"""
import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from server import (
    process_event_transcript,
    extract_press_quotes,
    generate_social_media_posts,
    create_press_release,
    generate_newsletter_recap,
    run_full_coverage_cycle
)


async def demo_individual_tools():
    """Demo: Running individual tools step by step"""
    print("\n" + "="*70)
    print("🎯 DEMO: Individual Tool Execution")
    print("="*70 + "\n")
    
    # Step 1: Process transcript
    print("1️⃣ Processing event transcript...")
    transcript = await process_event_transcript()
    transcript_data = json.loads(transcript)
    print(f"   Event: {transcript_data['event_name']}")
    print(f"   Duration: {transcript_data['duration_minutes']} minutes")
    print(f"   Speakers: {len(transcript_data['speakers'])}")
    print(f"   Segments: {transcript_data['total_segments']}\n")
    
    # Step 2: Extract quotes
    print("2️⃣ Extracting press-ready quotes...")
    quotes = await extract_press_quotes()
    quotes_data = json.loads(quotes)
    print(f"   Press quotes extracted: {quotes_data['total_quotes']}")
    if quotes_data['quotes']:
        print(f"   Sample: \"{quotes_data['quotes'][0]['quote'][:80]}...\"\n")
    
    # Step 3: Generate social posts
    print("3️⃣ Generating social media posts...")
    twitter = await generate_social_media_posts("twitter")
    twitter_data = json.loads(twitter)
    print(f"   Twitter posts: {twitter_data['posts_generated']}")
    if twitter_data['posts']:
        print(f"   Sample tweet: {twitter_data['posts'][0]['content'][:100]}...\n")
    
    # Step 4: Press release
    print("4️⃣ Creating press release...")
    pr = await create_press_release()
    pr_data = json.loads(pr)
    print(f"   Word count: {pr_data['word_count']}")
    print(f"   Quotes included: {pr_data['quotes_included']}\n")
    
    # Step 5: Newsletter
    print("5️⃣ Generating newsletter recap...")
    newsletter = await generate_newsletter_recap()
    newsletter_data = json.loads(newsletter)
    print(f"   Sections: {', '.join(newsletter_data['sections'])}")
    print(f"   Word count: {newsletter_data['word_count']}\n")


async def demo_full_cycle():
    """Demo: Running the complete coverage cycle"""
    print("\n" + "="*70)
    print("🚀 DEMO: Full Event Coverage Cycle")
    print("="*70 + "\n")
    
    result = await run_full_coverage_cycle()
    result_data = json.loads(result)
    
    outputs = result_data['outputs']
    
    # Display Press Quotes
    print("💬 PRESS-READY QUOTES")
    print("-" * 70)
    quotes = outputs['press_quotes']['quotes'][:3]
    for i, quote in enumerate(quotes, 1):
        print(f"\n{i}. {quote['formatted']}")
    
    # Display Social Media Posts
    print("\n\n📱 SOCIAL MEDIA POSTS")
    print("-" * 70)
    
    print("\n🐦 Twitter:")
    for i, post in enumerate(outputs['social_media']['twitter']['posts'][:2], 1):
        print(f"\nTweet {i}:")
        print(f"{post['content']}")
        print(f"({post['character_count']} characters)")
    
    print("\n\n💼 LinkedIn:")
    linkedin_post = outputs['social_media']['linkedin']['posts'][0]
    print(f"\n{linkedin_post['content'][:300]}...")
    
    # Display Press Release (excerpt)
    print("\n\n📰 PRESS RELEASE (Excerpt)")
    print("-" * 70)
    pr_text = outputs['press_release']['press_release']
    print(pr_text[:500] + "...\n")
    print(f"[Full press release: {outputs['press_release']['word_count']} words]")
    
    # Display Newsletter (excerpt)
    print("\n\n📧 NEWSLETTER RECAP (Excerpt)")
    print("-" * 70)
    newsletter_text = outputs['newsletter']['newsletter']
    print(newsletter_text[:500] + "...\n")
    print(f"[Full newsletter: {outputs['newsletter']['word_count']} words]")
    
    # Summary
    print("\n" + "="*70)
    print("✅ COVERAGE SUMMARY")
    print("-" * 70)
    print(f"Press Quotes: {outputs['press_quotes']['total_quotes']} extracted")
    print(f"Twitter Posts: {outputs['social_media']['twitter']['posts_generated']} generated")
    print(f"LinkedIn Posts: {outputs['social_media']['linkedin']['posts_generated']} generated")
    print(f"Press Release: {outputs['press_release']['word_count']} words")
    print(f"Newsletter: {outputs['newsletter']['word_count']} words")
    print("="*70 + "\n")


async def show_detailed_output(output_type: str):
    """Show detailed output for a specific content type."""
    print(f"\n{'='*70}")
    print(f"📄 DETAILED OUTPUT: {output_type.upper()}")
    print(f"{'='*70}\n")
    
    if output_type == "quotes":
        result = await extract_press_quotes()
        data = json.loads(result)
        for i, quote in enumerate(data['quotes'], 1):
            print(f"{i}. {quote['formatted']}")
            print(f"   Category: {quote['category']} | Timestamp: {quote['timestamp']}\n")
    
    elif output_type == "press_release":
        result = await create_press_release()
        data = json.loads(result)
        print(data['press_release'])
    
    elif output_type == "newsletter":
        result = await generate_newsletter_recap()
        data = json.loads(result)
        print(data['newsletter'])


async def main():
    """Run all demos"""
    print("\n🎤 EVENT COVERAGE AGENT")
    print("Automated Transcription & Content Generation\n")
    
    # Option 1: Run individual tools
    await demo_individual_tools()
    
    # Option 2: Run full cycle
    await demo_full_cycle()
    
    # Option 3: Show detailed outputs
    print("\n📋 DETAILED OUTPUTS AVAILABLE")
    print("="*70)
    print("\nTo see detailed output, uncomment one of these:")
    print("# await show_detailed_output('quotes')")
    print("# await show_detailed_output('press_release')")
    print("# await show_detailed_output('newsletter')")
    
    # Uncomment to see full outputs:
    # await show_detailed_output('press_release')
    
    print("\n✅ Demo complete! Agent is ready for production use.")


if __name__ == "__main__":
    asyncio.run(main())
