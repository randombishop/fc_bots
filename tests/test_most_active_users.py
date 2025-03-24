from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestMostActiveUsers(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.action, 'MostActiveUsers')
    self.assertEqual(len(state.casts), 1)
    self.assertEqual(len(state.casts[0]['mentions']), 3)
    self.assertTrue(state.reply)
      
  def test1(self):
    request = "Who is most active in channel /politics?"
    state = run_bot(request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['channel'], 'https://warpcast.com/~/channel/politics')
    
  def test2(self):
    request = "Who is most active here?"
    channel_url = 'https://farcaster.group/data'
    state = run_bot(request, root_parent_url=channel_url)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['channel'], channel_url)
    
  def test3(self):
    request = "Who is most active in channel /mfers"
    state = run_bot(request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['channel'], 'https://warpcast.com/~/channel/mfers')
    self.assertIn('most active mfers', state.casts[0]['text'])
