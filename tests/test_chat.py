import unittest
from bots.utils.tests import make_bot


def assert_expected_output(t, bot, expected_continue):
  action = bot.state.selected_action
  should_continue = bot.state.should_continue
  if expected_continue:
    t.assertTrue(action == 'Chat' or action == 'Perplexity')
    t.assertTrue(should_continue)
  else:
    t.assertTrue(action is None or action == 'Chat')
    if action == 'Chat':
      t.assertFalse(should_continue)

class TestChat(unittest.TestCase):
    
  def test1(self):
    request = "Not interested."
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot, False)

  def test2(self):
    request = "Who are you?"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot, True)

  def test3(self):
    request = "How old are you?"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot, True)

  def test4(self):
    request = "Do you think DeepSeek will surpass OpenAI?"
    fid_origin=253232
    bot = make_bot()
    bot.respond(request, fid_origin=fid_origin)
    bot.state.debug_action()  
    assert_expected_output(self, bot, True)

  def test5(self):
    request = "Thank you so much for sharing 😺❤️❤️❤️"
    fid_origin=388401
    parent_hash='0x7506e607e722d543b61306d1357814ad61caa132'
    bot = make_bot()
    bot.respond(request, fid_origin=fid_origin, parent_hash=parent_hash)
    bot.state.debug_action()
    assert_expected_output(self, bot, False)