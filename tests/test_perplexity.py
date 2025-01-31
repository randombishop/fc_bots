import unittest
from bots.action.perplexity import Perplexity
from bots.router import route


class TestPerplexity(unittest.TestCase):
  
  def test1(self):
    request = "Ask perplexity how many stars are there in our galaxy?"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, Perplexity)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)
    
  def test2(self):
    request = "Ask perplexity what is the answer to life, the universe and everything?"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, Perplexity)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)
