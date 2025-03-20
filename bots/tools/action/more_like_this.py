from langchain.agents import Tool
from bots.data.casts import get_more_like_this


def more_like_this(input):
  state = input['state']
  exclude_hash = state.attachment_hash if state.attachment_hash is not None else state.parent_hash
  similar = get_more_like_this(state.action_params['text'], exclude_hash=exclude_hash, limit=3)
  if len(similar) == 0:
    raise Exception("No similar posts found.")
  data = similar.to_dict(orient='records')
  casts = []
  for similar in data:
    casts.append({
      'text': '', 
      'embeds': [{'fid': similar['fid'], 'user_name': similar['user_name'], 'hash': similar['hash']}],
      'embeds_description': similar['text'],
      'q_distance': similar['q_distance'],
      'dim_distance': similar['dim_distance']
    })
  state.casts = casts
  return {
    'casts': state.casts
  }


MoreLikeThis = Tool(
  name="more_like_this",
  description="Find similar posts",
  func=more_like_this,
  metadata={
    'depends_on': ['parse_more_like_this_params']
  }
)
