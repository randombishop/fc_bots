from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent



class TestIntents(unittest.TestCase):
  
  def test_favorite_users(self):
    request = "Who are @vitalik.eth's favorite users?"
    state = run_agent(test_id='TestActionSelection:favorite_users', mode='bot',request=request)
    self.assertEqual(state.get('intent'), 'FavoriteUsers')
    
  def test_more_like_this(self):
    request = "More Like This: #Bitcoin is sweet!"
    state = run_agent(test_id='TestActionSelection:more_like_this', mode='bot',request=request)
    self.assertEqual(state.get('intent'), 'MoreLikeThis')
    
  def test_most_active_users(self):
    request = "Who is most active in channel /data?"
    state = run_agent(test_id='TestActionSelection:most_active_users', mode='bot',request=request)
    self.assertEqual(state.get('intent'), 'MostActiveUsers')
    
  def test_news(self):
    request = "Data Science news"
    state = run_agent(test_id='TestActionSelection:news', mode='bot',request=request)
    self.assertEqual(state.get('intent'), 'News')
    
  def test_perplexity(self):
    request = "Ask perplexity to compare Farcaster and Bluesky"
    state = run_agent(test_id='TestActionSelection:perplexity', mode='bot',request=request)
    self.assertEqual(state.get('intent'), 'Perplexity')
    
  def test_pick(self):
    request = "Pick your favorite cast in channel /mfers"
    state = run_agent(test_id='TestActionSelection:pick', mode='bot',request=request)
    self.assertEqual(state.get('intent'), 'Pick')
  
  def test_praise(self):
    request = "Praise @randombishop"
    state = run_agent(test_id='TestActionSelection:praise', mode='bot',request=request)
    self.assertEqual(state.get('intent'), 'Praise')
    
  def test_psycho(self):
    request = "Psycho analyze @v"
    state = run_agent(test_id='TestActionSelection:psycho', mode='bot',request=request)
    self.assertEqual(state.get('intent'), 'Psycho')
    
  def test_roast(self):
    request = "Roast @v"
    state = run_agent(test_id='TestActionSelection:roast', mode='bot',request=request)
    self.assertEqual(state.get('intent'), 'Roast')

  def test_summary(self):
    request = "Give me a summary about keyword ethereum."
    state = run_agent(test_id='TestActionSelection:summary', mode='bot',request=request)
    self.assertEqual(state.get('intent'), 'Summary')
      
  def test_who_is(self):
    request = "Who is @randombishop"
    state = run_agent(test_id='TestActionSelection:who_is', mode='bot',request=request)
    self.assertEqual(state.get('intent'), 'WhoIs')
    
  def test_word_cloud(self):
    request = "Make a wordcloud for user @dwr.eth"
    state = run_agent(test_id='TestActionSelection:word_cloud', mode='bot',request=request)
    self.assertEqual(state.get('intent'), 'WordCloud')