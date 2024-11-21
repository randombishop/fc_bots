import unittest
from bots import actions
from bots.router import route


class TestRouter(unittest.TestCase):
  
  def test_chat(self):
    request = "How are you today?"
    action = route(request)
    self.assertIsInstance(action, actions.chat.Chat)
    
  def test_digest_casts(self):
    request = "Give me a summary about Bitcoin."
    action = route(request)
    self.assertIsInstance(action, actions.digest_casts.DigestCasts)
    
  def test_favorite_users(self):
    request = "Who are @vitalik.eth's favorite users?"
    action = route(request)
    self.assertIsInstance(action, actions.favorite_users.FavoriteUsers)
    
  def test_most_active_users(self):
    request = "Who is most active in channnel /data?"
    action = route(request)
    self.assertIsInstance(action, actions.most_active_users.MostActiveUsers)
    
  def test_pick_cast(self):
    request = "Pick the funniest cast in channnel /data?"
    action = route(request)
    self.assertIsInstance(action, actions.pick_cast.PickCast)
    
  def test_prefs_cloud(self):
    request = "Make a wordcloud for user @vitalik.eth"
    action = route(request)
    self.assertIsInstance(action, actions.word_cloud.WordCloud)

  def test_psycho(self):
    request = "Psycho analyze @v"
    action = route(request)
    self.assertIsInstance(action, actions.psycho.Psycho)
    
  def test_roast(self):
    request = "Roast @v"
    action = route(request)
    self.assertIsInstance(action, actions.roast.Roast)
