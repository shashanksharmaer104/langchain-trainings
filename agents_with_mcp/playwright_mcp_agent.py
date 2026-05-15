import asyncio
import itertools
import sys
import traceback

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient


# Spinner animation
async def thinking_animation():

    for frame in itertools.cycle(
        ["Thinking   ", "Thinking.  ", "Thinking.. ", "Thinking..."]
    ):
        sys.stdout.write(f"\r{frame}")
        sys.stdout.flush()
        await asyncio.sleep(0.4)


async def main():

    spinner_task = None

    try:

        client = MultiServerMCPClient(
            {
                "playwright": {
            "command": "npx",
            "args": [
                "@playwright/mcp@latest",
                "--browser", "chrome"
            ],
            "transport": "stdio",
            "env": {
                "PLAYWRIGHT_LAUNCH_OPTIONS": '{"args": ["--no-sandbox", "--disable-setuid-sandbox"]}'
            }
                }
            }
        )

        print("Loading MCP tools...")

        tools = await client.get_tools()

        print(f"Loaded tools: {len(tools)}")

        llm = ChatOllama(
            model="qwen3.5:9b",
            base_url="http://localhost:11434",
            temperature=0,
            reasoning=True
        )

        agent = create_agent(
            model=llm,
            tools=tools,
        )

        # Start animation
        spinner_task = asyncio.create_task(thinking_animation())

        # Agent execution
        response = await agent.ainvoke(
            {
                "messages": [
                    (
                        "user",
                        """
                            Do this:
                            1. Go to https://www.google.com/
                            2. Search for "AI for Playwright tool" and press "Enter"
                            3. Get the top 5 results from the search, including:
                                - Title
                                - URL
                                - Short description (1-2 sentences)

                            Return JSON only.
                        """,
                    )
                ]
            }
        )

        # Stop animation
        spinner_task.cancel()

        # Clear line
        sys.stdout.write("\r" + " " * 30 + "\r")

        print("\n-----------------FINAL RESPONSE:---------------------\n")
        print(response)

    except Exception:

        if spinner_task:
            spinner_task.cancel()

        sys.stdout.write("\r" + " " * 30 + "\r")

        print("\nERROR OCCURRED:\n")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())