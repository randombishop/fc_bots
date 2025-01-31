import unittest
from bots.utils.tests import make_bot


def assert_expected_output(t, bot):
  t.assertEqual(bot.state.selected_action, 'News')
  t.assertEqual(len(bot.state.casts), 1)
  t.assertEqual(len(bot.state.casts[0]['embeds']), 1)
  

class TestNews(unittest.TestCase):
  
  def test1(self):
    request = "Search the news for Data Science"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    
