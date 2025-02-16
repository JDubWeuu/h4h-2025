import asyncio
import os
from datetime import datetime
from typing import List
from pydantic import BaseModel, SecretStr
from dotenv import load_dotenv
from browser_use import ActionResult, Agent, Browser, Controller, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI
import langchain
from langchain_openai import ChatOpenAI

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
# llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))
# llm=ChatOllama(model="llama3.2:latest", num_ctx=32000)
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0,
)

browser = Browser()
controller = Controller()

# Define the action for saving flight details
# @controller.action(
#     "Save flight details which you found on page",
#     param_model=Flights
# )
# async def save_flight(params: Flights, browser: Browser):
#     for flight in params.flights:
#         print(f"Saving flight: {flight.airline} from {flight.origin} to {flight.destination}")

# Define the main function to run the browser agent
async def run_browser(user_request: str):
    task = f"""
    You are a travel assistant browsing for a blind person.
    based on information from the user, depending on the current phase of the booking processing follow the appropriate procedures.

    following the user's request, use only one set of the phase instructions to fulfill their request. If the user request contains a URL, you will know to run the second phase: Book Flight phase
    The user request:
    {user_request}

    ## Searching for flight phase:
    1. go to https://www.kayak.com
    2. select the flights tab
    3. fill out from left to right: search and select destinations (ensure it is selected from the dropdown. you will know it is selected when there is a remove button)
    4. select the dates on the calendar and submit
    5. select 1 adult if the user did not specify other travellers
    6. press the search icon and wait for responses
    7. use the save_flights tool to save flight price information
    8. tell the user the best flights (include the URLs for the flights as well)
    Example output for Searching for flight phase:
    "Here are some of the best flight options from SFO to JFK on March 20th to 22nd:
        1. **American Airlines**
        - **Flight ID**: AA123
        - **Departure**: March 20th, 7:27 AM
        - **Arrival**: March 20th, 4:01 PM
        - **Price**: $297
        - [View Deal](https://www.kayak.com/flights/SFO-JFK/2025-03-20/2025-03-22?flight=AA123)

        2. **Alaska Airlines**
        - **Flight ID**: AS456
        - **Departure**: March 20th, 1:45 PM
        - **Arrival**: March 20th, 10:29 PM
        - **Price**: $277
        - [View Deal](https://www.kayak.com/flights/SFO-JFK/2025-03-20/2025-03-22?flight=AS456)

        3. **JetBlue**
        - **Flight ID**: B678
        - **Departure**: March 20th, 4:40 PM
        - **Arrival**: March 21st, 12:57 AM
        - **Price**: $277
        - [View Deal](https://www.kayak.com/flights/SFO-JFK/2025-03-20/2025-03-22?flight=B678)

        Please review these options and let me know if you would like to proceed with booking any of these flight"

    ## Book Flight phase:
    1. go to the URL of the user's preferred flight
    2. wait for the page to load and then scroll until you find a flight that matches the specified airline and price
    3. click the 'view detail' button
    4. select the 'accept restrictions'
    5. go to checkout
    6. last step is to get to the contact info screen, do not fill it in

    **Important:** Ensure efficiency and accuracy throughout the process.

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
    # if result:
    #     try:
    #         parsed: Flights = Flights.model_validate_json(result)
    #         for flight in parsed.flights:
    #             print("\n--------------------------------")
    #             print(f"Airline:       {flight.airline}")
    #             print(f"URL:           {flight.flight_url}")
    #             print(f"Travel:        {flight.origin} -> {flight.destination}")
    #             print(f"Price:         {flight.price}")
    #     except Exception as e:
    #         print(f"Error parsing flight data: {e}")
    # else:
    #     print("No result found.")
    return result

# Example usage
if __name__ == "__main__":
    user_request = "I want to book a flight from SFO to JFK on March 20th to 22nd"
    asyncio.run(run_browser(user_request))