from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestPraise(unittest.TestCase):

  def assert_expected_output(self, state, fid, username):
    self.assertEqual(state.get_selected_intent(), 'Praise')
    self.assertTrue(state.is_valid())
    user_id = state.get_last_variable_value_by_type('UserId')
    if fid is not None:
      self.assertEqual(user_id.fid, fid)
      self.assertEqual(user_id.username, username)
    else:
      self.assertIsNotNone(user_id)
    
  def test1(self):
    request = "Praise @randombishop"
    state = run_agent(test_id='TestPraise:1', mode='bot', request=request)
    self.assert_expected_output(state, 253232, 'randombishop')
    
  def test2(self):
    request = "Praise me"
    fid_origin = 253232
    state = run_agent(test_id='TestPraise:2', mode='bot', request=request, fid_origin=fid_origin)
    self.assert_expected_output(state, fid_origin, 'randombishop')
    
  def test3(self):
    request = "Praise a random user in channel /mfers"
    state = run_agent(test_id='TestPraise:3', mode='bot', request=request)
    self.assert_expected_output(state, None, None)
