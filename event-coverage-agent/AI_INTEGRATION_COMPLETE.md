# AI-Powered Event Coverage Agent - UPDATED

## 🚀 What Changed?

The Event Coverage Agent now uses **AI (OpenAI GPT-4o-mini)** to generate content that actually matches your YouTube video content!

### Before (❌ Old Version):
- Used basic text processing and keyword matching
- Content was generic and didn't understand the video
- Just filtered segments by patterns
- Output didn't match YouTube video content

### After (✅ New Version):
- Uses **OpenAI's GPT-4o-mini** to understand the transcript
- Generates relevant, contextual content based on actual video
- Creates engaging quotes, social posts, press releases
- Content now **matches your YouTube video**!

---

## 🔧 Setup Instructions

### 1. Get an OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to **API Keys** section
4. Click **"Create new secret key"**
5. Copy the key (it starts with `sk-...`)

### 2. Set the Environment Variable

**On macOS/Linux:**
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

**Or add to your `~/.zshrc` or `~/.bashrc` to make it permanent:**
```bash
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**On Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-api-key-here"
```

### 3. Verify the Setup

```bash
cd event-coverage-agent
source ../.venv/bin/activate
python -c "import os; print('API Key set!' if os.environ.get('OPENAI_API_KEY') else 'API Key NOT set')"
```

### 4. Run the Agent

```bash
python app.py
```

Then open http://localhost:5001 in your browser!

---

## 🎯 How It Works Now

### 1. **YouTube Transcript Extraction** (Same as before)
   - Extracts transcript from YouTube video
   - Segments into 120-second chunks
   - Saves to `data/youtube_transcript.json`

### 2. **AI Content Generation** (NEW!)
   
   **Press Quotes:**
   - AI analyzes the entire transcript
   - Identifies 5-8 most impactful quotes
   - Provides context and significance
   - Uses actual speaker names from video
   
   **Social Media Posts:**
   - **Twitter:** Creates engaging 280-char tweets with hashtags
   - **LinkedIn:** Professional long-form posts with insights
   - **Instagram:** Visual-friendly captions with storytelling
   
   **Press Release:**
   - Complete professional press release
   - Uses actual quotes from the video
   - Highlights key announcements
   - Proper formatting with contact info
   
   **Newsletter:**
   - Engaging post-event recap
   - Executive summary of content
   - Key takeaways and memorable quotes
   - Call-to-action and contact info

---

## 💰 Cost Estimate

Using GPT-4o-mini (very cost-effective):
- **~$0.15 per 1M input tokens**
- **~$0.60 per 1M output tokens**

For a typical 15-minute video:
- Transcript: ~3,000 tokens
- All content generation: ~10,000 tokens total
- **Cost per video: ~$0.01-0.02** (1-2 cents!)

---

## 🧪 Testing

1. **Start the server:**
   ```bash
   python app.py
   ```

2. **Open browser:** http://localhost:5001

3. **Add a YouTube URL** like:
   - `https://www.youtube.com/watch?v=arj7oStGLkU`

4. **Click "Process YouTube Video"**

5. **Wait for AI to generate content** (takes 10-30 seconds)

6. **Check the output** - it should now match the video content!

---

## 🐛 Troubleshooting

### "OpenAI API key not configured"
- Make sure you set the environment variable: `export OPENAI_API_KEY="sk-..."`
- Restart the terminal after setting it
- Verify with: `echo $OPENAI_API_KEY`

### "Rate limit exceeded"
- OpenAI has usage limits for free tier
- Upgrade to paid tier or wait a few minutes

### "Invalid API key"
- Check that your API key is correct
- Make sure there are no extra spaces
- Regenerate a new key if needed

### "Content still doesn't match video"
- Check the terminal logs to see if AI is being used
- Look for `🤖 Using AI to...` messages
- Ensure OpenAI API key is set correctly

---

## 📝 Files Modified

1. **`src/ai_generator.py`** (NEW)
   - AI-powered content generation functions
   - Uses OpenAI GPT-4o-mini model
   - Handles quotes, social posts, press releases, newsletters

2. **`src/server.py`** (UPDATED)
   - Now imports and uses AI functions
   - Replaced keyword-based logic with AI calls
   - Better error handling for API key issues

3. **`src/youtube_processor.py`** (NO CHANGES)
   - Still extracts YouTube transcripts
   - Works the same as before

4. **`app.py`** (MINOR UPDATES)
   - Fixed global state bug
   - Now passes `skip_transcript_processing=True` parameter

---

## 🎉 Try It Now!

The agent will now generate content that **actually understands and reflects your YouTube video**!

**Example:** If your video is about AI development, the quotes, social posts, and press release will discuss AI development - not generic TechCorp announcements!

---

## 📚 Next Steps

- Try different YouTube videos
- Customize the prompts in `ai_generator.py` for your specific needs
- Adjust temperature settings for more/less creative output
- Add support for other AI models (Claude, Gemini, etc.)

---

## ✨ Enjoy Your AI-Powered PR Agent!
