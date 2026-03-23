import asyncio
import os

from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from querate.agent import root_agent


async def main():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="querate",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="querate",
        user_id="user",
    )

    print("Querate — Cultural Intelligence Agent ready. Type 'quit' to exit.\n")

    while True:
        query = input("You: ").strip()
        if query.lower() in ("quit", "exit"):
            break
        if not query:
            continue

        print("\nAgent: ", end="", flush=True)

        async for event in runner.run_async(
            user_id="user",
            session_id=session.id,
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=query)],
            ),
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    print("".join(p.text for p in event.content.parts if p.text))

        print()


if __name__ == "__main__":
    asyncio.run(main())
