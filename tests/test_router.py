import unittest
from bots import actions
from bots.router import route
from bots.actions.like import Like

class TestRouter(unittest.TestCase):
  
  def test_chat(self):
    request = "How are you today?"
    action = route(request)
    action.print()
    self.assertIsInstance(action, Like)
    
  def test_digest_casts(self):
    request = "Give me a summary about Bitcoin."
    action = route(request)
    action.print()
    self.assertIsInstance(action, actions.digest_casts.DigestCasts)
    
  def test_favorite_users(self):
    request = "Who are @vitalik.eth's favorite users?"
    action = route(request)
    action.print()
    self.assertIsInstance(action, actions.favorite_users.FavoriteUsers)
  
  def test_more_like_this(self):
    request = "More Like This: #Bitcoin is sweet!"
    action = route(request)
    action.print()
    self.assertIsInstance(action, actions.more_like_this.MoreLikeThis)
    
  def test_most_active_users(self):
    request = "Who is most active in channnel /data?"
    action = route(request)
    action.print()
    self.assertIsInstance(action, actions.most_active_users.MostActiveUsers)
    
  def test_pick_cast(self):
    request = "Pick the funniest cast in channnel /data?"
    action = route(request)
    action.print()
    self.assertIsInstance(action, actions.pick_cast.PickCast)
    
  def test_prefs_cloud(self):
    request = "Make a wordcloud for user @vitalik.eth"
    action = route(request)
    action.print()
    self.assertIsInstance(action, actions.word_cloud.WordCloud)

  def test_psycho(self):
    request = "Psycho analyze @v"
    action = route(request)
    action.print()
    self.assertIsInstance(action, actions.psycho.Psycho)
    
  def test_roast(self):
    request = "Roast @v"
    action = route(request)
    action.print()
    self.assertIsInstance(action, actions.roast.Roast)

  def test_perplexity(self):
    request = "Ask perplexity to live or not to live"
    action = route(request)
    action.print()
    self.assertIsInstance(action, actions.perplexity.Perplexity)

  def test_news(self):
    request = "Data Science news"
    action = route(request)
    action.print()
    self.assertIsInstance(action, actions.news.News)