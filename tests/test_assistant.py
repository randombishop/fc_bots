from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


prompt1 = """
Post about the most active users in a channel in a way that fits the channel spirit.
Tag the top 3 and show them some appreciation for their contributions.
Embed the activity chart url.
"""

prompt2 = """
Pick a random user and post a thread to praise them.
Embed their generated avatar in the first post and links to their best posts on the next ones.
"""



class TestAssistant(unittest.TestCase):
  
  def test1(self):
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:1', mode='assistant', request=prompt1, channel=channel)
    self.assertIn('GetMostActiveUsers', state.get_tools_sequence())
    self.assertIn('CreateMostActiveUsersChart', state.get_tools_sequence())
    
  def test2(self):
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:2', mode='assistant', request=prompt2, channel=channel)
    self.assertIn('SelectRandomUser', state.get_tools_sequence())
    self.assertIn('GetUserProfile', state.get_tools_sequence())
    self.assertIn('GetCastsUser', state.get_tools_sequence())
    self.assertIn('CreateAvatar', state.get_tools_sequence())