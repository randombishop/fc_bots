from langchain.agents import Tool
from bots.data.casts import get_more_like_this as get_more_like_this_data


def get_more_like_this(input):
  state = input.state
  if state.text is None:
    raise Exception("Missing text param")
  exclude_hash = state.attachment_hash if state.attachment_hash is not None else state.parent_hash
  df = get_more_like_this_data(state.text, exclude_hash=exclude_hash, limit=10)
  state.df_more_like_this = df
  return {
    'df_more_like_this': state.df_more_like_this
  }


GetMoreLikeThis = Tool(
  name="GetMoreLikeThis",
  description="Find similar posts",
  metadata={
    'inputs': 'Requires text parameter, will fail if not set',
    'outputs': 'Dataframe df_more_like_this'
  },
  func=get_more_like_this
)
