from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestSaySomethingInChannel(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.action, 'SaySomethingInChannel')
    self.assertGreaterEqual(len(state.casts), 1)
    
  def test1(self):
    channel = 'data'
    action = "SaySomethingInChannel"
    state = run_bot(selected_channel=channel, action=action)
    self.assert_expected_output(state)
    self.assertEqual(state.selected_channel, channel)
    self.assertEqual(state.request, f'Say something in channel /{channel}')
    
  def test2(self):
    channel = "objkt"
    action = "SaySomethingInChannel"
    state = run_bot(selected_channel=channel, action=action)
    self.assert_expected_output(state)
    self.assertEqual(state.selected_channel, channel)
    self.assertEqual(state.request, f'Say something in channel /{channel}')

  