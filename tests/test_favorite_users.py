import unittest
from bots.utils.tests import make_bot


def assert_expected_output(t, bot):
  t.assertEqual(bot.state.selected_action, 'FavoriteUsers')
  t.assertEqual(len(bot.state.casts), 1)
  t.assertEqual(len(bot.state.casts[0]['mentions']), 3)
  t.assertEqual(len(bot.state.casts[0]['embeds']), 1)
  

class TestFavoriteUsers(unittest.TestCase):
  
  def test1(self):
    request = "Who are @dwr.eth's favorite users?"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    self.assertEqual(bot.state.action_params['fid'], 3)
    
  def test2(self):
    request = "Who are my favorite users?"
    fid_origin = 2
    bot = make_bot()
    bot.respond(request, fid_origin=fid_origin)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    self.assertEqual(bot.state.action_params['fid'], fid_origin)
    
  def test3(self):
    request = "Who are this guy's favorite users?"
    fid_origin = 874939
    parent_hash = '0x86e946e7ffe837e0a27ae70f60826337028394d7'
    fid_target = 253232
    bot = make_bot()
    bot.respond(request, fid_origin=fid_origin, parent_hash=parent_hash)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    self.assertEqual(bot.state.action_params['fid'], fid_target)
