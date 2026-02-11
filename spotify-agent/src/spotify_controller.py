import json
import os
import subprocess

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def _get_spotify_client() -> spotipy.Spotify:
    """Create a Spotify client using Client Credentials flow for searching."""
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    ))


def run_applescript(script: str) -> dict:
    """Execute AppleScript and return standardized response."""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return {"success": True, "output": result.stdout.strip()}
        return {"success": False, "error": result.stderr.strip()}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def play_music(query: str = "") -> str:
    """Play music on Spotify. If query is provided, search and play that song/artist/album."""
    if query:
        # Use Spotipy to search for the track and get its URI
        try:
            sp = _get_spotify_client()
            results = sp.search(q=query, type="track", limit=1)
            if results["tracks"]["items"]:
                track = results["tracks"]["items"][0]
                track_uri = track["uri"]
                track_name = track["name"]
                artist_name = track["artists"][0]["name"]
                
                # Play the track using AppleScript with the actual URI
                escaped_uri = track_uri.replace("'", "\\'")
                script = f'''tell application "Spotify"
                    activate
                    play track "{escaped_uri}"
                end tell'''
                result = run_applescript(script)
                
                if result["success"]:
                    return json.dumps({
                        "status": "success", 
                        "message": f"Playing '{track_name}' by {artist_name}"
                    })
                else:
                    return json.dumps({
                        "status": "error", 
                        "message": f"Failed to play: {result['error']}"
                    })
            else:
                return json.dumps({
                    "status": "error", 
                    "message": f"No tracks found for '{query}'"
                })
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
    else:
        script = '''tell application "Spotify"
            activate
            play
        end tell'''
        result = run_applescript(script)
        status = "success" if result["success"] else "error"
        msg = "Resuming playback" if result["success"] else f"Failed: {result['error']}"
        return json.dumps({"status": status, "message": msg})


def play_uri(uri: str) -> str:
    """Play a specific Spotify URI (track, episode, etc.)."""
    escaped_uri = uri.replace("'", "\\'")
    script = f'''tell application "Spotify"
        activate
        play track "{escaped_uri}"
    end tell'''

    result = run_applescript(script)
    status = "success" if result["success"] else "error"
    msg = f"Playing URI {uri}" if result["success"] else f"Failed: {result['error']}"
    return json.dumps({"status": status, "message": msg})


def pause_music() -> str:
    """Pause Spotify playback."""
    result = run_applescript('tell application "Spotify" to pause')
    status = "success" if result["success"] else "error"
    msg = "Music paused" if result["success"] else f"Failed to pause: {result['error']}"
    return json.dumps({"status": status, "message": msg})


def next_track() -> str:
    """Skip to next track on Spotify."""
    result = run_applescript('tell application "Spotify" to next track')
    status = "success" if result["success"] else "error"
    msg = "Skipped to next track" if result["success"] else f"Failed to skip: {result['error']}"
    return json.dumps({"status": status, "message": msg})


def previous_track() -> str:
    """Go to previous track on Spotify."""
    result = run_applescript('tell application "Spotify" to previous track')
    status = "success" if result["success"] else "error"
    msg = "Went to previous track" if result["success"] else f"Failed to go back: {result['error']}"
    return json.dumps({"status": status, "message": msg})


def get_current_track() -> str:
    """Get information about the currently playing track."""
    script = '''tell application "Spotify"
        set current_track to current track
        return (name of current_track) & "|" & (artist of current_track) & "|" & (album of current_track) & "|" & (player state as string)
    end tell'''

    result = run_applescript(script)
    if not result["success"]:
        return json.dumps({"status": "error", "message": f"Failed to get track info: {result['error']}"})

    track_info = result["output"].split("|")
    if len(track_info) >= 4:
        return json.dumps({
            "status": "success",
            "track": track_info[0],
            "artist": track_info[1],
            "album": track_info[2],
            "player_state": track_info[3],
        })
    return json.dumps({"status": "error", "message": "Could not parse track info"})


def set_volume(volume: int) -> str:
    """Set Spotify volume (0-100)."""
    if not 0 <= volume <= 100:
        return json.dumps({"status": "error", "message": "Volume must be between 0 and 100"})

    result = run_applescript(f'tell application "Spotify" to set sound volume to {volume}')
    status = "success" if result["success"] else "error"
    msg = f"Volume set to {volume}%" if result["success"] else f"Failed to set volume: {result['error']}"
    return json.dumps({"status": status, "message": msg})
