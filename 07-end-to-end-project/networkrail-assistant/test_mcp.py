import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_FILE = Path(__file__).with_name("bigquery_mcp.py")


async def main():
    server = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_FILE)],
        env=None,
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Connected. Available tools:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            result = await session.call_tool("get_networkrail_movements", {"limit": 3})
            print("Result from get_networkrail_movements:")
            print(result.content)


asyncio.run(main())
