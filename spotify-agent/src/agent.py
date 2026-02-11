from typing import Annotated

from dotenv import load_dotenv
from pydantic import Field
from agent_framework import Agent, tool
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

from src.spotify_controller import (
    get_current_track as _get_current_track,
    next_track as _next_track,
    pause_music as _pause_music,
    play_music as _play_music,
    play_uri as _play_uri,
    previous_track as _previous_track,
    set_volume as _set_volume,
)
from src.podcast_service import (
    get_podcast_episodes as _get_podcast_episodes,
    search_podcasts as _search_podcasts,
)

load_dotenv()

AGENT_INSTRUCTIONS = """You are a Spotify DJ assistant. You can control music playback, 
search for and play podcasts, and manage volume. When users ask to play something, 
use the appropriate tool. For podcasts, search first, then list episodes, and play 
the one the user wants. Always confirm actions with a brief, friendly response."""


# Define tool functions with @tool decorator for the agent
@tool
def play_music(
    query: Annotated[str, Field(description="The song, artist, or album to search and play. Leave empty to resume playback.")] = ""
) -> str:
    """Play music on Spotify. If query is provided, search and play that song/artist/album. If empty, resume playback."""
    return _play_music(query)


@tool
def pause_music() -> str:
    """Pause Spotify playback."""
    return _pause_music()


@tool
def next_track() -> str:
    """Skip to next track on Spotify."""
    return _next_track()


@tool
def previous_track() -> str:
    """Go to previous track on Spotify."""
    return _previous_track()


@tool
def set_volume(
    volume: Annotated[int, Field(description="Volume level from 0 to 100.")]
) -> str:
    """Set Spotify volume (0-100)."""
    return _set_volume(volume)


@tool
def get_current_track() -> str:
    """Get information about the currently playing track including name, artist, album, and player state."""
    return _get_current_track()


@tool
def search_podcasts(
    query: Annotated[str, Field(description="The podcast name or topic to search for.")]
) -> str:
    """Search for podcasts on Spotify. Returns a list of matching shows with name, publisher, description, and ID."""
    return _search_podcasts(query)


@tool
def get_podcast_episodes(
    show_id: Annotated[str, Field(description="The Spotify show ID from search_podcasts.")]
) -> str:
    """Get recent episodes for a podcast show. Requires the Spotify show ID (from search_podcasts)."""
    return _get_podcast_episodes(show_id)


@tool
def play_episode(
    episode_uri: Annotated[str, Field(description="The Spotify URI for the episode to play (e.g. spotify:episode:xxx).")]
) -> str:
    """Play a specific podcast episode by its Spotify URI."""
    return _play_uri(episode_uri)


def create_agent() -> Agent:
    """Create and return the Spotify agent using Microsoft Agent Framework."""
    return Agent(
        client=AzureOpenAIChatClient(credential=AzureCliCredential()),
        name="SpotifyAgent",
        instructions=AGENT_INSTRUCTIONS,
        tools=[
            play_music,
            pause_music,
            next_track,
            previous_track,
            set_volume,
            get_current_track,
            search_podcasts,
            get_podcast_episodes,
            play_episode,
        ],
    )
