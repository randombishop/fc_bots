from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestPsycho(unittest.TestCase):

  def assert_expected_output(self, state, fid, username):
    self.assertEqual(state.get_selected_intent(), 'Psycho')
    self.assertTrue(state.is_valid())
    user_id = state.get_last_variable_value_by_type('UserId')
    self.assertEqual(user_id.fid, fid)
    self.assertEqual(user_id.username, username)
    
  def test1(self):
    request = "Psycho analyze @randombishop"
    state = run_agent(test_id='TestPsycho:1', mode='bot', request=request)
    self.assert_expected_output(state, 253232, 'randombishop')
    
  def test2(self):
    request = "psycho analyze me"
    fid_origin = 253232
    state = run_agent(test_id='TestPsycho:2', mode='bot', request=request, fid_origin=fid_origin)
    self.assert_expected_output(state, fid_origin, 'randombishop')
    
  def test3(self):
    request = "Psycho analyze @aethernet"
    state = run_agent(test_id='TestPsycho:3', mode='bot', request=request)
    self.assert_expected_output(state, 862185, 'aethernet')
