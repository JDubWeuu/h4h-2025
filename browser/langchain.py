from pydantic import SecretStr
from pydantic import BaseModel
from datetime import datetime
from typing import List

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

api_key = os.getenv("GEMINI_API_KEY")

interface_llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))
browser_llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))


agent = Agent(
    task="your task",
    llm=llm,
    planner_llm=planner_llm,           # Separate model for planning
    use_vision_for_planner=False,      # Disable vision for planner
    planner_interval=4                 # Plan every 4 steps
)

# langchain agent:
# interface_agent asks the user for info
# (enough info)? ask for the missing info : call the browser agent
# browser_agent returns Flights
# interface_agent asks the user for preferred flight
# browser agent steps through process