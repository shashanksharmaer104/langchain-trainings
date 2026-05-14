"""
LangChain Agent Script
Converted from Jupyter Notebook — all errors resolved.
"""

# ─────────────────────────────────────────────
# 1. Env and LLM Initialisation
# ─────────────────────────────────────────────
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

import asyncio
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from playwright.async_api import async_playwright

load_dotenv('./../.env', override=True)

ollama_local_llm = ChatOllama(
    base_url="http://localhost:11434/",
    model="gemma4:latest",
    temperature=0.5,
    max_tokens=500,
    num_gpu=999,
)

# ─────────────────────────────────────────────
# 2. Tool Definitions
# ─────────────────────────────────────────────

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
search_tool = DuckDuckGoSearchRun()

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return int(a) + int(b)


@tool
def subtract_numbers(a: int, b: int) -> int:
    """Subtract two numbers and return the result."""
    return int(a) - int(b)


@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers and return the result."""
    return int(a) * int(b)

# FIX: Added search_tool to tools list (was imported but never used)
tools = [wikipedia, search_tool, add_numbers, subtract_numbers, multiply_numbers]
print("Tools registered:", [t.name for t in tools])

# ─────────────────────────────────────────────
# 5. Agent — Playwright Browser Toolkit
# FIX: create_async_playwright_browser() internally calls
#      run_until_complete(), which raises "event loop already running"
#      when we're already inside asyncio.run(). Solution: use
#      async_playwright() directly and await .start() ourselves.
# ─────────────────────────────────────────────


async def run_playwright_agent():
    # Launch browser manually so we fully control the async lifecycle
    pw = await async_playwright().start()
    async_browser = await pw.chromium.launch(headless=False)

    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
    browser_tools = toolkit.get_tools()
    print("\nPlaywright tools:", [t.name for t in browser_tools])

    tools_by_name = {t.name: t for t in browser_tools}
    navigate_tool = tools_by_name["navigate_browser"]
    get_element_tool = tools_by_name["get_elements"]

    # Navigate to the target page
    # await navigate_tool.arun({"url": "http://eaapp.somee.com/Employee/"})

    # Extract table cell text
    # cell_text = await get_element_tool.arun({
    #     "selector": "td",
    #     "action": "innerText",
    # })
    # print("Table cells:", cell_text)

    # Agent answering a question about the page
    browser_agent = create_react_agent(
        tools=browser_tools,
        model=ollama_local_llm,
        prompt="You are a helpful assistant that can answer questions using the available tools.",
    )

    pw_query = "What are the links in http://eaapp.somee.com/Employee/ page? Show me the results in list view or bullet points."
    pw_result = await browser_agent.ainvoke(
        {"messages": [HumanMessage(content=pw_query)]}
    )
    print("\n--- Playwright Agent Result ---")
    print(pw_result["messages"][-1].content)

    # Clean up: close browser and stop playwright
    await async_browser.close()
    await pw.stop()


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(run_playwright_agent())