from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent
from bots.data.app import get_bot_prompt


class TestAssistant(unittest.TestCase):
  
  def skip_test1(self):
    prompt = get_bot_prompt(1)
    request = prompt['prompt']
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:1', mode='assistant', request=request, channel=channel)
    self.assertIn('GetMostActiveUsers', state.get_tools_sequence())
    self.assertIn('CreateMostActiveUsersChart', state.get_tools_sequence())
    
  def skip_test2(self):
    prompt = get_bot_prompt(2)
    request = prompt['prompt']
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:2', mode='assistant', request=request, channel=channel)
    self.assertIn('SelectRandomUser', state.get_tools_sequence())
    self.assertIn('GetUserProfile', state.get_tools_sequence())
    self.assertIn('GetCastsUser', state.get_tools_sequence())
    self.assertIn('CreateAvatar', state.get_tools_sequence())
    
  def skip_test3(self):
    prompt = get_bot_prompt(3)
    request = prompt['prompt']
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:3', mode='assistant', request=request, channel=channel)
    self.assertIn('GetCastsChannel', state.get_tools_sequence())
    self.assertIn('CallPerplexity', state.get_tools_sequence())
    
  def skip_test4(self):
    prompt = get_bot_prompt(4)
    request = prompt['prompt']
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:4', mode='assistant', request=request, channel=channel)
    self.assertIn('GetCastsChannel', state.get_tools_sequence())
    
  def skip_test5(self):
    prompt = get_bot_prompt(5)
    request = prompt['prompt']
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:5', mode='assistant', request=request, channel=channel)
    self.assertIn('GetCastsSearch', state.get_tools_sequence())
    
  def skip_test6(self):
    prompt = get_bot_prompt(6)
    request = prompt['prompt']
    channel = prompt['channel']
    state = run_agent(test_id='TestAssistant:6', mode='assistant', request=request, channel=channel)
    self.assertIn('GetNews', state.get_tools_sequence())
    
    
    
