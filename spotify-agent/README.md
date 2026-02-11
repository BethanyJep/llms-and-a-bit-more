# Spotify Agent

AI-powered Spotify assistant built with [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) and Azure OpenAI. Controls music playback via AppleScript and discovers podcasts via the Spotify Web API.

## Features

- **Music Playback** — Play, pause, skip, previous track, volume control
- **Now Playing** — Get current track info (name, artist, album, state)
- **Podcast Discovery** — Search podcasts and browse episodes
- **Podcast Playback** — Play specific podcast episodes
- **Conversational** — Natural language interaction

## Prerequisites

- **macOS** (uses AppleScript for Spotify control)
- **Python 3.10+**
- **Spotify Desktop App** installed and logged in
- **Azure OpenAI** resource with a deployed model (e.g. `gpt-4o`)
- **Azure CLI** logged in (`az login`)
- **Spotify Developer App** for search/podcasts ([developer.spotify.com](https://developer.spotify.com/dashboard))

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure OpenAI and Spotify credentials
   ```

3. **Login to Azure CLI:**
   ```bash
   az login
   ```

4. **Run the agent:**
   ```bash
   python client.py
   ```

## Usage

```
🎵 Spotify Agent (type 'quit' to exit)
----------------------------------------

You: Play some jazz music
Agent: 🎵 Now playing jazz music on Spotify!

You: Search for tech podcasts
Agent: Here are some tech podcasts I found: ...

You: Play the latest episode of the first one
Agent: 🎧 Playing the latest episode!

You: What's currently playing?
Agent: Currently playing "Kind of Blue" by Miles Davis
```

## Architecture

```mermaid
flowchart TB
    subgraph User
        CLI[["🎵 client.py<br/>(CLI Chat Loop)"]]
    end

    subgraph Agent["Microsoft Agent Framework"]
        AG["Agent<br/>(agent.py)"]
        AOAI["Azure OpenAI<br/>(gpt-4o)"]
        AG <--> AOAI
    end

    subgraph Tools["@tool Functions"]
        direction LR
        T1[play_music]
        T2[pause_music]
        T3[next_track]
        T4[previous_track]
        T5[set_volume]
        T6[get_current_track]
        T7[search_podcasts]
        T8[get_podcast_episodes]
        T9[play_episode]
    end

    subgraph Services
        SC["spotify_controller.py"]
        PS["podcast_service.py"]
    end

    subgraph External
        SPOT_API[("Spotify Web API<br/>(Spotipy)")]
        SPOT_APP[["🎧 Spotify Desktop App<br/>(AppleScript)"]]
    end

    CLI -->|"user input"| AG
    AG -->|"response"| CLI
    AG -->|"calls"| Tools
    
    T1 & T2 & T3 & T4 & T5 & T6 --> SC
    T7 & T8 --> PS
    T9 --> SC

    SC -->|"search tracks"| SPOT_API
    SC -->|"play/pause/skip"| SPOT_APP
    PS -->|"search podcasts"| SPOT_API
```

### File Structure

```
spotify-agent/
├── client.py                 # CLI chat loop
├── requirements.txt
├── .env.example
└── src/
    ├── agent.py              # Agent + Azure OpenAI setup with @tool functions
    ├── spotify_controller.py # AppleScript-based Spotify control + search
    └── podcast_service.py    # Spotify Web API podcast search
```

### Tools

| Tool | Description |
|------|-------------|
| `play_music` | Play/search music |
| `pause_music` | Pause playback |
| `next_track` | Skip to next |
| `previous_track` | Go back |
| `set_volume` | Set volume 0-100 |
| `get_current_track` | Now playing info |
| `search_podcasts` | Find podcasts |
| `get_podcast_episodes` | List episodes |
| `play_episode` | Play a podcast episode |
