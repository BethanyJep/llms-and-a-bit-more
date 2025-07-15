import json
import subprocess
from mcp.server.fastmcp import FastMCP

server = FastMCP("spotify_play_music")

def run_applescript(script: str) -> dict:
    """Helper function to execute AppleScript and return standardized response."""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return {"success": True, "output": result.stdout.strip()}
        else:
            return {"success": False, "error": result.stderr.strip()}
            
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@server.tool()
async def play_music(query: str = "") -> str:
    """Play music on Spotify. If query is provided, search and play that song/artist/album."""
    if query:
        escaped_query = query.replace("'", "\\'")
        script = f'''tell application "Spotify"
            activate
            play track "spotify:search:{escaped_query}"
        end tell'''
        message = f"Playing '{query}'"
    else:
        script = '''tell application "Spotify"
            activate
            play
        end tell'''
        message = "Resuming playback"
    
    result = run_applescript(script)
    status = "success" if result["success"] else "error"
    msg = message if result["success"] else f"Failed: {result['error']}"
    return json.dumps({"status": status, "message": msg})

@server.tool()
async def pause_music() -> str:
    """Pause Spotify playback."""
    result = run_applescript('tell application "Spotify" to pause')
    status = "success" if result["success"] else "error"
    msg = "Music paused" if result["success"] else f"Failed to pause: {result['error']}"
    return json.dumps({"status": status, "message": msg})

@server.tool()
async def next_track() -> str:
    """Skip to next track on Spotify."""
    result = run_applescript('tell application "Spotify" to next track')
    status = "success" if result["success"] else "error"
    msg = "Skipped to next track" if result["success"] else f"Failed to skip: {result['error']}"
    return json.dumps({"status": status, "message": msg})

@server.tool()
async def previous_track() -> str:
    """Go to previous track on Spotify."""
    result = run_applescript('tell application "Spotify" to previous track')
    status = "success" if result["success"] else "error"
    msg = "Went to previous track" if result["success"] else f"Failed to go back: {result['error']}"
    return json.dumps({"status": status, "message": msg})

@server.tool()
async def get_current_track() -> str:
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
            "player_state": track_info[3]
        })
    else:
        return json.dumps({"status": "error", "message": "Could not parse track info"})

@server.tool()
async def set_volume(volume: int) -> str:
    """Set Spotify volume (0-100)."""
    if not 0 <= volume <= 100:
        return json.dumps({"status": "error", "message": "Volume must be between 0 and 100"})
    
    result = run_applescript(f'tell application "Spotify" to set sound volume to {volume}')
    status = "success" if result["success"] else "error"
    msg = f"Volume set to {volume}%" if result["success"] else f"Failed to set volume: {result['error']}"
    return json.dumps({"status": status, "message": msg})
