import unittest
from bots.utils.tests import run_bot


class TestLike(unittest.TestCase):
  
  def test1(self):
    request = "Thank you!"
    bot = run_bot(request)
    self.assertTrue(bot.state.like)
    self.assertFalse(bot.state.reply)
    
  def test2(self):
    request = "Not interested."
    bot = run_bot(request)
    self.assertFalse(bot.state.like)
    self.assertFalse(bot.state.reply)