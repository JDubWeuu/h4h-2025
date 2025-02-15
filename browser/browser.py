import asyncio
import os
from langchain_ollama import ChatOllama
from browser_use import Agent, Browser, BrowserConfig
from pydantic import SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI


import asyncio

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Initialize the model
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))

browser = Browser()


# Initialize the model

task="""
search google for 'SFO-JFK march 20th 10am',set the return date to march 22nd, ensure the dates are correct, press search, after loading the search, give me the prices for resulting flights"""


agent = Agent(
    task=task,
    llm=llm,
    browser=browser,
    use_vision=False,
    max_failures=2,
    max_actions_per_step=1,
)

async def main():
    await agent.run()
    input("Press Enter to close the browser...")
    await browser.close()

asyncio.run(main())