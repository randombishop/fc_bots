from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.data import neynar


class TestNeynar(unittest.TestCase):
  
  def test1(self):
    info = neynar.get_user_info(253232)
    self.assertEqual(info['fid'], 253232)
    self.assertEqual(info['user_name'], 'randombishop')
    
  def test2(self):
    info = neynar.get_user_info('randombishop')
    self.assertEqual(info['fid'], 253232)
    self.assertEqual(info['user_name'], 'randombishop')

  def test3(self):
    info = neynar.get_cast_info('0xf2ec06f84673254e6e6bb88800423603e65f054c')
    self.assertEqual(info['fid'], 253232)
    self.assertEqual(info['username'], 'randombishop')
    self.assertEqual(info['quote']['url'], 'https://randombishop.medium.com/my-journey-into-farcaster-ai-agents-9f9f503f727d')
    
  def test4(self):
    info = neynar.get_cast_info('0x4978e05ad19b921d6250426132c97a3b2bb16107')
    self.assertEqual(info['fid'], 253232)
    self.assertEqual(info['username'], 'randombishop')
    self.assertEqual(info['quote']['fid'], 9082)
    self.assertEqual(info['quote']['username'], 'yassinelanda.eth')
    
  def test5(self):
    casts = neynar.get_casts_channel('https://warpcast.com/~/channel/airdrop', 10)
    self.assertEqual(len(casts), 10)
    
  def test6(self):
    casts = neynar.search_casts('ethereum', 'literal', 10)
    self.assertGreater(len(casts), 0)
    
  def test7(self):
    casts = neynar.search_casts('the beauty of canada', 'semantic', 10)
    self.assertGreater(len(casts), 0)
    
  def test8(self):
    casts = neynar.get_casts_user(253232, 10)
    self.assertGreater(len(casts), 0)
    self.assertEqual(casts[0]['username'], 'randombishop')
    
  def test9(self):
    casts = neynar.get_casts_user_channel(253232, 'https://warpcast.com/~/channel/retroparc', 10)
    self.assertGreater(len(casts), 0)
    self.assertEqual(casts[0]['username'], 'randombishop')

  def test10(self):
    likes = neynar.get_user_likes(253232, 10)
    self.assertGreater(len(likes), 0)
    
  def test11(self):
    replies_recasts = neynar.get_user_replies_and_recasts(253232, 1)
    self.assertGreater(len(replies_recasts), 0)

