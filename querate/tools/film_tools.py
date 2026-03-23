import json
import os
from typing import Any

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
FILM_PATH = os.path.join(DATA_DIR, "film_library.json")

_CACHE: list[dict[str, Any]] | None = None


def _get_data() -> list[dict[str, Any]]:
    """Loads data once into memory, then serves from cache."""
    global _CACHE
    if _CACHE is None:
        try:
            with open(FILM_PATH, "r") as f:
                _CACHE = json.load(f)
        except FileNotFoundError:
            print(f"\n[Warning] {FILM_PATH} not found.")
            _CACHE = []
    return _CACHE


def _compute_taste_score(item: dict[str, Any]) -> float:
    """Composite taste score from ratings, likes, lists, rewatches, and watch time."""
    score = 0.0

    rating = item.get("letterboxd_rating")
    try:
        if rating is not None:
            score += float(rating)
    except (ValueError, TypeError):
        pass

    if item.get("liked"):
        score += 3.0

    for lst in item.get("custom_lists", []):
        list_score = 2.0
        rank = lst.get("rank")
        if rank is not None:
            if rank <= 10:
                list_score += 3.0
            elif rank <= 25:
                list_score += 2.0
            elif rank <= 50:
                list_score += 1.0
        score += list_score

    watch_history = item.get("netflix_watch_history", [])
    if len(watch_history) > 1:
        score += len(watch_history) * 1.5

    minutes = item.get("total_minutes_watched") or 0
    if minutes > 60:
        score += 1.0

    return score


def search_media_by_title(title: str) -> dict:
    """Searches the library for a specific movie or TV show by title.
    Returns full record including ratings, lists, and watch history.
    """
    data = _get_data()
    title_lower = title.lower()
    for item in data:
        if item.get("title", "").lower() == title_lower:
            return {"status": "success", "result": item}
    return {"status": "error", "message": f"Could not find '{title}' in the library."}


def get_highly_valued_media(media_type: str = "Movie", limit: int = 20) -> dict:
    """Returns the films or shows the user values most, based on a composite score
    combining ratings, liked status, list membership/rank, rewatches, and watch time.
    Use this to understand what the user considers their favorites.
    """
    data = _get_data()
    results = []

    for item in data:
        if media_type and item.get("type") != media_type:
            continue
        score = _compute_taste_score(item)
        if score > 0:
            results.append({
                "title": item.get("title"),
                "year": item.get("year"),
                "score": round(score, 2),
                "liked": item.get("liked"),
                "rating": item.get("letterboxd_rating"),
                "lists": [lst.get("name") for lst in item.get("custom_lists", [])],
                "rewatch_count": len(item.get("netflix_watch_history", [])),
                "minutes_watched": item.get("total_minutes_watched")
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return {"results": results[:limit]}


def get_items_on_custom_list(list_name: str, limit: int = 30) -> dict:
    """Retrieves all movies or shows on a specific named custom list, sorted by rank.
    Examples: 'Fav Films Of All Time', 'Gilded Child Research', 'Criterion'.
    """
    data = _get_data()
    results = []
    list_name_lower = list_name.lower()

    for item in data:
        for lst in item.get("custom_lists", []):
            if lst.get("name", "").lower() == list_name_lower:
                results.append({
                    "title": item.get("title"),
                    "year": item.get("year"),
                    "rank": lst.get("rank"),
                    "rating": item.get("letterboxd_rating"),
                    "liked": item.get("liked")
                })
                break

    results.sort(key=lambda x: (x["rank"] is None, x["rank"]))
    return {"results": results[:limit]}


def get_all_list_names() -> dict:
    """Returns all unique custom list names in the user's library.
    Call this first to know what lists exist before querying a specific one.
    """
    data = _get_data()
    names: set[str] = set()
    for item in data:
        for lst in item.get("custom_lists", []):
            name = lst.get("name")
            if name:
                names.add(name)
    return {"list_names": sorted(names)}


def get_most_watched(media_type: str = "Movie", limit: int = 20) -> dict:
    """Returns items the user has watched the most, based on total minutes watched
    and number of watch sessions. Strong implicit taste signal even without ratings.
    """
    data = _get_data()
    results = []

    for item in data:
        if media_type and item.get("type") != media_type:
            continue
        minutes = item.get("total_minutes_watched") or 0
        sessions = len(item.get("netflix_watch_history", []))
        if minutes > 0 or sessions > 0:
            results.append({
                "title": item.get("title"),
                "year": item.get("year"),
                "total_minutes_watched": minutes,
                "watch_sessions": sessions,
                "rating": item.get("letterboxd_rating"),
                "lists": [lst.get("name") for lst in item.get("custom_lists", [])]
            })

    results.sort(key=lambda x: x["total_minutes_watched"], reverse=True)
    return {"results": results[:limit]}


def get_recently_watched(limit: int = 20) -> dict:
    """Returns items the user watched most recently based on netflix_watch_history dates."""
    data = _get_data()
    results = []

    for item in data:
        history = item.get("netflix_watch_history", [])
        if history:
            recent_date = max(history)
            results.append({
                "title": item.get("title"),
                "year": item.get("year"),
                "last_watched": recent_date,
                "type": item.get("type"),
                "rating": item.get("letterboxd_rating"),
                "lists": [lst.get("name") for lst in item.get("custom_lists", [])]
            })

    results.sort(key=lambda x: x["last_watched"], reverse=True)
    return {"results": results[:limit]}


def get_films_by_era(start_year: int = 2000, end_year: int = 2024, limit: int = 20) -> dict:
    """Returns highly valued films from a specific era/decade.
    Useful for understanding if the user prefers classic vs contemporary cinema.
    """
    data = _get_data()
    results = []

    for item in data:
        year = item.get("year")
        if year is None:
            continue
        if start_year <= int(year) <= end_year:
            score = _compute_taste_score(item)
            if score > 0:
                results.append({
                    "title": item.get("title"),
                    "year": year,
                    "score": round(score, 2),
                    "rating": item.get("letterboxd_rating"),
                    "lists": [lst.get("name") for lst in item.get("custom_lists", [])]
                })

    results.sort(key=lambda x: x["score"], reverse=True)
    return {"results": results[:limit]}
