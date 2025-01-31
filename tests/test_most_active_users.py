import unittest
from bots.utils.tests import make_bot


def assert_expected_output(t, bot):
  t.assertEqual(bot.state.selected_action, 'MostActiveUsers')
  t.assertEqual(len(bot.state.casts), 1)
  t.assertEqual(len(bot.state.casts[0]['mentions']), 3)
   

class TestMostActiveUsers(unittest.TestCase):
  
  def test1(self):
    request = "Who is most active in channel /politics?"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    self.assertEqual(bot.state.action_params['channel'], 'https://warpcast.com/~/channel/politics')
    
  def test2(self):
    request = "Who is most active here?"
    channel_url = 'https://farcaster.group/data'
    bot = make_bot()
    bot.respond(request, root_parent_url=channel_url)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    self.assertEqual(bot.state.action_params['channel'], channel_url)
