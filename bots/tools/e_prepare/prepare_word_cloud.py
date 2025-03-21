from langchain.agents import Tool
from bots.data.casts import get_top_casts, get_more_like_this
from bots.utils.word_counts import get_word_counts


def prepare_word_cloud(input):
  state = input.state
  top_n = 50
  posts = []
  if state.search is not None:
    posts = get_more_like_this(state.search, limit=state.max_rows)
  else:
    posts = get_top_casts(channel=state.channel_url,
                          keyword=state.keyword,
                          category=state.category,
                          user_name=state.user,
                          max_rows=state.max_rows)
  if posts is None or len(posts) == 0:
    raise Exception(f"Not enough activity to buid a word cloud.")
  posts = posts['text'].tolist()
  word_counts = get_word_counts(posts, top_n)
  if len(word_counts) < 5:
    raise Exception(f"Not enough activity to buid a word cloud.")
  top_5 = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:5]
  top_5 = " ".join([x[0] for x in top_5])
  state.wordcloud_text = top_5
  state.wordcloud_counts = word_counts
  return {
    'wordcloud_text': state.wordcloud_text,
    'wordcloud_counts': state.wordcloud_counts
  }

PrepareWordCloud = Tool(
  name="prepare_word_cloud",
  description="Prepare the word cloud data",
  func=prepare_word_cloud
)
