from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestNews(unittest.TestCase):
  
  def assert_expected_output(self, state):
    self.assertEqual(state.action, 'News')
    self.assertEqual(len(state.casts), 1)
    self.assertEqual(len(state.casts[0]['embeds']), 1)
    self.assertTrue(state.reply)
  
  def test1(self):
    request = "Search the news for Data Science"
    state = run_bot(test_id='TestNews:1', request=request)
    self.assert_expected_output(state)
    
