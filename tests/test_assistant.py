from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_assistant


class TestAssistant(unittest.TestCase):
  
  def test1(self):
    instructions = "Post something about the most active users in a channel."
    state = run_assistant(test_id='TestAssistant:1', instructions=instructions)
