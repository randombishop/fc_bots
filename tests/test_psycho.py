import unittest
from bots.utils.tests import make_bot


def assert_expected_output(t, bot):
  t.assertEqual(bot.state.selected_action, 'Psycho')
  t.assertEqual(len(bot.state.casts), 3)
  

class TestPsycho(unittest.TestCase):
  
  def test1(self):
    request = "Psycho analyze @randombishop"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    self.assertEqual(bot.state.action_params['fid'], 253232)
    self.assertEqual(bot.state.action_params['user_name'], 'randombishop')
    
  def test2(self):
    request = "psycho analyze me"
    fid_origin = 253232
    bot = make_bot()
    bot.respond(request, fid_origin=fid_origin)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    self.assertEqual(bot.state.action_params['fid'], fid_origin)
    self.assertEqual(bot.state.action_params['user_name'], 'randombishop')
    
  def test3(self):
    request = "Psycho analyze @aethernet"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    self.assertEqual(bot.state.action_params['fid'], 862185)
    self.assertEqual(bot.state.action_params['user_name'], 'aethernet')
