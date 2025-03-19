from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.v2.bot2 import Bot2
from langchain.agents import AgentExecutor
import json


class TestBot2(unittest.TestCase):
  
  def test1(self):
    input = {
      'bot_id': 788096,
      'request': 'Who is most active in channel /data'
    }
    bot = Bot2()
    executor = AgentExecutor(agent=bot, tools=bot._tools, llm=bot._llm)
    executor.invoke(input=json.dumps(input), config={"run_name": "test1"})
    
