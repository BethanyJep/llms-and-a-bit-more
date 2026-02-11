# 🎵 Spotify Control MCP Server

An MCP Server for controlling Spotify playback on macOS using AppleScript. Control your music with natural language through AI agents. It includes the following features:

- **Music Playback Control**: Play, pause, skip tracks, and search for songs
- **Volume Management**: Adjust Spotify volume programmatically
- **Track Information**: Get details about currently playing tracks
- **Connect to Agent Builder**: Test and debug the MCP server with AI Toolkit
- **Debug in [MCP Inspector](https://github.com/modelcontextprotocol/inspector)**: Visual debugging tool for MCP servers

## Get started with the Spotify Control MCP Server

> **Prerequisites**
>
> To run the MCP Server on your local dev machine, you will need:
>
> - [Python](https://www.python.org/) 3.10 or higher
> - **Spotify Desktop App** installed on macOS
> - (*Optional - if you prefer uv*) [uv](https://github.com/astral-sh/uv)
> - [Python Debugger Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)

## Prepare environment

There are two approaches to set up the environment for this project. You can choose either one based on your preference.

> Note: Reload VSCode or terminal to ensure the virtual environment python is used after creating the virtual environment.

| Approach | Steps |
| -------- | ----- |
| Using `uv` | 1. Create virtual environment: `uv venv` <br>2. Run VSCode Command "***Python: Select Interpreter***" and select the python from created virtual environment <br>3. Install dependencies (include dev dependencies): `uv pip install -r pyproject.toml --extra dev` |
| Using `pip` | 1. Create virtual environment: `python -m venv .venv` <br>2. Run VSCode Command "***Python: Select Interpreter***" and select the python from created virtual environment<br>3. Install dependencies (include dev dependencies): `pip install -e .[dev]` | 

After setting up the environment, you can run the server in your local dev machine via Agent Builder as the MCP Client to get started:
1. **Make sure Spotify Desktop App is installed and running** on your macOS machine
2. Open VS Code Debug panel. Select `Debug in Agent Builder` or press `F5` to start debugging the MCP server.
3. Use AI Toolkit Agent Builder to test the server with [this prompt](vscode://ms-windows-ai-studio.windows-ai-studio/open_prompt_builder?model_id=github/gpt-4o-mini&system_prompt=You%20are%20a%20music%20assistant%20that%20can%20control%20Spotify%20playback&user_prompt=Play%20some%20energetic%20rock%20music&track_from=vsc_md&mcp=spotify_play_music). Server will be auto-connected to the Agent Builder.
4. Click `Run` to test the server with the prompt.

**Congratulations**! You have successfully run the Spotify Control MCP Server in your local dev machine via Agent Builder as the MCP Client.
![DebugMCP](https://raw.githubusercontent.com/microsoft/windows-ai-studio-templates/refs/heads/dev/mcpServers/mcp_debug.gif)

## Available Tools

| Tool | Description | Example Usage |
| ---- | ----------- | ------------- |
| `play_music(query)` | Search and play a track, artist, or album on Spotify | "Play Bohemian Rhapsody" |
| `pause_music()` | Pause the current playback | "Pause the music" |
| `next_track()` | Skip to the next track | "Play the next song" |
| `previous_track()` | Go back to the previous track | "Go back to the previous track" |
| `get_current_track()` | Get information about the currently playing track | "What's playing right now?" |
| `set_volume(volume)` | Set Spotify volume (0-100) | "Set volume to 75" |

## What's included in the template

| Folder / File| Contents                                     |
| ------------ | -------------------------------------------- |
| `.vscode`    | VSCode files for debugging                   |
| `.aitk`      | Configurations for AI Toolkit                |
| `src`        | The source code for the Spotify MCP server   |
| `inspector`  | MCP Inspector configuration                  |

## How to debug the Spotify Control MCP Server

> Notes:
> - [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is a visual developer tool for testing and debugging MCP servers.
> - All debugging modes support breakpoints, so you can add breakpoints to the tool implementation code.
> - **Spotify Desktop App must be running** for the tools to work properly.

| Debug Mode | Description | Steps to debug |
| ---------- | ----------- | --------------- |
| Agent Builder | Debug the MCP server in the Agent Builder via AI Toolkit. | 1. Open VS Code Debug panel. Select `Debug in Agent Builder` and press `F5` to start debugging the MCP server.<br>2. Use AI Toolkit Agent Builder to test the server with [this prompt](vscode://ms-windows-ai-studio.windows-ai-studio/open_prompt_builder?model_id=github/gpt-4o-mini&system_prompt=You%20are%20a%20music%20assistant%20that%20can%20control%20Spotify%20playback&user_prompt=Play%20some%20jazz%20music&track_from=vsc_md&mcp=spotify_play_music). Server will be auto-connected to the Agent Builder.<br>3. Click `Run` to test the server with the prompt. |
| MCP Inspector | Debug the MCP server using the MCP Inspector. | 1. Install [Node.js](https://nodejs.org/)<br> 2. Set up Inspector: `cd inspector` && `npm install` <br> 3. Open VS Code Debug panel. Select `Debug SSE in Inspector (Edge)` or `Debug SSE in Inspector (Chrome)`. Press F5 to start debugging.<br> 4. When MCP Inspector launches in the browser, click the `Connect` button to connect this MCP server.<br> 5. Then you can `List Tools`, select a tool, input parameters, and `Run Tool` to debug your server code.<br> |

## Default Ports and customizations

| Debug Mode | Ports | Definitions | Customizations | Note |
| ---------- | ----- | ------------ | -------------- |-------------- |
| Agent Builder | 3001 | [tasks.json](.vscode/tasks.json) | Edit [launch.json](.vscode/launch.json), [tasks.json](.vscode/tasks.json), [\_\_init\_\_.py](src/__init__.py), [mcp.json](.aitk/mcp.json) to change above ports. | N/A |
| MCP Inspector | 3001 (Server); 5173 and 3000 (Inspector) | [tasks.json](.vscode/tasks.json) | Edit [launch.json](.vscode/launch.json), [tasks.json](.vscode/tasks.json), [\_\_init\_\_.py](src/__init__.py), [mcp.json](.aitk/mcp.json) to change above ports.| N/A |

## Platform Support

**Current:** macOS only (uses AppleScript to control Spotify Desktop App)

**Future:** Windows and Linux support planned using Spotify Web API

## Troubleshooting

### "Failed to execute command" errors
- Make sure Spotify Desktop App is installed and running
- Check that Spotify is not in a restricted state (e.g., during ads on free tier)

### No audio playing
- Verify Spotify app has an active device selected
- Check system volume and Spotify volume levels

### Search not working
- Ensure you have an active Spotify Premium account (search may be limited on free tier)
- Try more specific search queries (include artist name)

## Feedback

If you have any feedback or suggestions for this MCP server, please open an issue on the [AI Toolkit GitHub repository](https://github.com/microsoft/vscode-ai-toolkit/issues)