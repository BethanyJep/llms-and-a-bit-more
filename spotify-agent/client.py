import asyncio

from agent_framework import Agent

from src.agent import create_agent


async def main():
    agent: Agent = create_agent()

    print("🎵 Spotify Agent (type 'quit' to exit)")
    print("-" * 40)

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input or user_input.lower() in ("quit", "exit"):
            print("Goodbye! 🎶")
            break

        result = await agent.run(user_input)
        print(f"\nAgent: {result}")


if __name__ == "__main__":
    asyncio.run(main())
