import unittest
from bots.utils.tests import run_bot



class TestActionPlan(unittest.TestCase):
  
  def test_chat(self):
    request = "How are you today?"
    bot = run_bot(request)
    self.assertTrue(bot.state.selected_action == 'Chat' or bot.state.selected_action is None)
    
  def test_digest_casts(self):
    request = "Give me a summary about keyword ethereum."
    bot = run_bot(request)
    self.assertEqual(bot.state.selected_action, 'Summary')
    self.assertTrue(bot.state.reply)
    
  def test_favorite_users(self):
    request = "Who are @vitalik.eth's favorite users?"
    bot = run_bot(request)
    self.assertEqual(bot.state.selected_action, 'FavoriteUsers')
    self.assertTrue(bot.state.reply)
  
  def test_more_like_this(self):
    request = "More Like This: #Bitcoin is sweet!"
    bot = run_bot(request)
    self.assertEqual(bot.state.selected_action, 'MoreLikeThis')
    self.assertTrue(bot.state.reply)
    
  def test_most_active_users(self):
    request = "Who is most active in channel /data?"
    bot = run_bot(request)
    self.assertEqual(bot.state.selected_action, 'MostActiveUsers')
    self.assertTrue(bot.state.reply)
    
  def test_pick_cast(self):
    request = "Pick the funniest cast in channel /mfers"
    bot = run_bot(request)
    self.assertEqual(bot.state.selected_action, 'Pick')
    self.assertTrue(bot.state.reply)
    
  def test_prefs_cloud(self):
    request = "Make a wordcloud for user @vitalik.eth"
    bot = run_bot(request)
    self.assertEqual(bot.state.selected_action, 'WordCloud')
    self.assertTrue(bot.state.reply)

  def test_psycho(self):
    request = "Psycho analyze @v"
    bot = run_bot(request)
    self.assertEqual(bot.state.selected_action, 'Psycho')
    self.assertTrue(bot.state.reply)
    
  def test_roast(self):
    request = "Roast @v"
    bot = run_bot(request)
    self.assertEqual(bot.state.selected_action, 'Roast')
    self.assertTrue(bot.state.reply)

  def test_perplexity(self):
    request = "Ask perplexity to compare Farcaster and Bluesky"
    bot = run_bot(request)
    self.assertEqual(bot.state.selected_action, 'Perplexity')
    self.assertTrue(bot.state.reply)

  def test_news(self):
    request = "Data Science news"
    bot = run_bot(request)
    self.assertEqual(bot.state.selected_action, 'News')
    self.assertTrue(bot.state.reply)