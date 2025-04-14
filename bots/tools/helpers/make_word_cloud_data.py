from langchain.agents import Tool
from bots.utils.word_counts import get_word_counts


def prepare(input):
  state = input.state
  top_n = 50
  posts = state.get('data_casts_all')
  if len(posts) == 0:
    raise Exception(f"Not enough activity to buid a word cloud.")
  posts = [x['text'] for x in posts]
  word_counts = get_word_counts(posts, top_n)
  if len(word_counts) < 5:
    raise Exception(f"Not enough activity to buid a word cloud.")
  top_5 = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:5]
  top_5 = " ".join([x[0] for x in top_5])
  return {
    'wordcloud_text': top_5,
    'wordcloud_counts': word_counts
  }

MakeWordCloudData = Tool(
  name="MakeWordCloudData",
  description="Make the word cloud text and counts",
  metadata={
    'inputs': ['data_casts_all'],
    'outputs': ['wordcloud_text', 'wordcloud_counts']
  },
  func=prepare
)
