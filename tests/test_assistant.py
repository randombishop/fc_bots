from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestAssistant(unittest.TestCase):
  
  def test1(self):
    request = """
    Create the most active users chart for the channel.
    Post about the most active ones in a way that fits the channel spirit.
    Tag the top 3 and show them some appreciation for their contributions.
    Embed the activity chart url.
    """
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:1', mode='assistant', request=request, channel=channel)
    self.assertIn('MostActiveUsers', state.get_variable_types())
    self.assertIn('MostActiveUsersChart', state.get_variable_types())
    
  def test2(self):
    request = """
    Pick a random user and post a thread to praise them.
    Embed their generated avatar in the first cast.
    Link to their best post on the second cast.
    Finally, invite them to try the avatar match mini app in the last cast.
    """
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:2', mode='assistant', request=request, channel=channel)
    self.assertIn('Avatar', state.get_variable_types())
    self.assertIn('MiniApp', state.get_variable_types())
    
    
  def test3(self):
    request = """
    First, fetch the casts from the channel.
    Then use recent channel activity to generate a relevant news search phrase that will be interesting to the channel audience.
    Your search phrase should be simple, short, and genuine: what news would you like to hear if you were a member of this channel?
    Your search phrase should yield results from a general news source such as yahoo news, don't make your search phrase too farcaster-specific or too obscure.
    Pick a search phrase that is generic enough to yield enough results from a search engine like yahoo news.
    Once your search phrase is ready, use it to fetch a news story.
    Once you have the news story, post something original, interesting and relevant to the channel.
    Make sure your post will be engaging for the channel audience, and double check that the url you embed is not off-topic.
    """
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:3', mode='assistant', request=request, channel=channel)
    self.assertIn('News', state.get_variable_types())


  def test4(self):
    request = """
    First, fetch the casts from the channel.
    Then study the channel activity carefully and summarize it.
    Then generate an original, creative and engaging post.
    It can be a question, an affirmation, a joke or a haiku.
    If something is at the intersection of the channel activity and your character (bio and lore), it will be a great post idea.
    Make sure your post is inline with the recent channel activity BUT DO NOT COPY OTHER POSTS.
    Avoid repeating things you already posted.
    """
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:4', mode='assistant', request=request, channel=channel)
    self.assertIsNotNone(state.casts)
    
  def test5(self):
    request = """
    Your goal is to be a polarity detector in the channel.
    First fetch the casts from the channel, then create a word cloud from the casts.
    Once your data is ready, study the channel activity carefully to detect 2 opposed camps, use any criteria you want.
    Classify the casts into 2 camps, then make a thread about it.
    In the first cast, describe the opposition that you discovered, maybe in the form of a question, and include a link to the wordcloud.
    Then in the second and third casts, describe each side, and link to an example cast to illustrate each side of the polarity.
    """
    channel = 'mfers'
    state = run_agent(test_id='TestAssistant:5', mode='assistant', request=request, channel=channel)
    self.assertIn('WordCloudImage', state.get_variable_types())
    
  def test6(self):
    request = """
    Your goal is to post an interesting news story about classic cars in channel /retroparc.
    Create a search phrase that will be interesting to the channel audience and can yield news about classic cars.
    Use the search phrase to check out the news then compose an engaging cast about it.
    Include the url link to the story in your post.
    """
    channel = 'retroparc'
    state = run_agent(test_id='TestAssistant:6', mode='assistant', request=request, channel=channel)
    self.assertIn('News', state.get_variable_types())
    self.assertIsNotNone(state.casts[0]['embeds'])
    
  def test7(self):
    request = """
    You are an expert in web3 apps and you are going to provide insights to builders into social app patterns and tips that they could use. 
    This can be about onboarding users, retaining them, adding things like social proof, or anything else in the social app builder toolkit.
    """
    state = run_agent(test_id='TestAssistant:7', mode='assistant', request=request)
    self.assertIsNotNone(state.casts)
    
  def test8(self):
    request = """
    Find the most liked and commented cast in the Japan channel, then cast about it, and tag those who shared it.
    Also, please include the link of that cast.
    """
    channel = 'japan'
    state = run_agent(test_id='TestAssistant:8', mode='assistant', request=request, channel=channel)
    self.assertIsNotNone(state.casts)
    
