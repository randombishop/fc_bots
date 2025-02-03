import unittest
from bots.utils.tests import run_bot


class TestDigestCasts(unittest.TestCase):
  
  def assert_expected_output(self, bot):
    self.assertEqual(bot.state.selected_action, 'Summary')
    self.assertGreaterEqual(len(bot.state.casts), 1)
    self.assertTrue(bot.state.reply)
      
  def test1(self):
    request = "Give me a summary using keyword ethereum"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['keyword'], 'ethereum')
    
  def test2(self):
    request = "Summary for arts category"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['category'], 'c_arts')
    
  def test3(self):
    request = "Summary for /data channel?"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['channel'], 'https://farcaster.group/data')
    
  def test4(self):
    request = "Summary of posts about the beauty of canadian landscapes"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertIsNotNone(bot.state.action_params['search'])
      
  def test5(self):
    request = "Summary of @randombishop's posts"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['user_name'], 'randombishop')
