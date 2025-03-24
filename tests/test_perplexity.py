from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestPerplexity(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.action, 'Perplexity')
    self.assertEqual(len(state.casts), 1)
    self.assertEqual(len(state.casts[0]['embeds']), 1)  
    self.assertTrue(state.reply)
    
  def test1(self):
    request = "Ask perplexity how many stars are there in our galaxy?"
    state = run_bot(request)
    self.assert_expected_output(state)
    
  def test2(self):
    request = "Ask perplexity what is the answer to life, the universe and everything?"
    state = run_bot(request)
    self.assert_expected_output(state)
