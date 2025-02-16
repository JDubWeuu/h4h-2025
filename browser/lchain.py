from pydantic import SecretStr, BaseModel, Field
from datetime import datetime
from typing import List
import os
import langchain
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from .bser import run_browser
from langchain_core.tools import StructuredTool, Tool, tool
from langchain.agents.agent_types import AgentType
from langchain.agents import initialize_agent
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




# Define browser_agent tool
@tool
async def browser_tool(query: str) -> str:
    """Get browser results based on the query."""
    if not query:
        raise ValueError("Query cannot be empty")
    
    print(f"[DEBUG] Running browser_agent with query: {query}")
    
    try:
        res = await run_browser(query)
        print(f"[DEBUG] Browser response: {res}")
        return res
    except Exception as e:
        print(f"[ERROR] Failed to run browser agent: {e}")
        return "Error fetching results"

# User input and prompt


async def runprompt(userinput):
    agent = initialize_agent(
        tools=[browser_tool],
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,  # or another agent type that supports function calls
        verbose=True,
    )
    prompt = f"""
    You are a travel assistant for a blind person and must use the `browser_tool` to search for flights when flight information is incomplete or needs verification. 
    You should never provide a final answer without first calling the tool to fetch real-time flight data. For example:

    Example:
    User: "I want to book a flight from SFO to JFK on March 20th to 22nd."
    Assistant: (Calls `browser_tool` with: {{"query": "search up flights from SFO to JFK on March 20th to 22nd"}})

    Now respond to the user's input: {userinput}
    """
    # interface_llm = llm.bind_tools([browser_tool])
    # response = await interface_llm.ainvoke(prompt)
    response = await agent.arun({"input": prompt, "chat_history": []})
    print(response)
    return response

# Run the main function




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


