import unittest
from bots.utils.tests import make_bot

def assert_expected_output(t, bot, expected_continue):
  action = bot.state.selected_action
  cont = bot.state.action_params['continue'] if bot.state.action_params is not None else False
  if expected_continue:
    t.assertTrue(action == 'Chat')
    t.assertEqual(cont, expected_continue)
  else:
    t.assertTrue(action is None or action == 'Chat')
    t.assertEqual(cont, expected_continue)


class TestChat(unittest.TestCase):
  
  def test1(self):
    request = "Thank you!"
    fid_origin=253232
    bot = make_bot()
    bot.respond(request, fid_origin=fid_origin)
    bot.state.debug_action()
    assert_expected_output(self, bot, False)
    
  def test2(self):
    request = "Not interested."
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot, False)

  def test3(self):
    request = "Who are you?"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot, True)

  def test4(self):
    request = "Who are you?"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot, True)

  def test5(self):
    request = "Do you think DeepSeek will surpass OpenAI?"
    fid_origin=253232
    bot = make_bot()
    bot.respond(request, fid_origin=fid_origin)
    bot.state.debug_action()  
    assert_expected_output(self, bot, True)
