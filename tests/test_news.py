from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestNews(unittest.TestCase):
  
  def assert_expected_output(self, state):
    self.assertEqual(state.plan['intent'], 'News')
    self.assertEqual(len(state.get_variable_values('News')), 1)
    self.assertIsNotNone(state.casts)
    self.assertTrue(state.valid)
  
  def test1(self):
    request = "Search the news for Data Science"
    state = run_agent(test_id='TestNews:1', mode='bot', request=request)
    self.assert_expected_output(state)
    
