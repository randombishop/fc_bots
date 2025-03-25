from langchain.agents import Tool


def compose_more_like_this(input):
  state = input.state
  similar = state.df_more_like_this
  if similar is None or len(similar) == 0:
    raise Exception("No similar posts found.")
  data = similar.to_dict(orient='records')
  casts = []
  for similar in data[:3]:
    casts.append({
      'text': '', 
      'embeds': [{'fid': similar['fid'], 'user_name': similar['user_name'], 'hash': similar['hash']}],
      'embeds_description': similar['text'],
      'embeds_warpcast': f"https://warpcast.com/{similar['user_name']}/{similar['hash'][:10]}",
      'q_distance': similar['q_distance'],
      'dim_distance': similar['dim_distance']
    })
  state.casts = casts
  return {
    'casts': state.casts
  }


ComposeMoreLikeThis = Tool(
  name="ComposeMoreLikeThis",
  description="Cast first 3 most similar links",
  func=compose_more_like_this
)
