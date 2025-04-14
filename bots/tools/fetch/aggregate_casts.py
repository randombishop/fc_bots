from langchain.agents import Tool


def aggregate_casts(input):
  state = input.state
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
  return {
    'data_casts_all': posts
  }

AggregateCasts = Tool(
  name="AggregateCasts",
  description="Aggregate all fetched casts into a single collection",
  metadata={
    'inputs': ['data_casts_category', 'data_casts_channel', 'data_casts_keyword', 'data_casts_search', 'data_casts_user', 'data_casts_text'],
    'require_inputs': 'any',
    'outputs': ['data_casts_all']
  },
  func=aggregate_casts
)
