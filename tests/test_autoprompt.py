from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestAutoprompt(unittest.TestCase):
  
  def test1(self):
    run_bot()
    
  def test2(self):
    bot = run_bot(selected_channel='data', selected_action='SaySomethingInChannel')
    self.assertEqual(bot.state.request, 'Say something in channel /data')
    
  def test3(self):
    bot = run_bot(selected_channel='mfers', selected_action='MostActiveUsers')
    self.assertEqual(bot.state.request, 'Most active users in channel /mfers')
    
  def test4(self):
    bot = run_bot(selected_channel='nature', selected_action='Perplexity')
    self.assertIn('Ask Perplexity', bot.state.request)
    
  def test5(self):
    bot = run_bot(selected_channel='tabletop', selected_action='Praise')
    self.assertEqual(bot.state.request, 'Praise a random user in channel /tabletop')
    
  def test6(self):
    bot = run_bot(selected_channel='product', selected_action='Summary')
    self.assertIn('Summarize', bot.state.request)
  
  def test7(self):
    bot = run_bot(selected_channel='None', selected_action='Summary')
    self.assertIn('Summarize', bot.state.request)

  def test8(self):
    bot = run_bot(selected_channel='None', selected_action='Perplexity')
    self.assertIn('Ask Perplexity', bot.state.request)