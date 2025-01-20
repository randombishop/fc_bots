import unittest
from bots.actions.perplexity import Perplexity
from bots.router import route


class TestPerplexity(unittest.TestCase):
  
  def test1(self):
    request = "Ask perplexity how many stars are there in our galaxy?"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, Perplexity)
