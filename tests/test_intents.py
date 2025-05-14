from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent



class TestIntents(unittest.TestCase):
  
  def test_meta(self):
    request = "What can you do?"
    state = run_agent(test_id='TestIntents:meta', mode='bot',request=request)
    self.assertEqual(state.get_selected_intent(), 'Meta')
    
  def test_avatar_match(self):
    request = "Help me find user profiles similar to @vitalik.eth"
    state = run_agent(test_id='TestIntents:avatar_match', mode='bot',request=request)
    self.assertEqual(state.get_selected_intent(), 'AvatarMatch')
    
  def test_favorite_users(self):
    request = "Who are @vitalik.eth's favorite users?"
    state = run_agent(test_id='TestIntents:favorite_users', mode='bot',request=request)
    self.assertEqual(state.get_selected_intent(), 'FavoriteUsers')
    
  def test_more_like_this(self):
    request = "More Like This: #Bitcoin is sweet!"
    state = run_agent(test_id='TestIntents:more_like_this', mode='bot',request=request)
    self.assertEqual(state.get_selected_intent(), 'MoreLikeThis')
    
  def test_most_active_users(self):
    request = "Who is most active in channel /data?"
    state = run_agent(test_id='TestIntents:most_active_users', mode='bot',request=request)
    self.assertEqual(state.get_selected_intent(), 'MostActiveUsers')
    
  def test_news(self):
    request = "Data Science news"
    state = run_agent(test_id='TestIntents:news', mode='bot',request=request)
    self.assertEqual(state.get_selected_intent(), 'News')
    
  def test_pick(self):
    request = "Pick your favorite cast in channel /mfers"
    state = run_agent(test_id='TestIntents:pick', mode='bot',request=request)
    self.assertEqual(state.get_selected_intent(), 'Pick')
  
  def test_praise(self):
    request = "Praise @randombishop"
    state = run_agent(test_id='TestIntents:praise', mode='bot',request=request)
    self.assertEqual(state.get_selected_intent(), 'Praise')
    
  def test_psycho(self):
    request = "Psycho analyze @v"
    state = run_agent(test_id='TestIntents:psycho', mode='bot',request=request)
    self.assertEqual(state.get_selected_intent(), 'Psycho')
    
  def test_roast(self):
    request = "Roast @v"
    state = run_agent(test_id='TestIntents:roast', mode='bot',request=request)
    self.assertEqual(state.get_selected_intent(), 'Roast')

  def test_summary(self):
    request = "Give me a summary about keyword ethereum."
    state = run_agent(test_id='TestIntents:summary', mode='bot',request=request)
    self.assertEqual(state.get_selected_intent(), 'Summary')
      
  def test_who_is(self):
    request = "Who is @randombishop"
    state = run_agent(test_id='TestIntents:who_is', mode='bot',request=request)
    self.assertEqual(state.get_selected_intent(), 'WhoIs')
    
  def test_word_cloud(self):
    request = "Make a wordcloud for user @dwr.eth"
    state = run_agent(test_id='TestIntents:word_cloud', mode='bot',request=request)
    self.assertEqual(state.get_selected_intent(), 'WordCloud')
    
  def test_user_stats(self):
    request = "How many Brazilians do we have on Farcaster?"
    state = run_agent(test_id='TestUserStats:1', mode='bot', request=request)
    self.assertEqual(state.get_selected_intent(), 'UserStats')