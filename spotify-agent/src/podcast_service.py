import json

from src.spotify_controller import _get_spotify_client


def search_podcasts(query: str, limit: int = 5) -> str:
    """Search for podcasts (shows) on Spotify."""
    try:
        sp = _get_spotify_client()
        results = sp.search(q=query, type="show", limit=limit)
        shows = []
        for item in results["shows"]["items"]:
            shows.append({
                "name": item["name"],
                "publisher": item["publisher"],
                "description": item["description"][:150],
                "total_episodes": item["total_episodes"],
                "id": item["id"],
                "uri": item["uri"],
            })
        return json.dumps({"status": "success", "podcasts": shows})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


def get_podcast_episodes(show_id: str, limit: int = 5) -> str:
    """Get episodes for a podcast show by its Spotify ID."""
    try:
        sp = _get_spotify_client()
        results = sp.show_episodes(show_id, limit=limit)
        episodes = []
        for item in results["items"]:
            episodes.append({
                "name": item["name"],
                "description": item["description"][:150],
                "duration_min": round(item["duration_ms"] / 60000, 1),
                "release_date": item["release_date"],
                "id": item["id"],
                "uri": item["uri"],
            })
        return json.dumps({"status": "success", "episodes": episodes})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
