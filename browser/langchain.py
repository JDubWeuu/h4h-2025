from pydantic import SecretStr, BaseModel, Field
from datetime import datetime
from typing import List
import os
import langchain
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_groq import ChatGroq
from langchain_core.tools import tool
import browser
import asyncio


# Load environment variables
load_dotenv()

# LangChain configuration
langchain.verbose = False
langchain.debug = False
langchain.llm_cache = False

# Initialize ChatGroq
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=30,  # Set a timeout value
    max_retries=2,
)

from langchain_core.tools import StructuredTool




# Define browser_agent tool
@tool
async def browser_agent(query: str) -> str:
    """Get browser results based on the query."""
    if not query:
        raise ValueError("Query cannot be empty")
    print(f"[DEBUG] Invoking browser with query: {query}")
    res = await browser.run_browser(query)
    print(f"[DEBUG] Browser response: {res}")
    return res

browser_tool = StructuredTool.from_function(coroutine=browser_agent)
# ab = asyncio.run(browser_tool.ainvoke("book a flight from sfo to jfk"))
# # Bind tools to LLM
tools = [browser_tool]
interface_llm = llm.bind_tools(tools)

# User input and prompt
user_input = "I want to book a flight march 20 to 22nd from sfo to jfk"
prompt = f"""You are a travel assistant browsing for a blind person. If there is insufficient information to get the correct flight, ask for more info from the user.
When you have all the necessary information, use the `browser_agent` tool with the following format:
    {{
        "query": "search up flights from <origin> to <destination> on <depart_date> to <return_date>"
    }}
Example:
    human: "I want to book a flight"
    ai: "Great! Where would you like to fly and what are your depart and return dates?"
    human: "I want to leave March 20th to 22nd from SFO to JFK"
    ai: "Thank you for all the information, looking up flights now" **uses the browser_agent tool**

Now respond to the user's input: {user_input}"""

async def main():
    try:
        ai_msg = await interface_llm.ainvoke(prompt)
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")

# Run the main function

asyncio.run(main())


# langchain agent:
# interface_agent asks the user for info
# (enough info)? ask for the missing info : call the browser agent
# browser_agent returns Flights
# interface_agent asks the user for preferred flight
# browser agent steps through process




# from langchain.chat_models import init_chat_model

# llm = init_chat_model("gemini-2.0-flash-001", model_provider="google_vertexai")
# # tools = []
# # llm_with_tools = llm.bind_tools(tools)


