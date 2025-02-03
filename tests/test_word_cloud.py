import unittest
from bots.utils.tests import make_bot


class TestWordCloud(unittest.TestCase):

  def assert_expected_output(self, bot):
    self.assertEqual(bot.state.selected_action, 'WordCloud')
    self.assertEqual(len(bot.state.casts), 1)
    self.assertEqual(len(bot.state.casts[0]['embeds']), 1)

  def test1(self):
    request = "Make @vitalik.eth's word cloud."
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['fid'], 5650)
    self.assertEqual(bot.state.action_params['user_name'], 'vitalik.eth')
    
  def test2(self):
    request = "Make my word cloud."
    fid_origin = 253232
    bot = make_bot()
    bot.respond(request, fid_origin=fid_origin)
    bot.state.debug_action()
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['fid'], fid_origin)
    self.assertEqual(bot.state.action_params['user_name'], 'randombishop')
    
  def test3(self):
    request = "Make a word cloud for keyword 'bitcoin'"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['keyword'], 'bitcoin')
    
  def test4(self):
    request = "Make a wordcloud for arts category"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['category'], 'c_arts')
     
  def test5(self):
    request = "Make a wordcloud for /data channel?"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['channel'], 'https://farcaster.group/data')

  def test6(self):
    request = "Make a word cloud about the beauty of canadian landscapes"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assert_expected_output(bot)
    self.assertIsNotNone(bot.state.action_params['search'])
      
  def test7(self):
    request = "Make a wordcloud for @randombishop's posts"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['user_name'], 'randombishop')
    
  def test8(self):
    request = "Make a word cloud for this channel"
    root_parent_url = "https://farcaster.group/data"
    bot = make_bot()
    bot.respond(request, root_parent_url=root_parent_url)
    bot.state.debug_action()
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['channel'], root_parent_url)
