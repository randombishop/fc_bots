from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestWhoIs(unittest.TestCase):
  
  def assert_expected_output(self, state):
    self.assertEqual(state.get('intent'), 'WhoIs')
    self.assertIn('GetUserProfile', state.get_tools_sequence())
    self.assertIn('CreateAvatar', state.get_tools_sequence())
    
  def test1(self):
    request = "Who is @randombishop?"
    state = run_agent(test_id='TestWhoIs:1', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('user_fid'), 253232)
    self.assertEqual(state.get('user'), 'randombishop')
    
  def test2(self):
    request = "Who am I?"
    fid_origin = 253232
    state = run_agent(test_id='TestWhoIs:2', mode='bot', request=request, fid_origin=fid_origin)
    self.assert_expected_output(state)
    self.assertEqual(state.get('user_fid'), fid_origin)
    self.assertEqual(state.get('user'), 'randombishop')

    
