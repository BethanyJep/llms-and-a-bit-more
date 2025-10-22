# 🚀 Azure OpenAI Setup Guide

## Overview

This Event Coverage Agent now uses **Azure OpenAI** to generate intelligent, context-aware content from YouTube videos. It can also use regular OpenAI if you prefer.

---

## 📋 Prerequisites

1. **Azure Account** with an active subscription
2. **Azure OpenAI Service** resource deployed
3. **GPT-4 or GPT-4o-mini** model deployed in your Azure OpenAI resource

---

## 🔧 Step-by-Step Setup

### Step 1: Create Azure OpenAI Resource

1. Go to [Azure Portal](https://portal.azure.com/)
2. Click **"Create a resource"**
3. Search for **"Azure OpenAI"**
4. Click **"Create"**
5. Fill in:
   - **Subscription**: Your Azure subscription
   - **Resource Group**: Create new or use existing
   - **Region**: Choose a region (e.g., East US, West Europe)
   - **Name**: Give it a unique name (e.g., `my-openai-resource`)
   - **Pricing Tier**: Standard S0
6. Click **"Review + Create"** → **"Create"**
7. Wait for deployment to complete

### Step 2: Deploy a Model

1. Go to your Azure OpenAI resource
2. Click **"Model deployments"** in the left menu
3. Click **"Create new deployment"**
4. Select:
   - **Model**: `gpt-4o-mini` (recommended for cost) or `gpt-4`
   - **Deployment name**: `gpt-4o-mini` (remember this!)
   - **Version**: Latest available
5. Click **"Create"**

### Step 3: Get Your Credentials

1. In your Azure OpenAI resource, go to **"Keys and Endpoint"**
2. Copy:
   - **Key 1** (your API key)
   - **Endpoint** (looks like `https://your-resource-name.openai.azure.com/`)

### Step 4: Configure the .env File

1. **Copy the example file:**
   ```bash
   cd event-coverage-agent
   cp .env.example .env
   ```

2. **Edit `.env` file:**
   ```bash
   nano .env  # or use any text editor
   ```

3. **Fill in your credentials:**
   ```env
   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=your-actual-api-key-here
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
   
   # Use Azure OpenAI (default)
   USE_OPENAI=false
   ```

4. **Save the file**

### Step 5: Install Dependencies

```bash
cd event-coverage-agent
source ../.venv/bin/activate
pip install -r requirements.txt
```

This installs:
- `openai` - OpenAI Python SDK (supports Azure)
- `python-dotenv` - For loading .env files

### Step 6: Test Your Setup

```bash
python test_openai.py
```

You should see:
```
🧪 Testing Azure OpenAI Integration
=====================================
✓ Step 1: Checking for .env file...
✅ .env file found

✓ Step 2: Checking environment variables...
📌 Using Azure OpenAI API
✅ Azure OpenAI API Key: ab12cd34ef...5678
✅ Azure Endpoint: https://your-resource.openai.azure.com/
✅ Deployment Name: gpt-4o-mini
✅ API Version: 2024-02-15-preview

✓ Step 3: Importing OpenAI library...
✅ OpenAI library imported successfully

✓ Step 4: Initializing OpenAI client...
✅ Client initialized successfully

✓ Step 5: Testing API connection...
✅ API test successful!
   Response: Hello from Event Coverage Agent!

✓ Step 6: Testing AI generator module...
✅ Using Azure OpenAI - Endpoint: https://your-resource.openai.azure.com/
   Deployment: gpt-4o-mini
✅ AI generator module works!

🎉 ALL TESTS PASSED!
```

### Step 7: Run the Agent

```bash
python app.py
```

Open http://localhost:5001 in your browser!

---

## 🔄 Alternative: Use Regular OpenAI Instead

If you prefer to use OpenAI instead of Azure OpenAI:

1. Get an API key from [OpenAI Platform](https://platform.openai.com/)
2. Edit your `.env` file:
   ```env
   USE_OPENAI=true
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```
3. Run the test: `python test_openai.py`

---

## 💰 Cost Estimates

### Azure OpenAI Pricing (GPT-4o-mini)
- **Input**: $0.15 per 1M tokens
- **Output**: $0.60 per 1M tokens

### Typical Usage per Video (15 minutes)
- Transcript: ~3,000 tokens input
- All content generation: ~7,000 tokens output
- **Cost per video: ~$0.01-0.02** (1-2 cents)

### Free Credits
- Azure offers $200 free credits for new accounts
- That's **10,000-20,000 videos** with free credits!

---

## 🐛 Troubleshooting

### "AI configuration error: Missing required environment variables"
**Solution:**
- Check that `.env` file exists in the `event-coverage-agent` folder
- Verify all required variables are set:
  - `AZURE_OPENAI_API_KEY`
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_DEPLOYMENT_NAME`

### "API call failed: Resource not found"
**Solution:**
- Verify your deployment name matches exactly what you set in Azure Portal
- Check that the deployment is in the same region as your endpoint
- Ensure the deployment is not paused or deleted

### "API call failed: Invalid API key"
**Solution:**
- Copy the key again from Azure Portal → Keys and Endpoint
- Make sure there are no extra spaces in the `.env` file
- Try using Key 2 instead of Key 1

### "API call failed: Quota exceeded"
**Solution:**
- Check your Azure subscription quota limits
- Wait a few minutes (rate limiting)
- Consider upgrading to a higher pricing tier

### ".env file not found"
**Solution:**
```bash
cd event-coverage-agent
cp .env.example .env
# Then edit .env with your credentials
```

### "Deployment not found"
**Solution:**
- Go to Azure Portal → Your OpenAI Resource → Model Deployments
- Verify the deployment exists and note the exact name
- Update `AZURE_OPENAI_DEPLOYMENT_NAME` in `.env` to match

---

## 📁 File Structure

```
event-coverage-agent/
├── .env                    # Your credentials (DO NOT commit to git!)
├── .env.example           # Template file (safe to commit)
├── test_openai.py         # Test script for Azure OpenAI
├── app.py                 # Flask web application
├── requirements.txt       # Python dependencies
└── src/
    ├── ai_generator.py    # Azure OpenAI integration
    └── server.py          # MCP tools with AI
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` file to git**
   - Already in `.gitignore`
   - Contains sensitive API keys

2. **Rotate keys regularly**
   - Azure Portal → Keys and Endpoint → Regenerate keys

3. **Use separate keys for dev/prod**
   - Create different Azure OpenAI resources for testing and production

4. **Monitor usage**
   - Azure Portal → Cost Management
   - Set up budget alerts

---

## ✅ Verification Checklist

Before running the agent, verify:

- [ ] `.env` file exists
- [ ] All Azure credentials are filled in
- [ ] Deployment name matches Azure Portal
- [ ] `python test_openai.py` passes all tests
- [ ] Dependencies installed: `pip install -r requirements.txt`

---

## 🎉 You're All Set!

Your Event Coverage Agent is now configured with Azure OpenAI. Try it with a YouTube video and see the AI-generated content!

**Next steps:**
1. Run `python app.py`
2. Open http://localhost:5001
3. Paste a YouTube URL
4. Watch the AI generate amazing content! 🚀

---

## 📚 Additional Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Azure OpenAI Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)
- [OpenAI Python SDK Docs](https://github.com/openai/openai-python)
- [Model Deployment Guide](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource)
