from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestUserStats(unittest.TestCase):
  
  def test1(self):
    request = "How many Brazilians do we have on Farcaster?"
    state = run_agent(test_id='TestUserStats:1', mode='bot', request=request)
    self.assertIn('GetUserStats', state.get_tools_sequence())
    
  def test2(self):
    request = "What is the percentage of farcaster accounts who are active?"
    state = run_agent(test_id='TestUserStats:2', mode='bot', request=request)
    self.assertIn('GetUserStats', state.get_tools_sequence())
    
  def test3(self):
    request = """
    Come up with an interesting user aggregation statistic about farcaster users and share your insight
    """
    state = run_agent(test_id='TestUserStats:2', mode='assistant', request=request)
    self.assertIn('GetUserStats', state.get_tools_sequence())
