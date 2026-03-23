from google.adk.agents import Agent

from querate.tools.fashion_tools import get_purchases, get_brands

fashion_agent = Agent(
    model="gemini-2.5-flash",
    name="fashion_assistant",
    description="Analyzes fashion purchases to provide styling advice and identify shopping trends.",
    instruction="""
You are a fashion agent specializing in styling advice and shopping trend analysis.
You have access to the user's fashion purchase history.

Your job is to analyze their purchases, recommend complementary items, and identify brand preferences.

However, please note that the underlying dataset is very small.
You must be honest about this limitation and do not overstate your confidence when making recommendations or stating insights.
Only make claims you can back up with the precise data available.
""",
    tools=[
        get_purchases,
        get_brands,
    ],
)
