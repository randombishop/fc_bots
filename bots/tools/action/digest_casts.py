from langchain.agents import Tool


def digest_casts(input):
  state = input['state']
  data = state.digest_casts_data
  casts = []
  cast1 = {'text': data['summary']}
  if 'wordcloud' in data:
    cast1['embeds'] = [data['wordcloud']]
    cast1['embeds_description'] = 'Wordcloud of words used in the posts'
  casts.append(cast1)
  for link in data['links']:
    casts.append({
      'text': link['comment'], 
      'embeds': [{'fid': link['fid'], 'user_name': link['user_name'], 'hash': link['hash']}],
      'embeds_description': link['text']
    })
  state.casts = casts
  return {'casts': casts}


Summary = Tool(
  name="Summary",
  description="Generate a summary of the posts and select some interesting ones",
  func=digest_casts,
  metadata={'depends_on': [
    'parse_digest_casts', 
    'prepare_digest_casts', 
    'generate_wordcloud_mask', 
    'generate_wordcloud'
  ]}
)
