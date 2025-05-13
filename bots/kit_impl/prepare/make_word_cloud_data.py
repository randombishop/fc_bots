from bots.kit_interface.casts import Casts
from bots.kit_interface.word_cloud_data import WordCloudData
from bots.utils.word_counts import get_word_counts


def make_word_cloud_data(casts: Casts) -> WordCloudData:
  top_n = 50
  posts = casts.casts
  if len(posts) == 0:
    raise Exception(f"Not enough activity to buid a word cloud.")
  posts = [x.text for x in posts]
  word_counts = get_word_counts(posts, top_n)
  if len(word_counts) < 5:
    raise Exception(f"Not enough activity to buid a word cloud.")
  top_5 = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:5]
  top_5 = " ".join([x[0] for x in top_5])
  return WordCloudData(top_5, word_counts)

