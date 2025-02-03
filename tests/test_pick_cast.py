import unittest
from bots.utils.tests import run_bot


class TestPickCast(unittest.TestCase):

  def assert_expected_output(self, bot):
    self.assertEqual(bot.state.selected_action, 'Pick')
    self.assertEqual(len(bot.state.casts), 1)
    self.assertEqual(len(bot.state.casts[0]['embeds']), 1)
    self.assertTrue(bot.state.reply)
    
  def test1(self):
    request = "Pick the most beautiful cast in arts category"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['category'], 'c_arts')
    self.assertIn('beautiful', bot.state.action_params['criteria'])
            
  def test2(self):
    request = "Pick the funniest cast from /parenting channel"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['channel'], 'chain://eip155:8453/erc721:0xb7310fc4b4a31c4fb7adf90b8201546bb2bcb52c')
    self.assertIn('fun', bot.state.action_params['criteria'])

  def test3(self):
    request = "Pick the most intriguing cast from @randombishop"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['user_name'], 'randombishop')
    self.assertIn('intrig', bot.state.action_params['criteria'])
    
  def test4(self):
    request = "Pick the funniest cast in channnel /data?"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['channel'], 'https://farcaster.group/data')
    self.assertIn('fun', bot.state.action_params['criteria'])