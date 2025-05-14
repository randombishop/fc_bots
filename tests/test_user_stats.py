from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestUserStats(unittest.TestCase):
  
  def assert_expected_output(self, state):
    self.assertTrue(state.has_variable_value_with_type('DuneQuery'))
    self.assertTrue(state.has_variable_value_with_type('DataFrame'))
    self.assertTrue(state.is_valid())
    
  def test1(self):
    request = "How many Brazilians do we have on Farcaster?"
    state = run_agent(test_id='TestUserStats:1', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get_selected_intent(), 'UserStats')
    
  def test2(self):
    request = "What is the percentage of farcaster accounts who are active?"
    state = run_agent(test_id='TestUserStats:2', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get_selected_intent(), 'UserStats')
    
  def test3(self):
    request = """
    Come up with an interesting user aggregation statistic about farcaster users and share your insight
    """
    state = run_agent(test_id='TestUserStats:3', mode='assistant', request=request)
    self.assert_expected_output(state)
