from langchain.agents import Tool
from bots.data.casts import get_more_like_this
from bots.utils.format_cast import concat_casts


def fetch(input):
  state = input.state
  exclude_hash = state.attachment_hash if state.attachment_hash is not None else state.parent_hash
  df = get_more_like_this(state.text, exclude_hash=exclude_hash, limit=10)
  posts = df.to_dict('records') if len(df) > 0 else []
  casts_text = concat_casts(posts)
  state.add_posts(posts)
  return {
    'casts_text': casts_text,
    'data_casts_text': posts
  }


GetMoreLikeThis = Tool(
  name="GetMoreLikeThis",
  description="Find similar posts using parameter text",
  metadata={
    'inputs': ['text'],
    'outputs': ['casts_text', 'data_casts_text']
  },
  func=fetch
)
