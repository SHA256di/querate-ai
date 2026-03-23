# Querate

A cultural intelligence agent that synthesizes music, film, and fashion taste into unified aesthetic portraits.

## Architecture

Querate uses a multi-agent architecture built on [Google ADK](https://google.github.io/adk-docs/):

- **`curator_agent`** — Root agent. Synthesizes cross-domain taste signals. Delegates to sub-agents.
- **`music_agent`** — Analyzes Spotify listening history from a local SQLite database.
- **`fashion_agent`** — Analyzes fashion purchase history from a JSON dataset.
- **`film_agent`** — Analyzes Netflix and Letterboxd watch history from a JSON dataset.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with your API key:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

3. Ensure the data files exist at:
   - `../agents/music_agent/music.db`
   - `../agents/fashion-agent/data/fashion_clean.json`
   - `../agents/film_agent/data/film_library.json`

## Running

```bash
python main.py
```

Or via ADK web UI:
```bash
adk web
```

## Project Structure

```
querate/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── main.py
├── querate/
│   ├── __init__.py
│   ├── agent.py              # Root curator_agent
│   ├── sub_agents/
│   │   ├── __init__.py
│   │   ├── music_agent.py
│   │   ├── fashion_agent.py
│   │   └── film_agent.py
│   └── tools/
│       ├── __init__.py
│       ├── music_tools.py
│       ├── fashion_tools.py
│       └── film_tools.py
└── tests/
    └── test_curator.py
```
