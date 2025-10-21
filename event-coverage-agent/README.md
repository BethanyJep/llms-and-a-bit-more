# 🎤 Event Coverage Agent

An MCP-based AI agent for automated event coverage and content generation. Transcribes keynote highlights from events and automatically generates press releases, social media posts, and newsletter recaps.

## 🎯 What It Does

The agent automates post-event content creation:

1. **Processes** event transcripts from audio/video recordings
2. **Extracts** press-ready quotes from speakers
3. **Generates** platform-specific social media posts (Twitter, LinkedIn, Instagram)
4. **Creates** professional press releases
5. **Produces** comprehensive newsletter recaps
6. **Identifies** key highlights and statistics

## 📁 Project Structure

```
event-coverage-agent/
├── src/
│   ├── server.py           # Main MCP server with 6 tools
│   └── utils.py            # Helper functions
├── data/
│   └── mock_transcript.json  # Sample event transcript
├── config/
│   ├── content_templates.json  # Templates for content generation
│   └── settings.json           # Configuration settings
├── client.py               # Demo client
└── README.md              # This file
```

## 🏗️ Building Blocks

### Core Tools (6 MCP Tools)

| Tool | Purpose |
|------|---------|
| `process_event_transcript` | Process and analyze event transcripts |
| `extract_press_quotes` | Extract quotable statements from speakers |
| `generate_social_media_posts` | Create platform-specific social posts |
| `create_press_release` | Generate professional press releases |
| `generate_newsletter_recap` | Produce post-event email recaps |
| `run_full_coverage_cycle` | Execute complete coverage workflow |

### Key Features

- **Multi-Speaker Support**: Handles multiple speakers with role attribution
- **Quote Extraction**: Automatically identifies the most impactful statements
- **Platform Optimization**: Tailors content for Twitter, LinkedIn, Instagram
- **Press-Ready Output**: Professional formatting for media distribution
- **Statistics Detection**: Identifies and highlights key metrics
- **Hashtag Generation**: Auto-generates relevant hashtags
- **Executive Summaries**: Creates concise event overviews

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
from server import extract_press_quotes

async def get_quotes():
    result = await extract_press_quotes()
    print(result)

asyncio.run(get_quotes())
```

## 📊 Sample Output

### Press Quotes
```
1. "Today marks a pivotal moment in TechCorp's history. We're not just 
   launching a product; we're introducing a new era of innovation." 
   - Sarah Chen, CEO

2. "Our new AI engine is 10 times faster than the previous generation, 
   with 95% accuracy improvement." 
   - Michael Rodriguez, CTO
```

### Social Media (Twitter)
```
🚀 TechCorp announces 200% year-over-year growth, with over 50,000 
customers now trusting our platform... #TechCorp #AI #Innovation
```

### Press Release Excerpt
```
FOR IMMEDIATE RELEASE

TechCorp Annual Launch Event 2025
Empowering Innovation Through AI

2025-10-21 - TechCorp today announced that we've achieved 200% 
year-over-year growth, with over 50,000 customers now trusting 
our platform...
```

## 🔧 Configuration

### Customize Company Info

Edit `config/settings.json`:

```json
{
  "company_info": {
    "name": "YourCompany",
    "tagline": "Your Tagline",
    "description": "Your description..."
  }
}
```

### Adjust Content Templates

Edit `config/content_templates.json`:

```json
{
  "quote_selection_criteria": {
    "min_words": 10,
    "max_words": 50,
    "importance_threshold": "high"
  }
}
```

### Update Event Transcript

Edit `data/mock_transcript.json` with your event data:

```json
{
  "event_metadata": {
    "event_name": "Your Event",
    "date": "2025-10-21",
    "speakers": [...]
  },
  "transcript_segments": [...]
}
```

## 🔌 Integration with Speech-to-Text

To connect real audio transcription services:

```python
# Example: Azure Speech Services Integration
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig

@server.tool()
async def process_event_transcript(audio_file: str):
    # Configure Azure Speech
    speech_config = SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION")
    )
    
    # Transcribe audio
    audio_config = AudioConfig(filename=audio_file)
    recognizer = SpeechRecognizer(
        speech_config=speech_config, 
        audio_config=audio_config
    )
    
    # Process transcript...
```

**Supported Services:**
- Azure Cognitive Services Speech-to-Text
- Google Cloud Speech-to-Text
- AWS Transcribe
- OpenAI Whisper
- Assembly AI

## 🧪 Testing

The project includes mock transcript data. To test:

1. Run the demo: `python client.py`
2. Review generated content
3. Modify `data/mock_transcript.json` for different events

## 📈 Use Cases

- **Product Launches**: Generate instant press coverage
- **Conference Coverage**: Create real-time social posts
- **Earnings Calls**: Extract key quotes and summaries
- **Keynote Speeches**: Produce shareable content
- **Panel Discussions**: Capture multi-speaker insights
- **Webinar Recaps**: Automate follow-up content

## 🎓 Architecture

```
┌─────────────────┐
│   MCP Client    │ (AI Agent / Automation)
│  (Agent Builder)│
└────────┬────────┘
         │
         │ MCP Protocol
         │
┌────────▼────────┐
│ Event Coverage  │
│   MCP Server    │
├─────────────────┤
│ • Transcribe    │
│ • Extract       │
│ • Generate      │
│ • Format        │
│ • Distribute    │
└────────┬────────┘
         │
    ┌────┴─────┬──────┬───────┐
    ▼          ▼      ▼       ▼
[Audio]  [Quotes] [Social] [Press]
```

## 🔐 Security Notes

- Store API keys in environment variables
- Sanitize transcript content before processing
- Implement access controls for sensitive events
- Add watermarking for embargoed content

## 📝 Content Generated

From a single event transcript, the agent produces:

✅ **Press-Ready Quotes** (5-10 formatted quotes)
✅ **Twitter Posts** (5 optimized tweets with hashtags)
✅ **LinkedIn Posts** (Professional, detailed updates)
✅ **Instagram Captions** (Visual-friendly with hashtags)
✅ **Press Release** (Full professional release)
✅ **Newsletter Recap** (Comprehensive email summary)

**Total Output**: ~2,000-3,000 words of ready-to-publish content

## 🚀 Production Workflow

1. **Record Event** → Audio/video file
2. **Transcribe** → Speech-to-text service
3. **Process** → Event Coverage Agent
4. **Review** → Human approval (optional)
5. **Publish** → Distribute content

**Time Saved**: 4-6 hours of manual content creation → 5 minutes automated

## 📚 Next Steps

1. **Add Speech-to-Text**: Integrate Azure/Google/AWS transcription
2. **Multi-Language Support**: Translate content automatically
3. **Brand Voice Tuning**: Customize tone and style
4. **Media Kit Generation**: Include speaker photos, logos
5. **Auto-Distribution**: Publish directly to social platforms
6. **Analytics Integration**: Track content performance

## 🤝 Contributing

Extend this agent with:
- Video clip extraction for social media
- Automated caption generation
- Speaker identification and diarization
- Real-time live event coverage
- Multi-format export (PDF, HTML, Markdown)

---

**Built with**: MCP (Model Context Protocol) + Python  
**License**: MIT
