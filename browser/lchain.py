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
async def find_flight_tool(query: str) -> str:
    """Get resulting flights based on the query."""
    if not query:
        raise ValueError("Query cannot be empty")
    
    print(f"[DEBUG] Running find_flight_tool with query: {query}")
    
    try:
        res = await run_browser(query)
        print(f"[DEBUG] Browser response: {res}")
        return res
    except Exception as e:
        print(f"[ERROR] Failed to run find_flight_tool: {e}")
        return "Error fetching results"

@tool
async def checkout_flight_tool(query: str) -> str:
    """checkout a flight based on the selected flight."""
    if not query:
        raise ValueError("Query cannot be empty")
    
    print(f"[DEBUG] Running checkout_flight_tool with query: {query}")
    
    try:
        res = await run_browser(query)
        print(f"[DEBUG] Browser response: {res}")
        return res
    except Exception as e:
        print(f"[ERROR] Failed to run checkout_flight_tool: {e}")
        return "Error fetching results"
# User input and prompt


async def get_flights(userinput):
    agent = initialize_agent(
        tools=[find_flight_tool],
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,  # or another agent type that supports function calls
        verbose=True,
    )
    prompt = f"""
    You are a travel assistant for a blind person and must use the `get_flights` to search for flights when flight information is incomplete or needs verification. 
    You should never provide a final answer without first calling the tool to fetch real-time flight data. 
    Example:
    User: "I want to book a flight from SFO to JFK on March 20th to 22nd."
    Assistant: (Calls `find_flight_tool` with: {{"query": "book flight from <origin> to <destination> on <depart_date> to <return_date>"}})
    
    Now respond to the user's input: {userinput}
    """
    # interface_llm = llm.bind_tools([browser_tool])
    # response = await interface_llm.ainvoke(prompt)
    response = await agent.arun({"input": prompt, "chat_history": []})

    print(response)
    prompt = f""" create a return message: 
    "I found the following flights from <origin> to <destination> for you, let me know which airline and price you would like: [list of <airline> <price>]
    create the concise list from the following:
    {response}

    """
    concise_output = llm.invoke(prompt)
    print(concise_output)
    return (concise_output, response)
    #ASK USER WHICH FLIGHT THEY WANT

async def checkout_flight(userinput,last_prompt):
    agent = initialize_agent(
        tools=[checkout_flight_tool],
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,  # or another agent type that supports function calls
        verbose=True,
    )
    prompt = f"""
    You are a travel assistant for a blind person and must use the `checkout_flight_tool` to book the flight our user is interested in. You already know what the user wants. Here are the links for the flights that suit the user's needs: 
    {last_prompt}
    Example:
    User: "I want the $200 flight on american airlines."
    Assistant: (Calls `checkout_flight_tool` with: {{"query": following the Book Flight phase: book the $<price> <Airline> flight at <URL> from {last_prompt}"}})
    
    
    Now run the checkout flights tool with the user's input: {userinput}
    """
    # interface_llm = llm.bind_tools([browser_tool])
    # response = await interface_llm.ainvoke(prompt)
    response = await agent.arun({"input": prompt, "chat_history": []})
    prompt = f""" create a return message based on the following: {response}
    Make sure the ending is the same, use the information above for the confirmation to assure them we are ready to book their flight.
    output format: "[confirmation(your flight info)] All that's left is your name, date of birth, credit card number, and billing address.

    """
    concise_output = llm.invoke(prompt)
    
    return concise_output

    

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


