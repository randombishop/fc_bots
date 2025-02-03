import unittest
from bots.utils.tests import run_bot


class TestNews(unittest.TestCase):
  
  def assert_expected_output(self, bot):
    self.assertEqual(bot.state.selected_action, 'News')
    self.assertEqual(len(bot.state.casts), 1)
    self.assertEqual(len(bot.state.casts[0]['embeds']), 1)
    self.assertTrue(bot.state.reply)
  
  def test1(self):
    request = "Search the news for Data Science"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    
