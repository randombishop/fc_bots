import unittest
from bots.bot_state import BotState
from bots.think.reply import Reply

class TestReply(unittest.TestCase):
  
  def test1(self):
    state = BotState()
    state.conversation = "Hey what's up?"
    state.casts = [{'text': "Just another day chunking data in Megacity, how about you?"}]
    reply = Reply(state)
    reply.think()
    self.assertTrue(state.reply)
    
  def test2(self):
    state = BotState()
    state.conversation = "Can you answer 1+1=2?"
    state.casts = [{'text': "The population of the world is 7.9 billion."}]
    reply = Reply(state)
    reply.think()
    self.assertFalse(state.reply)
