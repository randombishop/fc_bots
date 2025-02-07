from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import make_bot
from bots.prompts.autopilot import autopilot_prompt_template, autopilot_instructions, autopilot_schema
from bots.utils.llms import call_llm


class TestAutoprompt(unittest.TestCase):
  
  def test1(self):
    bot = make_bot()
    bot.initialize()
    bot.wakeup()
    instructions = bot.state.format(autopilot_instructions)
    prompt = bot.state.format(autopilot_prompt_template)
    print(instructions)
    print('-'*100)
    print(prompt)
    print('-'*100)
    print(autopilot_schema)
    result = call_llm(prompt, instructions, autopilot_schema)
    print('-'*100)
    print(result)
    