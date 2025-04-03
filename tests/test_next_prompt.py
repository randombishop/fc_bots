from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import bot_id
from bots.assistant.next_prompt import get_next_prompt


class TestNextPrompt(unittest.TestCase):
  
  def test1(self):
    next = get_next_prompt(bot_id)
    