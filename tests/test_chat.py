from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestChat(unittest.TestCase):

  def test1(self):
    request = "Not interested."
    state = run_bot(test_id='TestChat:test1', request=request)
    self.assertTrue(state.action is None or state.action == 'Chat')
    self.assertFalse(state.should_continue) 
    self.assertIsNone(state.casts)
    self.assertFalse(state.reply) 

  def test2(self):
    request = "Chat with me: Who are you?"
    state = run_bot(test_id='TestChat:test2', request=request)
    self.assertTrue(state.action == 'Chat')
    self.assertEqual(len(state.casts), 1)
    self.assertTrue(state.reply)
    

  def test3(self):
    request = "Chat with me: Do you think DeepSeek will surpass OpenAI?"
    fid_origin=253232
    state = run_bot(test_id='TestChat:test3', request=request, fid_origin=fid_origin)
    self.assertTrue(state.action == 'Chat')
    self.assertEqual(len(state.casts), 1)
    self.assertEqual(state.category, 'c_tech_science')
    self.assertEqual(state.user_origin, 'randombishop')

  def test4(self):
    request = "Thank you so much for sharing 😺❤️❤️❤️"
    fid_origin=388401
    parent_hash='0x7506e607e722d543b61306d1357814ad61caa132'
    state = run_bot(test_id='TestChat:test4', request=request, fid_origin=fid_origin, parent_hash=parent_hash)
    self.assertTrue(state.action is None or state.action == 'Chat')
    self.assertIsNone(state.casts)
    self.assertFalse(state.reply) 