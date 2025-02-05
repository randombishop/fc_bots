from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.data.bot_history import get_bot_casts_stats



class TestAutoprompt(unittest.TestCase):
  
  def test1(self):
    stats = get_bot_casts_stats(788096)
    for s in stats:
      print()
    