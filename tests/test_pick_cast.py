import unittest
from bots.utils.tests import make_bot


def assert_expected_output(t, bot):
  t.assertEqual(bot.state.selected_action, 'Pick')
  t.assertEqual(len(bot.state.casts), 1)
  t.assertEqual(len(bot.state.casts[0]['embeds']), 1)


class TestPickCast(unittest.TestCase):
    
  def test1(self):
    request = "Pick the most beautiful cast in arts category"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    self.assertEqual(bot.state.action_params['category'], 'c_arts')
    self.assertIn('beautiful', bot.state.action_params['criteria'])
            
  def test2(self):
    request = "Pick the funniest cast from /parenting channel"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    self.assertEqual(bot.state.action_params['channel'], 'chain://eip155:8453/erc721:0xb7310fc4b4a31c4fb7adf90b8201546bb2bcb52c')
    self.assertIn('fun', bot.state.action_params['criteria'])

  def test3(self):
    request = "Pick the most intriguing cast from @randombishop"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    self.assertEqual(bot.state.action_params['user_name'], 'randombishop')
    self.assertIn('intrig', bot.state.action_params['criteria'])
