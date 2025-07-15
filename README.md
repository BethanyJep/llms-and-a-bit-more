# LLMs and a Bit More

A comprehensive educational repository exploring **Large Language Models (LLMs)**, **Retrieval-Augmented Generation (RAG)**, **AI Agents**, and **Model Context Protocol (MCP)** through practical, hands-on examples.

[![Discord](https://dcbadge.limes.pink/api/server/ByRwuEEgH4)](https://aka.ms/genai-discord?WT.mc_id=academic-105485-koreyst)

## What's Inside

This repository contains practical demonstrations and implementations of modern AI technologies:

### **LLM Demonstrations** (`llms.ipynb`)
- **Azure OpenAI Integration**: Complete setup guide for Azure OpenAI services
- **Chat Conversations**: Build an AI study buddy for computer science topics
- **Image Generation**: Create visual aids using DALL-E
- **Educational Applications**: Real-world examples for students
- **Essay Writing Assistant**: Help with academic writing and outlines

### **RAG Implementation** (`rag.ipynb`)
- **Document Processing**: Extract text from PDF files (Constitution of Kenya 2010)
- **Text Chunking**: Intelligent document segmentation
- **Vector Embeddings**: Using Sentence Transformers for semantic search
- **FAISS Integration**: Efficient similarity search
- **Query System**: Ask questions about constitutional content

### **Spotify MCP Server** (`spotify-play-music/`)
A complete Model Context Protocol (MCP) server for Spotify integration:
- **Music Control**: Play, pause, skip tracks, and adjust volume
- **Apple Script Integration**: Native macOS Spotify control
- **MCP Tools**: Structured tool definitions for AI agents
- **Debug Support**: Built-in debugging with MCP Inspector
- **Agent Builder Integration**: Connect with AI Toolkit Agent Builder

## Getting Started

### Prerequisites
- Python 3.8+
- Azure OpenAI subscription (for LLM demos)
- Spotify application (for MCP server)
- macOS (for Spotify MCP server)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BethanyJep/llms-and-a-bit-more.git
   cd llms-and-a-bit-more
   ```

2. **For LLM Notebooks:**
   - Create a `.env` file with your Azure OpenAI credentials:
     ```env
     AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here
     AZURE_OPENAI_API_KEY=your_azure_api_key_here
     ```
   - Install dependencies:
     ```bash
     pip install openai python-dotenv requests pillow
     ```

3. **For RAG Implementation:**
   ```bash
   pip install pymupdf sentence-transformers faiss-cpu openai tiktoken
   ```

4. **For Spotify MCP Server:**
   ```bash
   cd spotify-play-music
   # Using uv (recommended)
   uv venv && uv pip install -r pyproject.toml --extra dev
   # Or using pip
   python -m venv .venv && pip install -e .[dev]
   ```

### Spotify MCP system prompt
[System ptompt:](/spotify.md)
Control Spotify playback effectively using specific tools for playing, pausing, skipping tracks, setting volume, and retrieving currently playing track information.

## Usage Examples

### LLM Chat Assistant
```python
# Create a conversation with AI
study_conversation = [
    {"role": "system", "content": "You are a helpful computer science tutor."},
    {"role": "user", "content": "Explain data structures simply."}
]
response = chat_with_ai(study_conversation)
```

### RAG Query System
```python
# Query the Constitution of Kenya
question = "What are the fundamental rights in Kenya?"
relevant_chunks = query_constitution(question, k=3)
```

### Spotify MCP Tools
- `play_music(query)`: Play specific songs, artists, or albums
- `pause_music()`: Pause current playback
- `next_track()` / `previous_track()`: Navigate tracks
- `get_current_track()`: Get currently playing track info
- `set_volume(level)`: Adjust volume (0-100)

## 🛠️ Features

- ✅ **Production-ready code** with error handling
- ✅ **Educational focus** with clear explanations
- ✅ **Practical examples** for real-world applications
- ✅ **Multiple AI technologies** in one repository
- ✅ **Cross-platform support** (Windows, macOS, Linux)
- ✅ **Documentation** and setup guides
- ✅ **Debugging tools** and testing frameworks

## Educational Resources

- [GenAI for Beginners](https://github.com/microsoft/generative-ai-for-beginners) - Microsoft's comprehensive guide to Generative AI
- [AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners?WT.mc_id=academic-105485-koreyst) - Learn about AI agents and autonomous systems
- [MCP for Beginners](https://github.com/microsoft/mcp-for-beginners?WT.mc_id=academic-105485-koreyst) - Model Context Protocol fundamentals
- [GitHub for Students](https://education.github.com/pack) - Free tools and resources for students
- [GitHub Models](https://github.com/marketplace?type=models) - Explore AI models on GitHub
- [Azure for Students](https://azure.microsoft.com/en-us/free/students) - Free Azure credits for students

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.


