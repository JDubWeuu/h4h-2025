import asyncio
import os
from datetime import datetime
from typing import List
from pydantic import BaseModel, SecretStr
from dotenv import load_dotenv
from browser_use import ActionResult, Agent, Browser, Controller, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI
import langchain

# LangChain configuration
langchain.verbose = False
langchain.debug = False
langchain.llm_cache = False

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

# Define the output format as a Pydantic model
class Flight(BaseModel):
    airline: str
    flight_id: str
    flight_url: str
    origin: str
    destination: str
    depart_time: datetime = None
    arrive_time: datetime = None
    price: float

class Flights(BaseModel):
    flights: List[Flight]

# Initialize the LLM and browser
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))
browser = Browser()
controller = Controller()

# Define the action for saving flight details
@controller.action(
    "Save flight details which you found on page",
    param_model=Flights
)
async def save_flight(params: Flights, browser: Browser):
    for flight in params.flights:
        print(f"Saving flight: {flight.airline} from {flight.origin} to {flight.destination}")

# Define the main function to run the browser agent
async def run_browser(user_request: str):
    task = f"""
    You are a travel assistant browsing for a blind person.
    If there is insufficient information to fill out the fields on the page for the desired action, halt and report what information is needed from the user.
    EX: The user must at least specify the flight origin, destination, and the depart and return dates. If one is missing, stop and ask them for the missing info.

    The user request:
    {user_request}
    """
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        controller=controller,
        use_vision=False,
        max_failures=2,
        max_actions_per_step=1,
    )

    # Run the agent and process the results
    history = await agent.run()
    result = history.final_result()
    if result:
        try:
            parsed: Flights = Flights.model_validate_json(result)
            for flight in parsed.flights:
                print("\n--------------------------------")
                print(f"Airline:       {flight.airline}")
                print(f"URL:           {flight.flight_url}")
                print(f"Travel:        {flight.origin} -> {flight.destination}")
                print(f"Price:         {flight.price}")
        except Exception as e:
            print(f"Error parsing flight data: {e}")
    else:
        print("No result found.")

# Example usage
if __name__ == "__main__":
    user_request = "I want to book a flight from SFO to JFK on March 20th to 22nd"
    asyncio.run(run_browser(user_request))