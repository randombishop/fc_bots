from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import make_tool_input
from bots.tools.check.reply import Reply


class TestReply(unittest.TestCase):
  
  def test1(self):
    input = make_tool_input()
    input.state.conversation = "Hey what's up?"
    input.state.casts = [{'text': "Just another day chunking data in Megacity, how about you?"}]
    Reply.invoke({'input': input})
    self.assertTrue(input.state.reply)
    
  def test2(self):
    input = make_tool_input()
    input.state.conversation = "Can you answer 1+1=2?"
    input.state.casts = [{'text': "The population of the world is 7.9 billion."}]
    Reply.invoke({'input': input})
    self.assertFalse(input.state.reply)
