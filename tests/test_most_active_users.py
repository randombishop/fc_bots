from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestMostActiveUsers(unittest.TestCase):

  def assert_expected_output(self, state, channel, channel_url):
    self.assertEqual(state.get_selected_intent(), 'MostActiveUsers')
    self.assertTrue(state.has_variable_value_with_type('MostActiveUsers'))
    self.assertTrue(state.has_variable_value_with_type('MostActiveUsersChart'))
    self.assertEqual(state.get_last_variable_value_by_type('ChannelId').channel, channel)
    self.assertEqual(state.get_last_variable_value_by_type('ChannelId').channel_url, channel_url)
    self.assertIsNotNone(state.casts)
    self.assertTrue(len(state.casts[0]['mentions']) > 0)
    self.assertTrue(state.is_valid())
      
  def test1(self):
    request = "Who is most active in channel /politics?"
    state = run_agent(test_id='TestMostActiveUsers:1', mode='bot', request=request)
    self.assert_expected_output(state, 'politics', 'https://warpcast.com/~/channel/politics')
    
  def test2(self):
    request = "Who is most active here? Mention at least 1 top contributor."
    channel_url = 'https://farcaster.group/data'
    state = run_agent(test_id='TestMostActiveUsers:2', mode='bot', request=request, root_parent_url=channel_url)
    self.assert_expected_output(state, 'data', channel_url)
    
  def test3(self):
    request = "Who is most active in channel /mfers? Include an activity chart."
    state = run_agent(test_id='TestMostActiveUsers:3', mode='bot', request=request)
    self.assert_expected_output(state, 'mfers', 'https://warpcast.com/~/channel/mfers')
