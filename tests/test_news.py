from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestNews(unittest.TestCase):
  
  def assert_expected_output(self, state):
    self.assertEqual(state.get('intent'), 'News')
    self.assertIn('ParseNewsSearch', state.get_tools_sequence())
    self.assertIn('GetNews', state.get_tools_sequence())
    self.assertIsNotNone(state.get('data_casts'))
    self.assertTrue(state.get('valid'))
  
  def test1(self):
    request = "Search the news for Data Science"
    state = run_agent(test_id='TestNews:1', mode='bot', request=request)
    self.assert_expected_output(state)
    
