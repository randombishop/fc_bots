from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestNews(unittest.TestCase):
  
  def assert_expected_output(self, state):
    self.assertEqual(state.get_selected_intent(), 'News')
    self.assertTrue(state.has_variable_value_with_type('News'))
    self.assertIsNotNone(state.casts)
    self.assertTrue(state.is_valid())
  
  def test1(self):
    request = "Search the news for Data Science"
    state = run_agent(test_id='TestNews:1', mode='bot', request=request)
    self.assert_expected_output(state)
    
