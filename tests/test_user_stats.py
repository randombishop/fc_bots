from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestUserStats(unittest.TestCase):
  
  def test1(self):
    request = "How many Brazilians do we have on Farcaster?"
    state = run_agent(test_id='TestUserStats:1', mode='bot', request=request)
    self.assertIn('GetUserStats', state.get_tools_sequence())
    
    
