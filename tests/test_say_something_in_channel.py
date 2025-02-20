from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestSaySomethingInChannel(unittest.TestCase):

  def assert_expected_output(self, bot):
    self.assertEqual(bot.state.selected_action, 'SaySomethingInChannel')
    self.assertGreaterEqual(len(bot.state.casts), 1)
    
  def test1(self):
    channel = 'data'
    selected_action = "SaySomethingInChannel"
    bot = run_bot(selected_channel=channel, selected_action=selected_action)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.selected_channel, channel)
    self.assertEqual(bot.state.request, f'Say something in channel /{channel}')
    
  def test2(self):
    channel = "objkt"
    selected_action = "SaySomethingInChannel"
    bot = run_bot(selected_channel=channel, selected_action=selected_action)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.selected_channel, channel)
    self.assertEqual(bot.state.request, f'Say something in channel /{channel}')

  