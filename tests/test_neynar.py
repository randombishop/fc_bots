from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.data.neynar import get_user_info, get_cast_info


class TestNeynar(unittest.TestCase):
  
  def test1(self):
    info = get_user_info(253232)
    self.assertEqual(info['fid'], 253232)
    self.assertEqual(info['user_name'], 'randombishop')
    
  def test2(self):
    info = get_user_info('randombishop')
    self.assertEqual(info['fid'], 253232)
    self.assertEqual(info['user_name'], 'randombishop')

  def test3(self):
    info = get_cast_info('0xf2ec06f84673254e6e6bb88800423603e65f054c')
    self.assertEqual(info['fid'], 253232)
    self.assertEqual(info['username'], 'randombishop')
    self.assertEqual(info['quote']['url'], 'https://randombishop.medium.com/my-journey-into-farcaster-ai-agents-9f9f503f727d')
    
  def test4(self):
    info = get_cast_info('0x4978e05ad19b921d6250426132c97a3b2bb16107')
    self.assertEqual(info['fid'], 253232)
    self.assertEqual(info['username'], 'randombishop')
    self.assertEqual(info['quote']['fid'], 9082)
    self.assertEqual(info['quote']['username'], 'yassinelanda.eth')
