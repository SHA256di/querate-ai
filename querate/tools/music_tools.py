import os
import sqlite3

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
DB_PATH = os.path.join(DATA_DIR, "music.db")


def _get_db():
    return sqlite3.connect(DB_PATH)


def get_top_artists(limit: int = 20, metric: str = "total_ms") -> dict:
    """Returns the user's top artists ranked by a specific metric.
    Args:
        limit: number of artists to return
        metric: one of total_ms, total_plays, loyalty_score, skip_rate
    """
    conn = _get_db()
    rows = conn.execute(f"""
        SELECT artist, total_plays, total_hours, skip_rate, loyalty_score, years_active
        FROM artist_stats
        ORDER BY {metric} DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return {
        "artists": [
            {
                "artist": r[0],
                "total_plays": r[1],
                "total_hours": r[2],
                "skip_rate": r[3],
                "loyalty_score": r[4],
                "years_active": r[5]
            } for r in rows
        ]
    }


def get_artist_stats(artist: str) -> dict:
    """Returns full stats for a specific artist.
    Args:
        artist: artist name to look up
    """
    conn = _get_db()
    row = conn.execute("""
        SELECT artist, total_plays, total_hours, skip_rate,
               avg_ms_per_play, first_heard, last_heard,
               years_active, loyalty_score
        FROM artist_stats
        WHERE LOWER(artist) LIKE LOWER(?)
    """, (f"%{artist}%",)).fetchone()
    conn.close()
    if not row:
        return {"error": f"Artist '{artist}' not found"}
    return {
        "artist": row[0],
        "total_plays": row[1],
        "total_hours": row[2],
        "skip_rate": row[3],
        "avg_ms_per_play": row[4],
        "first_heard": row[5],
        "last_heard": row[6],
        "years_active": row[7],
        "loyalty_score": row[8]
    }


def get_loyalty_tiers() -> dict:
    """Returns artists bucketed into core, seasonal, and discovery tiers."""
    conn = _get_db()

    core = conn.execute("""
        SELECT artist, loyalty_score, total_hours, years_active
        FROM artist_stats
        WHERE loyalty_score >= 80
        ORDER BY loyalty_score DESC
        LIMIT 20
    """).fetchall()

    seasonal = conn.execute("""
        SELECT artist, loyalty_score, total_hours, years_active
        FROM artist_stats
        WHERE loyalty_score BETWEEN 50 AND 79
        ORDER BY loyalty_score DESC
        LIMIT 20
    """).fetchall()

    discoveries = conn.execute("""
        SELECT artist, loyalty_score, total_hours, years_active
        FROM artist_stats
        WHERE years_active <= 2
        ORDER BY total_hours DESC
        LIMIT 20
    """).fetchall()

    conn.close()

    def fmt(rows):
        return [{"artist": r[0], "loyalty_score": r[1],
                 "total_hours": r[2], "years_active": r[3]} for r in rows]

    return {
        "core": fmt(core),
        "seasonal": fmt(seasonal),
        "discoveries": fmt(discoveries)
    }


def get_late_night_artists(limit: int = 10) -> dict:
    """Returns artists most listened to between 10pm and 4am."""
    conn = _get_db()
    rows = conn.execute("""
        SELECT artist, SUM(total_ms) as night_ms, SUM(plays) as night_plays
        FROM hourly_profile
        WHERE hour >= 22 OR hour <= 4
        GROUP BY artist
        ORDER BY night_ms DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return {
        "late_night_artists": [
            {"artist": r[0], "night_ms": r[1], "night_plays": r[2]}
            for r in rows
        ]
    }


def get_taste_evolution() -> dict:
    """Returns top artist per year showing how taste has shifted over time."""
    conn = _get_db()
    rows = conn.execute("""
        SELECT year, artist, SUM(total_ms) as total_ms
        FROM monthly_taste
        GROUP BY year, artist
        HAVING total_ms = (
            SELECT MAX(t2.total_ms)
            FROM monthly_taste t2
            WHERE t2.year = monthly_taste.year
        )
        ORDER BY year
    """).fetchall()
    conn.close()
    return {
        "evolution": [
            {"year": r[0], "top_artist": r[1], "total_ms": r[2]}
            for r in rows
        ]
    }


def get_skip_hypocrisy(limit: int = 10) -> dict:
    """Returns artists with high plays but high skip rate —
    habit vs genuine taste tension."""
    conn = _get_db()
    rows = conn.execute("""
        SELECT artist, total_plays, total_hours, skip_rate, loyalty_score
        FROM artist_stats
        WHERE total_plays > 50
        AND skip_rate > 0.4
        ORDER BY total_plays DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return {
        "artists": [
            {
                "artist": r[0],
                "total_plays": r[1],
                "total_hours": r[2],
                "skip_rate": r[3],
                "loyalty_score": r[4]
            } for r in rows
        ]
    }
