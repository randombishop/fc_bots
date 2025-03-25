from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestPraise(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.action, 'Praise')
    self.assertEqual(len(state.casts), 3)
    self.assertTrue(state.reply)
    
  def test1(self):
    request = "Praise @randombishop"
    state = run_bot(test_id='TestPraise:1', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.user_fid, 253232)
    self.assertEqual(state.user, 'randombishop')
    
  def test2(self):
    request = "Praise me"
    fid_origin = 2
    state = run_bot(test_id='TestPraise:2', request=request, fid_origin=fid_origin)
    self.assert_expected_output(state)
    self.assertEqual(state.user_fid, fid_origin)
    self.assertEqual(state.user, 'v')
    
  def test3(self):
    request = "Praise a random user"
    state = run_bot(test_id='TestPraise:3', request=request)
    self.assert_expected_output(state)
