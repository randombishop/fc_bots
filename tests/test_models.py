import unittest
from bots.models.bert import bert
from bots.models.gambit import gambit, categories, topics
from bots.models.bird import bird

class TestModels(unittest.TestCase):
  
  def test_bert(self):
    sentences = [
        "Hay dữ mày! 😘  Hôm nay chị đã dành thời gian để thưởng thức cuộc sống chưa?",
        "Atto km dey ken",
        "Zowie! May today be the start of something beautiful in your life.   "
    ]
    result = bert(sentences)
    self.assertEqual(result.shape[0], 3)
    self.assertEqual(result.shape[1], 512)
    
  def test_gambit(self):
    sentences = [
        "gm crypto folks! long live #bitcoin the king!",
        "Pink Floyd are great artists",
        "Let's talk about football: who is the greatest player of all time?"
    ]
    expected_categories = ['c_crypto', 'c_arts', 'c_sports']
    expected_topics = ['t_bitcoin', 't_music', 't_football']
    embed = bert(sentences)
    df = gambit(embed)
    category_label = list(df[categories].idxmax(axis=1))
    topic_label = list(df[topics].idxmax(axis=1))
    for i in range(len(sentences)):
      self.assertEqual(category_label[i], expected_categories[i])
      self.assertEqual(topic_label[i], expected_topics[i])
      
  def test_bird(self):
    sentences = [
        "gm! I am new to farcaster and looking for instructive content in #ML and #DataScience. Who should I follow?",
        "Leave me alone"
    ]
    embed = bert(sentences)
    df = gambit(embed)
    predict, _, _ = bird(df)
    self.assertEqual(predict.shape[0], 2)
    predict1 = float(predict[0])
    predict2 = float(predict[1])
    self.assertGreater(predict1, predict2)
    
