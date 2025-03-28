from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestMostActiveUsers(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertIn('GetMostActiveUsers', state.get_tools_sequence())
    self.assertEqual(len(state.get('data_casts')), 1)
    self.assertTrue(state.get('valid'))
      
  def test1(self):
    request = "Who is most active in channel /politics?"
    state = run_bot(test_id='TestMostActiveUsers:1', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('channel'), 'politics')
    self.assertEqual(state.get('channel_url'), 'https://warpcast.com/~/channel/politics')
    
  def test2(self):
    request = "Who is most active here? Mention at least 1 top contributor."
    channel_url = 'https://farcaster.group/data'
    state = run_bot(test_id='TestMostActiveUsers:2', request=request, root_parent_url=channel_url)
    self.assert_expected_output(state)
    self.assertEqual(state.get('channel'), 'data')
    self.assertEqual(state.get('channel_url'), channel_url)
    self.assertTrue(len(state.get('data_casts')[0]['mentions']) > 0)
    
  def test3(self):
    request = "Who is most active in channel /mfers? Include an activity chart."
    state = run_bot(test_id='TestMostActiveUsers:3', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('channel'), 'mfers')
    self.assertEqual(state.get('channel_url'), 'https://warpcast.com/~/channel/mfers')
    self.assertIn('PrepareMostActiveUsersChart', state.get_tools_sequence())