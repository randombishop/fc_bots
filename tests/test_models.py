import unittest
from bots.models.bert import preprocess, bert


class TestModels(unittest.TestCase):
  
  def test_bert(self):
    sentences = [
        "Hay dữ mày! 😘  Hôm nay chị đã dành thời gian để thưởng thức cuộc sống chưa?",
        "Atto km dey ken",
        "Zowie! May today be the start of something beautiful in your life.   "
    ]
    result = bert(sentences)
    print(result)
    