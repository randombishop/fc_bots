from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.format_cast import insert_mentions, extract_mentions


expected_full_text = """The most active users are:
🥇 @user_xyz: bla bla bla.
🥈 @u999: x y z.
🥉 @random.eth: GO!"""

class TestTextMentions(unittest.TestCase):

  def test1(self):
    mentions = ['@user_xyz', '@u999', '@random.eth']
    mentions_positions = []
    text = "The most active users are:\n"
    text += "🥇 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += ": bla bla bla.\n"
    text += "🥈 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += ": x y z.\n"
    text += "🥉 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += f": GO!"
    full_text = insert_mentions(text, mentions, mentions_positions)
    print('TestTextMentions:')
    print('full_text')
    print('mentions', mentions)
    print('mentions_positions', mentions_positions)
    self.assertEqual(full_text, expected_full_text)
    text2, mentions2, positions2 = extract_mentions(full_text)
    self.assertEqual(text2, text)
    self.assertEqual(mentions2, mentions)
    self.assertEqual(positions2, mentions_positions)
    
    
    
  