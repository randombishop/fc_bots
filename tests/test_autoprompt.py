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
    
