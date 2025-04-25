from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestCastStats(unittest.TestCase):
  
  def test1(self):
    request = "Compare casts statistics between high follower accounts vs low ones on Farcaster"
    state = run_agent(test_id='TestCastStats:1', mode='bot', request=request)
    self.assertIn('GetCastStats', state.get_tools_sequence())
    
  