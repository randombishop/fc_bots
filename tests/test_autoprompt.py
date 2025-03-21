from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestAutoprompt(unittest.TestCase):
  
  def test1(self):
    run_bot(test_id='TestAutoprompt:test1')
    
  def test2(self):
    state = run_bot(selected_channel='data', selected_action='SaySomethingInChannel')
    self.assertEqual(state.request, 'Say something in channel /data')
    
  def test3(self):
    state = run_bot(selected_channel='mfers', selected_action='MostActiveUsers')
    self.assertEqual(state.request, 'Most active users in channel /mfers')
    
  def test4(self):
    state = run_bot(selected_channel='nature', selected_action='Perplexity')
    self.assertIn('Ask Perplexity', state.request)
    
  def test5(self):
    state = run_bot(selected_channel='tabletop', selected_action='Praise')
    self.assertEqual(state.request, 'Praise a random user in channel /tabletop')
    
  def test6(self):
    state = run_bot(selected_channel='product', selected_action='Summary')
    self.assertIn('Summarize', state.request)
  
  def test7(self):
    state = run_bot(selected_channel='None', selected_action='Summary')
    self.assertIn('Summarize', state.request)

  def test8(self):
    state = run_bot(selected_channel='None', selected_action='Perplexity')
    self.assertIn('Ask Perplexity', state.request)