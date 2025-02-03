import unittest
from bots.utils.tests import run_bot


class TestMostActiveUsers(unittest.TestCase):

  def assert_expected_output(self, bot):
    self.assertEqual(bot.state.selected_action, 'MostActiveUsers')
    self.assertEqual(len(bot.state.casts), 1)
    self.assertEqual(len(bot.state.casts[0]['mentions']), 3)
    self.assertTrue(bot.state.reply)
      
  def test1(self):
    request = "Who is most active in channel /politics?"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['channel'], 'https://warpcast.com/~/channel/politics')
    
  def test2(self):
    request = "Who is most active here?"
    channel_url = 'https://farcaster.group/data'
    bot = run_bot(request, root_parent_url=channel_url)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['channel'], channel_url)
    
  def test3(self):
    request = "Who is most active in channel /mfers"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['channel'], 'https://warpcast.com/~/channel/mfers')
    self.assertIn('most active mfers', bot.state.casts[0]['text'])
