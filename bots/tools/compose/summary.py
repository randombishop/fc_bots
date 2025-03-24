from langchain.agents import Tool


def compose_summary(input):
  state = input.state
  data = state.digest_casts_data
  casts = []
  cast1 = {'text': data['summary']}
  if state.wordcloud_url is not None:
    cast1['embeds'] = [state.wordcloud_url]
    cast1['embeds_description'] = 'Wordcloud'
  casts.append(cast1)
  for link in data['links']:
    casts.append({
      'text': link['comment'], 
      'embeds': [{'fid': link['fid'], 'user_name': link['user_name'], 'hash': link['hash']}],
      'embeds_description': link['text'],
      'embeds_warpcast': f"https://warpcast.com/{link['user_name']}/{link['hash'][:10]}"
    })
  state.casts = casts
  return {'casts': casts}


ComposeSummary = Tool(
  name="ComposeSummary",
  description="Generate a summary of the posts and select some interesting ones",
  func=compose_summary
)
