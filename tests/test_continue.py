from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestContinue(unittest.TestCase):

  def test1(self):
    request = "Not interested."
    state = run_agent(test_id='TestContinue:1', mode='bot', request=request)
    self.assertFalse(state.get('should_continue')) 
    self.assertIsNone(state.get('casts'))

  def test2(self):
    request = "Who are you?"
    state = run_agent(test_id='TestContinue:2', mode='bot', request=request)
    self.assertTrue(state.get('should_continue')) 
    self.assertIsNotNone(state.get('casts'))
    self.assertTrue(state.get('valid'))
    
  def test3(self):
    request = "Thank you so much for sharing 😺❤️❤️❤️"
    fid_origin=388401
    parent_hash='0x7506e607e722d543b61306d1357814ad61caa132'
    state = run_agent(test_id='TestContinue:3', mode='bot', request=request, fid_origin=fid_origin, parent_hash=parent_hash)
    self.assertFalse(state.get('should_continue')) 
    self.assertIsNone(state.get('casts'))
    self.assertTrue(state.get('like')) 