# YouTube Integration Guide

## Overview
The Event Coverage Agent now supports processing YouTube videos directly! Simply paste a YouTube URL and the agent will:
1. Extract the video transcript automatically
2. Segment it into logical chunks
3. Generate all PR content (quotes, social posts, press release, newsletter)

## Setup

### Install Dependencies
```bash
cd event-coverage-agent
pip install -r requirements.txt
```

This will install:
- `youtube-transcript-api` - For extracting YouTube captions/transcripts
- `pytube` - For getting video metadata (title, author, etc.)
- `flask` - Web framework
- `openai` - (Optional) For future AI enhancements

### Run the Application
```bash
python app.py
```

Then open your browser to: **http://localhost:5001**

## How to Use

### Option 1: YouTube URL (Recommended)
1. Copy a YouTube video URL (e.g., from a conference talk, product launch, keynote)
2. Paste it into the YouTube URL input field
3. Click "Process YouTube Video"
4. Wait 30-60 seconds while the agent:
   - Extracts the transcript
   - Processes the content
   - Generates all PR materials

### Option 2: Mock Data
Click "Generate All Content (Mock Data)" to use the pre-loaded sample event transcript.

## Supported YouTube URL Formats

The agent supports all standard YouTube URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/v/VIDEO_ID`

## What Gets Generated

From a YouTube video, the agent automatically creates:

### 📝 Press-Ready Quotes
- 5+ key quotes from the video
- Speaker attribution
- Timestamps
- Category tags (announcement, vision, technical, etc.)

### 📲 Social Media Posts
**Twitter:**
- 5 posts optimized for Twitter (280 chars)
- Relevant hashtags
- Engaging hooks

**LinkedIn:**
- 3 professional posts (up to 3000 chars)
- Business-focused messaging
- Call-to-actions

**Instagram:**
- 3 visual-focused posts
- Emoji-rich captions
- Hashtag strategy

### 📰 Press Release
- Professional press release format
- Executive quotes
- Company boilerplate
- Media contact information

### 📬 Newsletter Recap
- Executive summary
- Key highlights section
- Technical details
- Next steps/call-to-action

## API Endpoints

### Process YouTube URL
```bash
POST /api/process-youtube
Content-Type: application/json

{
  "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "event_name": "Optional Event Name",
  "event_date": "2024-03-15",
  "segment_duration": 120
}
```

**Response:**
```json
{
  "success": true,
  "video_info": {
    "title": "Video Title",
    "duration": "45:30",
    "segments": 23,
    "words": 6789
  },
  "content_generated": {
    "quotes": 7,
    "twitter_posts": 5,
    "linkedin_posts": 3,
    "press_release": true,
    "newsletter": true
  },
  "data": { ... }
}
```

### Individual Content Generation
Once a transcript is processed, you can generate individual content types:

```bash
# Generate quotes only
POST /api/generate-quotes

# Generate social media posts (twitter, linkedin, or instagram)
POST /api/generate-social/twitter

# Generate press release
POST /api/generate-press-release

# Generate newsletter
POST /api/generate-newsletter
```

## Technical Details

### Transcript Extraction
The agent uses `youtube-transcript-api` to extract official captions or auto-generated transcripts. The transcript is then:
1. **Segmented** into ~2-minute chunks for better processing
2. **Cleaned** to remove repetitive filler words
3. **Formatted** with timestamps and metadata
4. **Stored** temporarily as `youtube_transcript.json`

### Segment Duration
Default: 120 seconds (2 minutes)

You can adjust this when calling the API:
```json
{
  "youtube_url": "...",
  "segment_duration": 180  // 3-minute segments
}
```

Longer segments = fewer, more comprehensive chunks
Shorter segments = more, focused chunks

### Language Support
Currently supports English transcripts. The processor will:
1. First try to get English transcripts
2. Fall back to auto-generated transcripts if available
3. Return an error if no transcripts are available

## Troubleshooting

### "Could not retrieve transcript"
**Causes:**
- Video has no captions/subtitles
- Video has disabled captions
- Video is private or age-restricted
- Network connection issues

**Solutions:**
- Try a different video with captions enabled
- Check if the video is publicly accessible
- Ensure stable internet connection

### "Invalid YouTube URL"
**Causes:**
- URL format is incorrect
- URL is not from YouTube

**Solutions:**
- Copy the URL directly from YouTube's address bar
- Ensure URL starts with `youtube.com` or `youtu.be`

### Slow Processing
**Normal:** Processing takes 30-60 seconds for typical videos
**Factors:**
- Video length (longer = slower)
- Number of segments
- Network speed for transcript download

## Example Videos to Try

Here are some good videos to test with (public talks with captions):

1. **TED Talks** - Most have official captions
2. **Google I/O** - Tech conference talks
3. **Apple WWDC** - Product announcements
4. **Company Earnings Calls** - Often have transcripts

## Files Created

When processing YouTube videos, these files are created:

- `data/youtube_transcript.json` - Extracted and formatted transcript
- Temporary files in `/tmp/` for exports

## Next Steps

### Enhancements Coming Soon:
- [ ] Support for multiple languages
- [ ] Speaker diarization (identify different speakers)
- [ ] Video timestamp links in generated content
- [ ] Direct upload of video files (not just URLs)
- [ ] Custom content templates
- [ ] AI-powered content enhancement with GPT-4

## Support

For issues or questions:
1. Check the terminal output for detailed error messages
2. Verify your YouTube URL is correct and accessible
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
