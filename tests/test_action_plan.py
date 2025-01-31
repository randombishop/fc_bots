import unittest
from bots.utils.tests import make_bot



class TestActionPlan(unittest.TestCase):
  
  def test_chat(self):
    request = "How are you today?"
    bot = make_bot()
    bot.respond(request)
    self.assertIsNone(bot.state.selected_action)
    
  def test_digest_casts(self):
    request = "Give me a summary about Bitcoin."
    bot = make_bot()
    bot.respond(request)
    self.assertEqual(bot.state.selected_action, 'Summary')
    
  def test_favorite_users(self):
    request = "Who are @vitalik.eth's favorite users?"
    bot = make_bot()
    bot.respond(request)
    self.assertEqual(bot.state.selected_action, 'FavoriteUsers')
  
  def test_more_like_this(self):
    request = "More Like This: #Bitcoin is sweet!"
    bot = make_bot()
    bot.respond(request)
    self.assertEqual(bot.state.selected_action, 'MoreLikeThis')
    
  def test_most_active_users(self):
    request = "Who is most active in channnel /data?"
    bot = make_bot()
    bot.respond(request)
    self.assertEqual(bot.state.selected_action, 'MostActiveUsers')
    
  def test_pick_cast(self):
    request = "Pick the funniest cast in channnel /data?"
    bot = make_bot()
    bot.respond(request)
    self.assertEqual(bot.state.selected_action, 'Pick')
    
  def test_prefs_cloud(self):
    request = "Make a wordcloud for user @vitalik.eth"
    bot = make_bot()
    bot.respond(request)
    self.assertEqual(bot.state.selected_action, 'WordCloud')

  def test_psycho(self):
    request = "Psycho analyze @v"
    bot = make_bot()
    bot.respond(request)
    self.assertEqual(bot.state.selected_action, 'Psycho')
    
  def test_roast(self):
    request = "Roast @v"
    bot = make_bot()
    bot.respond(request)
    self.assertEqual(bot.state.selected_action, 'Roast')

  def test_perplexity(self):
    request = "Ask perplexity to live or not to live"
    bot = make_bot()
    bot.respond(request)
    self.assertEqual(bot.state.selected_action, 'Perplexity')

  def test_news(self):
    request = "Data Science news"
    bot = make_bot()
    bot.respond(request)
    self.assertEqual(bot.state.selected_action, 'News')