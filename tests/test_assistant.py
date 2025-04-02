from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent
from bots.data.assistants import get_bot_prompt


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

prompt4 = """
First, study the channel activity carefully and summarize it.
Then generate an original, creative and engaging post.
It can be a question, an affirmation, a joke or a haiku.
If something is at the intersection of the channel activity and your character (bio and lore), it will be a great post idea.
Make sure your post is inline with the recent channel activity BUT DO NOT COPY OTHER POSTS.
Avoid repeating things you already posted.
"""

prompt5 = """
Your goal is to be a polarity detector in the channel.
Use recent channel activity to generate a search phrase that will be interesting to the channel audience and can yield opposed opinions.
Once your search phrase is ready, use it to search for casts.
Once you have your posts, classify them into 2 opposed camps by any criteria you want, then make a thread about it.
In the first post, describe the opposition that you discovered, maybe in the form of a question, and embed a wordcloud in embed_url1.
Then in the second and third posts, describe each side, and embed an example post to illustrate the categories in embed_hash2 and embed_hash3.
"""

prompt6 = """
Your goal is to post an interesting news story about classic cars in channel /retroparc.
Create a search phrase that will be interesting to the channel audience and can yield news about classic cars.
Use the search phrase to check out the news then compose an engaging cast about it.
Include a link to the story in embed_url1.
"""


class TestAssistant(unittest.TestCase):
  
  def test1(self):
    prompt = get_bot_prompt(1)
    request = prompt['prompt']
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:1', mode='assistant', request=request, channel=channel)
    self.assertIn('GetMostActiveUsers', state.get_tools_sequence())
    self.assertIn('CreateMostActiveUsersChart', state.get_tools_sequence())
    
  def test2(self):
    prompt = get_bot_prompt(2)
    request = prompt['prompt']
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:2', mode='assistant', request=request, channel=channel)
    self.assertIn('SelectRandomUser', state.get_tools_sequence())
    self.assertIn('GetUserProfile', state.get_tools_sequence())
    self.assertIn('GetCastsUser', state.get_tools_sequence())
    self.assertIn('CreateAvatar', state.get_tools_sequence())
    
  def test3(self):
    prompt = get_bot_prompt(3)
    request = prompt['prompt']
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:3', mode='assistant', request=request, channel=channel)
    self.assertIn('GetCastsChannel', state.get_tools_sequence())
    self.assertIn('CallPerplexity', state.get_tools_sequence())
    
  def test4(self):
    prompt = get_bot_prompt(4)
    request = prompt['prompt']
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:4', mode='assistant', request=request, channel=channel)
    self.assertIn('GetCastsChannel', state.get_tools_sequence())
    
  def test5(self):
    prompt = get_bot_prompt(5)
    request = prompt['prompt']
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:5', mode='assistant', request=request, channel=channel)
    self.assertIn('GetCastsSearch', state.get_tools_sequence())
    
  def test6(self):
    prompt = get_bot_prompt(6)
    request = prompt['prompt']
    channel = prompt['channel']
    state = run_agent(test_id='TestAssistant:6', mode='assistant', request=request, channel=channel)
    self.assertIn('GetNews', state.get_tools_sequence())
    
    
    
