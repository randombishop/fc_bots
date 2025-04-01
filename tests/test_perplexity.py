from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestPerplexity(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertIn('ParsePerplexityQuestion', state.get_tools_sequence())
    self.assertIn('CallPerplexity', state.get_tools_sequence())
    self.assertIsNotNone(state.get('perplexity_answer'))
    self.assertIsNotNone(state.get('perplexity_link'))
    self.assertTrue(state.get('valid'))
    
  def test1(self):
    request = "Ask perplexity how many stars are there in our galaxy?"
    state = run_agent(test_id='TestPerplexity:1', mode='bot', request=request)
    self.assert_expected_output(state)
    
  def test2(self):
    request = "Ask perplexity what is the answer to life, the universe and everything?"
    state = run_agent(test_id='TestPerplexity:2', mode='bot', request=request)
    self.assert_expected_output(state)
