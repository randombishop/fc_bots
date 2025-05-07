from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestFavoriteUsers(unittest.TestCase):

  def assert_expected_output(self, state, fid_target):
    self.assertEqual(state.plan['intent'], 'FavoriteUsers')
    self.assertEqual(len(state.get_variable_values('FavoriteUsers')), 1)
    self.assertEqual(len(state.get_variable_values('FavoriteUsersTable')), 1)
    self.assertEqual(state.get_variable_values('UserId')[0].fid, fid_target)
    self.assertTrue(state.valid)
    
  def test1(self):
    request = "Who are @vitalik.eth's favorite users?"
    state = run_agent(test_id='TestFavoriteUsers:1', mode='bot', request=request)
    self.assert_expected_output(state, 5650)
    
  def test2(self):
    request = "Who are @dwr.eth's favorite users?"
    state = run_agent(test_id='TestFavoriteUsers:2', mode='bot', request=request)
    self.assert_expected_output(state, 3)
    
  def test3(self):
    request = "Who are my favorite users?"
    fid_origin = 2
    state = run_agent(test_id='TestFavoriteUsers:3', mode='bot', request=request, fid_origin=fid_origin)
    self.assert_expected_output(state, fid_origin)
    
  def test4(self):
    request = "Who are this guy's favorite users?"
    fid_origin = 874939
    parent_hash = '0x86e946e7ffe837e0a27ae70f60826337028394d7'
    fid_target = 253232
    state = run_agent(test_id='TestFavoriteUsers:4', mode='bot', request=request, fid_origin=fid_origin, parent_hash=parent_hash)
    self.assert_expected_output(state, fid_target)

  