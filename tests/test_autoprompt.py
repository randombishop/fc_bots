from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import make_bot
from bots.utils.tests import run_bot
from bots.plan.select_channel import SelectChannel
from bots.plan.select_action import SelectAction


class TestAutoprompt(unittest.TestCase):
  
  def test1(self):
    bot = make_bot()
    bot.initialize()
    bot.wakeup()
    # select channel
    select_channel_step = SelectChannel(bot.state)
    select_channel_step.plan()
    # select action
    select_action_step = SelectAction(bot.state)
    select_action_step.plan()
    print('selected_action', bot.state.selected_action)
    print('-'*100)
    
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
