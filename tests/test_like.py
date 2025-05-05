from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestLike(unittest.TestCase):
  
  def test1(self):
    request = "Thank you!"
    state = run_agent(test_id='TestLike:1', mode='bot', request=request)
    self.assertTrue(state.like)
    self.assertFalse(state.should_continue)
    
  def test2(self):
    request = "Not interested."
    state = run_agent(test_id='TestLike:2', mode='bot', request=request)
    self.assertFalse(state.like)
    self.assertFalse(state.should_continue)
