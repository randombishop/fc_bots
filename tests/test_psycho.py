from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestPsycho(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.action, 'Psycho')
    self.assertEqual(len(state.casts), 3)
    self.assertTrue(state.reply)
    
  def test1(self):
    request = "Psycho analyze @randombishop"
    state = run_bot(test_id='TestPsycho:1', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.user_fid, 253232)
    self.assertEqual(state.user, 'randombishop')
    
  def test2(self):
    request = "psycho analyze me"
    fid_origin = 253232
    state = run_bot(test_id='TestPsycho:2', request=request, fid_origin=fid_origin)
    self.assert_expected_output(state)
    self.assertEqual(state.user_fid, fid_origin)
    self.assertEqual(state.user, 'randombishop')
    
  def test3(self):
    request = "Psycho analyze @aethernet"
    state = run_bot(test_id='TestPsycho:3', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.user_fid, 862185)
    self.assertEqual(state.user, 'aethernet')