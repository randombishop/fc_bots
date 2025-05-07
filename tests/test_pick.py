from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestPickCast(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.plan['intent'], 'Pick')
    self.assertIsNotNone(state.casts[0]['embeds'])
              
  def test1(self):
    request = "Pick the funniest cast from /parenting channel"
    state = run_agent(test_id='TestPickCast:2', mode='bot', request=request)
    self.assert_expected_output(state)
    channel_id = state.get_variable_values('ChannelId')[-1]
    self.assertEqual(channel_id.channel, 'parenting')
    self.assertEqual(channel_id.channel_url, 'chain://eip155:8453/erc721:0xb7310fc4b4a31c4fb7adf90b8201546bb2bcb52c')

  def test3(self):
    request = "Pick the most intriguing cast from @randombishop"
    state = run_agent(test_id='TestPickCast:3', mode='bot', request=request)
    self.assert_expected_output(state)
    user_id = state.get_variable_values('UserId')[-1]
    self.assertEqual(user_id.fid, 253232)
    self.assertEqual(user_id.username, 'randombishop')
    
  def test4(self):
    request = "Pick the funniest cast in channnel /data?"
    state = run_agent(test_id='TestPickCast:4', mode='bot', request=request)
    self.assert_expected_output(state)
    channel_id = state.get_variable_values('ChannelId')[-1]
    self.assertEqual(channel_id.channel, 'data')
    self.assertEqual(channel_id.channel_url, 'https://farcaster.group/data')
