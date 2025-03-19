from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestLike(unittest.TestCase):
  
  def test1(self):
    request = "Thank you!"
    state = run_bot(request)
    self.assertTrue(state.like)
    self.assertFalse(state.reply)
    
  def test2(self):
    request = "Not interested."
    state = run_bot(request)
    self.assertFalse(state.like)
    self.assertFalse(state.reply)