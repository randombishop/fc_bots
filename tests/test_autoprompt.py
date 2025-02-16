from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import make_bot
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
    print('len(channel_list)', len(bot.state.channel_list))
    print('len(select_channel_df)', len(bot.state.select_channel_df))
    print('select_channel_df:')
    print(bot.state.select_channel_df)
    print(bot.state.select_channel_df.describe())
    print('select_channel_reasoning:')
    print(bot.state.select_channel_reasoning)
    print('select_channel_log:')
    print(bot.state.select_channel_log)
    print('channel', bot.state.channel)
    print('-'*100)
    # select action
    select_action_step = SelectAction(bot.state)
    select_action_step.plan()
    print('selected_action', bot.state.selected_action)
    
  def test2(self):
    bot = make_bot()
    bot.initialize()
    bot.wakeup()
    select_action_step = SelectAction(bot.state)
    select_action_step.plan()
    print('selected_action', bot.state.selected_action)
