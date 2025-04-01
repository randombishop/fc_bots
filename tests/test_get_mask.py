from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import make_tool_input
from bots.tools.helpers.make_word_cloud_mask import prepare


class TestGetMask(unittest.TestCase):
  
  def test1(self):
    wordcloud_text = "Japan posts: from zen cushions to Valentine's Day traditions, and even a lost mask!  Explore the diverse experiences of Farcaster users in Japan."
    wordcloud_counts = {'farcaster': 21, 'collection': 16, 'minted': 15, 'faces': 15, 'custom': 15, 'onchain': 15, 'exclusively': 15, 'farcasters': 15, 'gidi': 11, 'kong': 11, 'love': 5, 'fiery': 5, 'different': 5, 'look': 4, 'completed': 4, 'liveart': 4, 'dreamverse': 4, 'layer': 4, 'adventure': 4, 'dark': 3, 'days': 3, 'find': 3, 'peace': 3, 'beauty': 3, 'hand': 3, 'explore': 3, 'digital': 3, 'mysticism': 3, 'being': 3, 'creative': 3, 'vinci': 3, 'eternal': 3, 'vibes': 2, 'world': 2, 'time': 2, 'night': 2, 'itap': 2, 'denver': 2, 'dive': 2, 'everything': 2, 'cool': 2, 'style': 2, 'blending': 2, 'illustrations': 2, 'mona': 2, 'lisa': 2, 'leonardo': 2, 'painting': 2, 'every': 2, 'shes': 2, 'people': 2, 'opening': 2}
    input = make_tool_input({
      'wordcloud_text': wordcloud_text,
      'wordcloud_counts': wordcloud_counts
    })
    result = prepare(input)
    self.assertEqual(result['wordcloud_width'], 1024)
    self.assertEqual(result['wordcloud_height'], 1024)
    
  