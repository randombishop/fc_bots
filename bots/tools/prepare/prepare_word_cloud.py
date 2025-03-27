from langchain.agents import Tool
from bots.utils.word_counts import get_word_counts


def prepare(input):
  state = input.state
  top_n = 50
  posts = []
  if state.get('data_casts_category') is not None:
    posts += state.get('data_casts_category')
  if state.get('data_casts_channel') is not None:
    posts += state.get('data_casts_channel')
  if state.get('data_casts_keyword') is not None:
    posts += state.get('data_casts_keyword')
  if state.get('data_casts_search') is not None:
    posts += state.get('data_casts_search')
  if state.get('data_casts_user') is not None:
    posts += state.get('data_casts_user')
  if state.get('data_casts_text') is not None:
    posts += state.get('data_casts_text')
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

PrepareWordCloud = Tool(
  name="PrepareWordCloud",
  description="Prepare the word cloud data",
  metadata={
    'inputs': ['data_casts_category', 'data_casts_channel', 'data_casts_keyword', 'data_casts_search', 'data_casts_user', 'data_casts_text'],
    'require_inputs': 'any',
    'outputs': ['wordcloud_text', 'wordcloud_counts']
  },
  func=prepare
)
