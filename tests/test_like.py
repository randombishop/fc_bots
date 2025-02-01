import unittest
from bots.utils.tests import make_bot


class TestLike(unittest.TestCase):
  
  def test1(self):
    request = "Thank you!"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assertTrue(bot.state.like)
    
  def test2(self):
    request = "Not interested."
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assertFalse(bot.state.like)
