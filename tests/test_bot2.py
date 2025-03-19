from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.v2.bot2 import Bot2
from langchain.agents import AgentExecutor

class TestBot2(unittest.TestCase):
  
  def test1(self):
    bot = Bot2(id=788096)
    executor = AgentExecutor(agent=bot, tools=bot._tools, llm=bot._llm)
    executor.invoke(input="What is 15 * 4?", config={"run_name": "test1"})
    
