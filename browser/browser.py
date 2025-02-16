import asyncio
import os
from browser_use import Agent, Browser, BrowserConfig
from playwright.async_api import BrowserContext
from pydantic import SecretStr

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Controller, ActionResult
from langchain_core.tools import tool

# Initialize the controller
controller = Controller()

import asyncio

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Initialize the model
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))
browser = Browser()
task="""
search google for 'SFO-JFK march 20th 10am',set the return date to march 22nd, ensure the dates are correct, press search, after loading the search, give me the prices for resulting flights"""

@controller.action('Ask user for information')
def ask_human(question: str) -> str:
    answer = input(f'\n{question}\nInput: ')
    return ActionResult(extracted_content=answer)
agent = Agent(
    llm=llm,
    browser=browser,
    controller=controller,
    use_vision=False,
    max_failures=2,
    max_actions_per_step=1,
)

async def main():
    print("hello, I am your travel agent")
    #introduce yourself as a travel agent
    await agent.run(task=task)
    input("Press Enter to close the browser...")
    await browser.close()

asyncio.run(main())