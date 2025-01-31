import unittest
from bots.utils.tests import make_bot



def assert_expected_output(t, bot):
  t.assertEqual(bot.state.selected_action, 'Perplexity')
  t.assertEqual(len(bot.state.casts), 1)
  t.assertEqual(len(bot.state.casts[0]['embeds']), 1)
  

class TestPerplexity(unittest.TestCase):
  
  def test1(self):
    request = "Ask perplexity how many stars are there in our galaxy?"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    
  def test2(self):
    request = "Ask perplexity what is the answer to life, the universe and everything?"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot)
