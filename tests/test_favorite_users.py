from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestFavoriteUsers(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.selected_action, 'FavoriteUsers')
    self.assertEqual(len(state.casts), 1)
    self.assertEqual(len(state.casts[0]['mentions']), 3)
    self.assertEqual(len(state.casts[0]['embeds']), 1)
    self.assertTrue(state.reply)
    
  def test1(self):
    request = "Who are @vitalik.eth's favorite users?"
    state = run_bot(request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['fid'], 5650)
    
  def test2(self):
    request = "Who are @dwr.eth's favorite users?"
    state = run_bot(request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['fid'], 3)
    
  def test3(self):
    request = "Who are my favorite users?"
    fid_origin = 2
    state = run_bot(request, fid_origin=fid_origin)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['fid'], fid_origin)
    
  def test4(self):
    request = "Who are this guy's favorite users?"
    fid_origin = 874939
    parent_hash = '0x86e946e7ffe837e0a27ae70f60826337028394d7'
    fid_target = 253232
    state = run_bot(request, fid_origin=fid_origin, parent_hash=parent_hash)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['fid'], fid_target)

  