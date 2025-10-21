# 🧠 Media Monitoring & Sentiment Analysis Agent

An MCP-based AI agent for reactive PR and brand monitoring. Automatically tracks brand mentions across social platforms, analyzes sentiment, and generates actionable morning briefings.

## 🎯 What It Does

The agent performs a complete monitoring cycle:

1. **Fetches** brand mentions from Twitter/X, blogs, and news sources
2. **Classifies** sentiment (positive/neutral/negative) for each mention
3. **Analyzes** trends and clusters related conversations
4. **Generates** structured PR briefings with actionable insights
5. **Triggers** escalation alerts when negative sentiment exceeds thresholds
6. **Drafts** PR responses for identified issues

## 📁 Project Structure

```
media-monitoring-agent/
├── src/
│   ├── server.py           # Main MCP server with 6 tools
│   └── utils.py            # Helper functions
├── data/
│   ├── mock_mentions.json  # Sample brand mentions
│   └── sentiment_keywords.json  # Keywords for sentiment analysis
├── config/
│   └── settings.json       # Configuration (thresholds, templates)
├── client.py               # Demo client
└── README.md              # This file
```

## 🏗️ Building Blocks

### Core Tools (6 MCP Tools)

| Tool | Purpose |
|------|---------|
| `fetch_brand_mentions` | Pull mentions from multiple platforms |
| `analyze_sentiment` | Calculate sentiment distribution & stats |
| `generate_morning_briefing` | Create structured PR reports |
| `check_escalation_trigger` | Detect crisis situations |
| `generate_response_draft` | Auto-draft PR responses |
| `run_full_monitoring_cycle` | Orchestrate complete workflow |

### Key Features

- **Multi-Platform Monitoring**: Twitter/X, blogs, news sites
- **Sentiment Classification**: Keyword-based analysis (easily extensible to LLM)
- **Trending Topic Detection**: Identifies hot conversation themes
- **Negative Clustering**: Groups complaints by category
- **Escalation System**: Automatic alerts for PR crises (default: 30% negative threshold)
- **Response Generation**: Context-aware PR draft responses

## 🚀 Quick Start

### Prerequisites

```bash
pip install mcp
```

### Run the Agent

**Option 1: Full Demo (Recommended)**
```bash
python client.py
```

**Option 2: As MCP Server**
```bash
cd src
python server.py
```

**Option 3: Individual Tools**
```python
import asyncio
import sys
sys.path.append('src')
from server import run_full_monitoring_cycle

async def monitor():
    result = await run_full_monitoring_cycle("YourBrand")
    print(result)

asyncio.run(monitor())
```

## 📊 Sample Output

```
📨 MORNING MEDIA BRIEFING
------------------------------------------------------------
Date: 2025-10-21
Brand: TechCorp

📊 SUMMARY:
  Total Mentions: 8
  Positive: 50.0%
  Neutral: 25.0%
  Negative: 25.0%
  Dominant: POSITIVE

🔥 TRENDING TOPICS:
  • innovation (3 mentions)
  • product launch (2 mentions)
  • customer service (2 mentions)

⚠️ NEGATIVE CLUSTERS:
  • Delivery Issues: 1 mention(s)
  • Technical Problems: 1 mention(s)

🎯 STATUS: ✅ Normal

💡 RECOMMENDATIONS:
  • Continue monitoring. Sentiment remains healthy.
```

## 🔧 Configuration

### Customize Settings

Edit `config/settings.json`:

```json
{
  "negative_threshold": 30,
  "escalation_severity": {
    "low": 0,
    "medium": 30,
    "high": 50
  }
}
```

### Add Sentiment Keywords

Edit `data/sentiment_keywords.json`:

```json
{
  "positive_keywords": ["love", "great", "amazing", ...],
  "negative_keywords": ["terrible", "bad", "frustrated", ...]
}
```

### Update Mock Data

Edit `data/mock_mentions.json` to test with your own data.

## 🔌 Integration with Real APIs

To connect real data sources, modify `src/server.py`:

```python
# Example: Twitter API Integration
import tweepy

@server.tool()
async def fetch_brand_mentions(brand_name: str, ...):
    # Twitter API
    tweets = twitter_client.search_tweets(
        query=f"@{brand_name} OR {brand_name}",
        max_results=100
    )
    
    # Transform to standard format
    mentions = [
        {
            "id": tweet.id,
            "platform": "twitter",
            "text": tweet.text,
            "author": tweet.author.username,
            "timestamp": tweet.created_at.isoformat(),
            "engagement": {
                "likes": tweet.public_metrics.like_count,
                "retweets": tweet.public_metrics.retweet_count
            }
        }
        for tweet in tweets.data
    ]
    
    # Continue with sentiment analysis...
```

## 🧪 Testing

The project includes mock data for demonstration. To test:

1. Run the demo client: `python client.py`
2. Review the generated briefing
3. Modify data in `data/mock_mentions.json` for different scenarios

## 📈 Use Cases

- **Daily PR Monitoring**: Run at 8am for morning briefings
- **Crisis Detection**: Real-time escalation for brand emergencies
- **Campaign Tracking**: Monitor product launch reception
- **Competitor Analysis**: Track competitor brand sentiment
- **Customer Support**: Identify recurring complaints

## 🎓 Architecture

```
┌─────────────────┐
│   MCP Client    │ (AI Agent / API)
│  (Agent Builder)│
└────────┬────────┘
         │
         │ MCP Protocol
         │
┌────────▼────────┐
│  Media Monitor  │
│   MCP Server    │
├─────────────────┤
│ • Fetch Tool    │
│ • Analyze Tool  │
│ • Briefing Tool │
│ • Escalate Tool │
│ • Response Tool │
└────────┬────────┘
         │
    ┌────┴─────┬──────┬───────┐
    ▼          ▼      ▼       ▼
[Twitter]  [Blogs] [News] [Reddit]
```

## 🔐 Security Notes

- Store API keys in environment variables
- Implement rate limiting for production
- Sanitize user inputs
- Add authentication for MCP server endpoints

## 📝 Next Steps

1. **Add LLM Integration**: Use OpenAI/Azure OpenAI for better sentiment analysis
2. **Connect Real APIs**: Twitter, Reddit, News APIs
3. **Build Dashboard**: Visualize trends over time
4. **Automate Scheduling**: Run daily via cron/scheduled tasks
5. **Add Slack Integration**: Send briefings to PR team channel

## 🤝 Contributing

This is a demo template. Extend it with:
- More platforms (LinkedIn, Reddit, TikTok)
- Advanced sentiment models (transformers, BERT)
- Historical trend analysis
- Automated response posting

---

**Built with**: MCP (Model Context Protocol) + Python  
**License**: MIT
