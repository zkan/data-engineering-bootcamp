import asyncio
import os
import sys
from pathlib import Path

import streamlit as st
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


MODEL = "gemini-3.1-flash-lite"
SERVER_FILE = Path(__file__).with_name("bigquery_mcp.py")
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your Gemini API key


async def ask_gemini(prompt: str, history: list[types.Content]) -> tuple[str, list[types.Content]]:
    server = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_FILE)],
        env=None,
    )

    client = genai.Client(api_key=GEMINI_API_KEY)

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Convert MCP tool definitions into ordinary Gemini function tools.
            mcp_tools = await session.list_tools()
            declarations = [
                types.FunctionDeclaration(
                    name=tool.name,
                    description=tool.description,
                    parameters_json_schema=tool.input_schema,
                )
                for tool in mcp_tools.tools
            ]

            config = types.GenerateContentConfig(
                tools=[types.Tool(function_declarations=declarations)],
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                ),
            )

            contents = [
                *history,
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)],
                ),
            ]

            # Gemini may request the MCP tool, then use its result to write an answer.
            while True:
                response = await client.aio.models.generate_content(
                    model=MODEL,
                    contents=contents,
                    config=config,
                )

                function_calls = response.function_calls or []
                if not function_calls:
                    answer = response.text or "I couldn't generate a response."
                    contents.append(response.candidates[0].content)
                    return answer, contents

                contents.append(response.candidates[0].content)

                function_response_parts = []
                for call in function_calls:
                    result = await session.call_tool(call.name, call.args)

                    function_response_parts.append(
                        types.Part(
                            function_response=types.FunctionResponse(
                                name=call.name,
                                id=call.id,
                                response={
                                    "result": result.model_dump(mode="json")
                                },
                            )
                        )
                    )

                contents.append(
                    types.Content(role="tool", parts=function_response_parts)
                )


st.set_page_config(page_title="BigQuery Chat for Network Rail Movements", page_icon="📊")
st.title("📊 BigQuery Chat for Network Rail Movements")
st.caption("Gemini can query only the MCP server's permitted table.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about network rail movements (e.g., 'Show me the last 5 movements')"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Querying BigQuery..."):
            try:
                answer, updated_history = asyncio.run(
                    ask_gemini(prompt, st.session_state.history)
                )
                st.session_state.history = updated_history
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except BaseException as error:
                st.exception(error)
