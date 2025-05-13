from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.kit_interface.cast import Cast
from bots.utils.format_cast import extract_cast


class TestExtractCast(unittest.TestCase):

  def test1(self):
    text = "Found one that really made me think. @randombishop asked for a truthful peek into himself. Intriguing! [https://warpcast.com/randombishop/0x86bc73]"
    link = Cast({
      'fid': 'randombishop',
      'username': 'randombishop',
      'hash': '0x86bc732208ee61e82d9e042a0ddaff6b6a1400ea',
      'text': "Tell me something special or unique you've noticed about me, but you think I haven't realized about myself yet.",
      'timestamp': '',
      'when': 'yesterday'
    })
    casts_map = {
      '0x86bc73': link
    }
    cast = extract_cast(text, casts_map, '')
    self.assertEqual(cast['mentions'][0], 253232)
    self.assertEqual(cast['mentions_ats'][0], '@randombishop')
    self.assertEqual(cast['embeds'][0]['hash'], '0x86bc732208ee61e82d9e042a0ddaff6b6a1400ea')
    

  def test2(self):
    text = "Hey friend! The most active folks in /politics lately are @mr-silverback, @javabu.eth, and @icetoad.\nYou can see the chart here: [https://fc.datascience.art/bot/main_files/e6d7c1bb-8a27-4823-a1ac-d8425da08017.png]"
    cast = extract_cast(text, {}, '')
    print(cast)