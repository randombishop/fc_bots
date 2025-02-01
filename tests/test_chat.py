import unittest
from bots.utils.tests import make_bot


def assert_expected_output(t, bot, expected_continue):
  action = bot.state.selected_action
  if expected_continue:
    t.assertTrue(action == 'Chat')
    t.assertEqual(len(bot.state.casts), 1)
  else:
    t.assertTrue(action is None or action == 'Chat')
    t.assertEqual(len(bot.state.casts), 0)


class TestChat(unittest.TestCase):
    
  def test1(self):
    request = "Not interested."
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot, False)

  def test2(self):
    request = "Chat with me: Who are you?"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot, True)

  def test3(self):
    request = "Chat with me: Do you think DeepSeek will surpass OpenAI?"
    fid_origin=253232
    bot = make_bot()
    bot.respond(request, fid_origin=fid_origin)
    bot.state.debug_action()  
    assert_expected_output(self, bot, True)

  def test4(self):
    request = "Thank you so much for sharing 😺❤️❤️❤️"
    fid_origin=388401
    parent_hash='0x7506e607e722d543b61306d1357814ad61caa132'
    bot = make_bot()
    bot.respond(request, fid_origin=fid_origin, parent_hash=parent_hash)
    bot.state.debug_action()
    assert_expected_output(self, bot, False)