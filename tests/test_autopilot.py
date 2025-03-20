from dotenv import load_dotenv
load_dotenv()
import os
import unittest
from bots.utils.tests import run_bot


bot_id = int(os.getenv('TEST_BOT'))


class TestAutopilot(unittest.TestCase):
  
  def test1(self):
    request = 'Who is most active in channel /data'
    run_bot(test_id='TestAutopilot:test1', request=request)
    
