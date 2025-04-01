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

prompt3 = """
Use recent channel activity to generate a relevant question that will be interesting to the channel audience.
Your question should be simple, short, original, interesting and creative.
Your question should be genuine: what would you like to know if you were a member of this channel?
Do not generate multiple questions or complex questions.
Generate only one single, simple and short question.
Once your question is ready, forward it to Perplexity AI.
Once you have the answer from perplexity and selected a good URL, post something original, interesting and relevant to the channel.
Make sure your post will be engaging for the channel audience, and double check that the url you embed is not off-topic.
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
    
  def test3(self):
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:3', mode='assistant', request=prompt3, channel=channel)
    
