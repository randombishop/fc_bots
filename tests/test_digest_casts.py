import unittest
from bots.utils.tests import make_bot


class TestDigestCasts(unittest.TestCase):
  
  def test1(self):
    request = "Give me a summary using keyword bitcoin"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assertEqual(bot.state.selected_action, 'Summary')
    self.assertEqual(bot.state.action_params['keyword'], 'bitcoin')
    self.assertGreaterEqual(len(bot.state.casts), 1)
    
  def test2(self):
    request = "Summary for arts category"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assertEqual(bot.state.selected_action, 'Summary')
    self.assertEqual(bot.state.action_params['category'], 'c_arts')
    self.assertGreaterEqual(len(bot.state.casts), 1)
    
  def test3(self):
    request = "Summary for /data channel?"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assertEqual(bot.state.selected_action, 'Summary')
    self.assertEqual(bot.state.action_params['channel'], 'https://farcaster.group/data')
    self.assertGreaterEqual(len(bot.state.casts), 1)
    
  def test4(self):
    request = "Summary of posts about the beauty of canadian landscapes"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assertEqual(bot.state.selected_action, 'Summary')
    self.assertIsNotNone(bot.state.action_params['search'])
    self.assertGreaterEqual(len(bot.state.casts), 1)
      
  def test5(self):
    request = "Summary of @randombishop's posts"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assertEqual(bot.state.selected_action, 'Summary')
    self.assertEqual(bot.state.action_params['user_name'], 'randombishop')
    self.assertGreaterEqual(len(bot.state.casts), 1)
