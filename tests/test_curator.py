"""
Smoke tests for the querate curator agent.
"""

import pytest
from unittest.mock import patch, MagicMock


def test_root_agent_exists():
    from querate.agent import root_agent
    assert root_agent is not None
    assert root_agent.name == "curator_agent"


def test_root_agent_has_sub_agents():
    from querate.agent import root_agent
    assert len(root_agent.sub_agents) == 3
    sub_agent_names = {a.name for a in root_agent.sub_agents}
    assert "music_taste_agent" in sub_agent_names
    assert "fashion_assistant" in sub_agent_names
    assert "Film_Taste_Specialist" in sub_agent_names


def test_root_agent_has_no_direct_tools():
    from querate.agent import root_agent
    assert not root_agent.tools


def test_music_agent_tools():
    from querate.sub_agents.music_agent import music_agent
    assert len(music_agent.tools) == 6


def test_fashion_agent_tools():
    from querate.sub_agents.fashion_agent import fashion_agent
    assert len(fashion_agent.tools) == 2


def test_film_agent_tools():
    from querate.sub_agents.film_agent import film_agent
    assert len(film_agent.tools) == 7


@patch("querate.tools.music_tools.sqlite3.connect")
def test_get_top_artists_returns_dict(mock_connect):
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchall.return_value = [
        ("Radiohead", 500, 120.5, 0.1, 95.0, 5)
    ]
    mock_connect.return_value = mock_conn
    from querate.tools.music_tools import get_top_artists
    result = get_top_artists(limit=1)
    assert isinstance(result, dict)
    assert "artists" in result


@patch("querate.tools.fashion_tools.open")
@patch("querate.tools.fashion_tools.json.load")
def test_get_purchases_returns_dict(mock_load, mock_open):
    mock_load.return_value = [{"brand": "Acne Studios", "title": "Scarf"}]
    mock_open.return_value.__enter__ = lambda s: s
    mock_open.return_value.__exit__ = MagicMock(return_value=False)
    from querate.tools.fashion_tools import get_purchases
    result = get_purchases()
    assert isinstance(result, dict)
    assert "purchases" in result


def test_film_tool_returns_dict_on_missing_file():
    import querate.tools.film_tools as ft
    ft._CACHE = None
    original = ft.DATA_FILE
    ft.DATA_FILE = "/nonexistent/path/film_library.json"
    result = ft.get_highly_valued_media()
    assert isinstance(result, dict)
    ft.DATA_FILE = original
    ft._CACHE = None
