import asyncio
import os
from browser_use import ActionResult, Agent, Browser, Controller, BrowserConfig

from pydantic import SecretStr
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Controller, ActionResult
from langchain_core.tools import tool

# Initialize the controller
controller = Controller()

import asyncio

from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel
from datetime import datetime

api_key = os.getenv("GEMINI_API_KEY")

# Define the output format as a Pydantic model
class Flight(BaseModel):
    airline:str
    flight_id: str
    flight_url: str
    origin:str
    destination:str
    depart_time: datetime = None
    arrive_time: datetime = None
    price: float

class Flights(BaseModel):
	flights: List[Flight]




# Initialize the model
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))
browser = Browser()


# Initialize the model
userreq = "I want to book a flight"
task=f"""
you are a travel assistant browsing for a blind person.
If there is insufficient information to fill out the fields on the page for the desired action, halt and report what information is needed from the user. 
EX: the user must at least specify the flight origin and destination, and the depart and return dates. if one is missing please stop and ask them for the missing info.

The user request:
{userreq}
"""
controller = Controller()

@controller.action(
    'Save flight details which you found on page',
    param_model=Flights
)

async def save_flight(params: Flights, browser: Browser):
    print(f"Saving flight: {params.airline} from {params.origin}")

@controller.action(
    'Ask user for travel details',
    param_model=Flights
)
async def ask_details(params: Flights, browser: Browser):
    await browser.close()
    print(f"please give more info")

agent = Agent(
    llm=llm,
    browser=browser,
    controller=controller,
    controller=controller,
    use_vision=False,
    max_failures=2,
    max_actions_per_step=1,
)

async def main():
    history = await agent.run()
    result = history.final_result()
    if result:
        parsed: Flights = Flights.model_validate_json(result)

        for flight in parsed.flights:
            print('\n--------------------------------')
            print(f'airline:            {flight.airline}')
            print(f'URL:              {flight.flight_url}')
            print(f'travel:         {flight.origin} -> {flight.destination}')
            print(f'price: {flight.price}')
    else:
        print('No result')


res = asyncio.run(main())
print(res)