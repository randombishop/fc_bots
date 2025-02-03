import unittest
from bots.utils.tests import run_bot



  

class TestFavoriteUsers(unittest.TestCase):

  def assert_expected_output(self, bot):
    self.assertEqual(bot.state.selected_action, 'FavoriteUsers')
    self.assertEqual(len(bot.state.casts), 1)
    self.assertEqual(len(bot.state.casts[0]['mentions']), 3)
    self.assertEqual(len(bot.state.casts[0]['embeds']), 1)
    self.assertTrue(bot.state.reply)
    
  def test1(self):
    request = "Who are @vitalik.eth's favorite users?"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['fid'], 5650)
    
  def test2(self):
    request = "Who are @dwr.eth's favorite users?"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['fid'], 3)
    
  def test3(self):
    request = "Who are my favorite users?"
    fid_origin = 2
    bot = run_bot(request, fid_origin=fid_origin)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['fid'], fid_origin)
    
  def test4(self):
    request = "Who are this guy's favorite users?"
    fid_origin = 874939
    parent_hash = '0x86e946e7ffe837e0a27ae70f60826337028394d7'
    fid_target = 253232
    bot = run_bot(request, fid_origin=fid_origin, parent_hash=parent_hash)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['fid'], fid_target)

  