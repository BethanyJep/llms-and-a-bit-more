# 🔍 Debugging Guide: "Getting Zero Content"

## Issue Summary

You've successfully:
- ✅ Configured Azure OpenAI (test passed)
- ✅ Extracted YouTube transcript (58 segments, 117 minutes)
- ✅ Fixed JavaScript errors

But when you process the YouTube video, **you're getting zero content displayed**.

---

## What We Know

### ✅ Working Parts:

1. **Azure OpenAI Configuration:**
   ```
   API Key: 4HgazE2gTV...8Frx ✓
   Endpoint: https://bethanycheum-5318-resource.openai.azure.com/ ✓
   Deployment: gpt-4.1 ✓
   Test: PASSED ✓
   ```

2. **YouTube Transcript Extraction:**
   ```
   Video ID: ceV3RsG946s ✓
   Event: Microsoft Build 2025 (Satya Nadella keynote) ✓
   Duration: 117 minutes ✓
   Segments: 58 ✓
   File: data/youtube_transcript.json (107KB) ✓
   ```

3. **JavaScript UI:**
   ```
   Fixed null checks ✓
   Added console logging ✓
   Safe error handling ✓
   ```

### ❓ Unknown Parts:

1. **Is the AI actually being called?**
2. **Is the AI returning data?**
3. **Is the data structure correct?**

---

## Debugging Steps

### Step 1: Check Browser Console

When you process a YouTube video:

1. Open **Browser DevTools** (F12 or Cmd+Option+I)
2. Go to **Console** tab
3. Click "Process YouTube Video"
4. Look for these debug logs:

```javascript
YouTube API Response: {...}  // Should show the full response
Outputs received: {...}       // Should show the outputs
displayAllContent called with: {...}  // Should show what's being displayed
```

**What to look for:**
- ❌ If you see errors about Azure OpenAI
- ❌ If `outputs` is empty: `{}`
- ❌ If `outputs.press_quotes` is `undefined` or `null`
- ✅ If you see actual quote data

### Step 2: Check Flask Server Logs

In your terminal where Flask is running, look for:

```
🎥 Processing YouTube Video
📥 Extracting transcript from YouTube...
✓ Extracted 58 segments
✓ Total words: XXXX
✓ Duration: 1:57:29

🤖 Processing transcript with AI agent...
📝 Using already processed transcript: youtube_transcript.json
💬 Extracting press quotes...
🤖 Using AI to extract press quotes...  ← KEY LINE
```

**What to look for:**
- ❌ If you see errors about deployment not found
- ❌ If you see errors about rate limits
- ❌ If AI calls are not showing "🤖 Using AI to..."
- ✅ If you see successful AI completion messages

### Step 3: Test AI Generation Manually

Run this in terminal:

```bash
python -c "
import asyncio
import sys
sys.path.insert(0, 'src')
from server import extract_press_quotes, set_transcript_file
from dotenv import load_dotenv
load_dotenv()

# Set to use YouTube transcript
set_transcript_file('youtube_transcript.json')

# Try to generate quotes
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
result = loop.run_until_complete(extract_press_quotes())
loop.close()

import json
data = json.loads(result)
print('Status:', data.get('status'))
if data.get('status') == 'error':
    print('ERROR:', data.get('message'))
else:
    print('Quotes found:', data.get('total_quotes'))
    print('AI Generated:', data.get('ai_generated'))
"
```

**Expected output:**
```
Status: success
Quotes found: 5-8
AI Generated: True
```

**If error:**
```
Status: error
ERROR: <error message here>
```

---

## Common Issues & Solutions

### Issue 1: "Deployment not found"

**Error in logs:**
```
DeploymentNotFound: The API deployment for this resource does not exist
```

**Solution:**
1. Check your deployment name in Azure Portal
2. Go to Azure OpenAI Studio → Deployments
3. Copy the EXACT deployment name
4. Update `.env`:
   ```
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4  # or whatever it's called
   ```

### Issue 2: "Rate limit exceeded"

**Error in logs:**
```
RateLimitError: Rate limit reached for requests
```

**Solution:**
- Wait a few minutes
- Or check your Azure quota limits
- Or upgrade to higher tier

### Issue 3: "Content returned but not displayed"

**Symptoms:**
- Flask logs show success
- But UI shows nothing

**Debug:**
1. Check browser console for structure:
   ```javascript
   console.log(result.data.outputs.press_quotes)
   ```
2. Verify the structure matches:
   ```javascript
   {
     status: "success",
     quotes: [...]  // Array of quotes
   }
   ```

### Issue 4: "AI returning empty arrays"

**Symptoms:**
- No errors
- But `quotes: []` is empty

**Possible causes:**
- AI is returning data in wrong format
- JSON parsing is failing
- AI prompt is not working correctly

**Test:**
```bash
# Check what AI is actually returning
python -c "
from src.ai_generator import initialize_openai, generate_press_quotes_ai
from src.utils import load_json_file, get_data_path
from dotenv import load_dotenv
load_dotenv()

initialize_openai()
transcript_data = load_json_file(get_data_path('youtube_transcript.json'))
quotes = generate_press_quotes_ai(transcript_data)
print('AI returned:', len(quotes), 'quotes')
print('First quote:', quotes[0] if quotes else 'NONE')
"
```

---

## Quick Fix Checklist

- [ ] `.env` file has correct Azure credentials
- [ ] Deployment name matches Azure Portal
- [ ] `python test_openai.py` passes all tests
- [ ] YouTube transcript exists in `data/youtube_transcript.json`
- [ ] Flask server is running without errors
- [ ] Browser console shows API response
- [ ] Manual test command returns quotes

---

## Next Steps

1. **Run Step 3 (Manual Test)** to see if AI generation works at all
2. **Check browser console** to see what data structure is returned
3. **Share the error message** from either:
   - Browser console logs
   - Flask server logs
   - Manual test output

Once you share those, I can pinpoint the exact issue!

---

## Quick Test Command

Run this complete test:

```bash
cd event-coverage-agent
source ../.venv/bin/activate

echo "=== Testing Azure OpenAI ==="
python test_openai.py

echo -e "\n=== Testing YouTube Transcript ==="
ls -lh data/youtube_transcript.json

echo -e "\n=== Testing AI Quote Generation ==="
python -c "
import asyncio, sys, json
sys.path.insert(0, 'src')
from server import extract_press_quotes, set_transcript_file
from dotenv import load_dotenv
load_dotenv()

set_transcript_file('youtube_transcript.json')
loop = asyncio.new_event_loop()
result = loop.run_until_complete(extract_press_quotes())
loop.close()

data = json.loads(result)
print('Status:', data.get('status'))
if data.get('status') == 'error':
    print('ERROR:', data.get('message'))
else:
    print('SUCCESS: Found', data.get('total_quotes'), 'quotes')
"

echo -e "\n=== If all above pass, start Flask ==="
echo "python app.py"
```

This will tell us exactly where the problem is!
