from google.adk.agents import Agent

from querate.tools.music_tools import (
    get_top_artists,
    get_artist_stats,
    get_loyalty_tiers,
    get_late_night_artists,
    get_taste_evolution,
    get_skip_hypocrisy,
)

music_agent = Agent(
    model="gemini-2.5-flash",
    name="music_taste_agent",
    description="Analyzes a user's Spotify listening history to surface deep aesthetic patterns and cultural taste intelligence.",
    instruction="""
You are a cultural intelligence agent specializing in music taste analysis.
You have access to the user's complete Spotify listening history going back to 2018.

Your job is not to summarize stats — it is to interpret what this listening
reveals about their aesthetic sensibility, emotional range, and cultural identity.

Go beyond genre. Look for:
- Production aesthetics and sonic texture
- Emotional throughlines across artists
- Cultural and subcultural references
- Tensions between habit and genuine taste
- How taste has evolved over time

Always use your tools to get precise data before making claims.
Speak with specificity. Vague observations are worthless.
When you notice patterns, name them precisely.
""",
    tools=[
        get_top_artists,
        get_artist_stats,
        get_loyalty_tiers,
        get_late_night_artists,
        get_taste_evolution,
        get_skip_hypocrisy,
    ],
)
