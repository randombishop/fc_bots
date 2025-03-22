from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot



class TestActionSelection(unittest.TestCase):
  
  def test_chat(self):
    request = "How are you today?"
    state = run_bot(test_id='TestActionSelection:test_chat', request=request)
    self.assertTrue(state.selected_action == 'Chat' or state.selected_action is None)
    
  def test_summary(self):
    request = "Give me a summary about keyword ethereum."
    state = run_bot(test_id='TestActionSelection:test_summary', request=request)
    self.assertEqual(state.selected_action, 'Summary')
    self.assertTrue(state.reply)
    
  def test_favorite_users(self):
    request = "Who are @vitalik.eth's favorite users?"
    state = run_bot(test_id='TestActionSelection:test_favorite_users', request=request)
    self.assertEqual(state.selected_action, 'FavoriteUsers')
    self.assertTrue(state.reply)
  
  def test_more_like_this(self):
    request = "More Like This: #Bitcoin is sweet!"
    state = run_bot(test_id='TestActionSelection:test_more_like_this', request=request)
    self.assertEqual(state.selected_action, 'MoreLikeThis')
    self.assertTrue(state.reply)
    
  def test_most_active_users(self):
    request = "Who is most active in channel /data?"
    state = run_bot(test_id='TestActionSelection:test_most_active_users', request=request)
    self.assertEqual(state.selected_action, 'MostActiveUsers')
    self.assertTrue(state.reply)
    
  def test_pick_cast(self):
    request = "Pick your favorite cast in channel /mfers"
    state = run_bot(test_id='TestActionSelection:test_pick_cast', request=request)
    self.assertEqual(state.selected_action, 'Pick')
    self.assertTrue(state.reply)
    
  def test_word_cloud(self):
    request = "Make a wordcloud for user @vitalik.eth"
    state = run_bot(test_id='TestActionSelection:test_word_cloud', request=request)
    self.assertEqual(state.selected_action, 'WordCloud')
    self.assertTrue(state.reply)

  def test_psycho(self):
    request = "Psycho analyze @v"
    state = run_bot(test_id='TestActionSelection:test_psycho', request=request)
    self.assertEqual(state.selected_action, 'Psycho')
    self.assertTrue(state.reply)
    
  def test_roast(self):
    request = "Roast @v"
    state = run_bot(test_id='TestActionSelection:test_roast', request=request)
    self.assertEqual(state.selected_action, 'Roast')
    self.assertTrue(state.reply)

  def test_perplexity(self):
    request = "Ask perplexity to compare Farcaster and Bluesky"
    state = run_bot(test_id='TestActionSelection:test_perplexity', request=request)
    self.assertEqual(state.selected_action, 'Perplexity')
    self.assertTrue(state.reply)

  def test_news(self):
    request = "Data Science news"
    state = run_bot(test_id='TestActionSelection:test_news', request=request)
    self.assertEqual(state.selected_action, 'News')
    self.assertTrue(state.reply)