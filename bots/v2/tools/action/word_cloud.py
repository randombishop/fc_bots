from langchain.agents import Tool


def word_cloud(state):
  cast = {
    'text': "", 
    'embeds': [state.wordcloud_url],
    'embeds_description': 'Wordcloud Image'
  }
  if state.action_params['fid'] is not None and state.action_params['user_name'] is not None:
    cast['mentions'] = [state.action_params['fid']]
    cast['mentions_pos'] = [0]
    cast['mentions_ats'] = [f"@{state.action_params['user_name']}"]
  casts =  [cast]
  state.casts = casts
  return {
    'casts': state.casts
  }

WordCloud = Tool(
  name="word_cloud",
  description="Create a word cloud",
  func=word_cloud,
  metadata={'depends_on': ['parse_word_cloud', 'prepare_word_cloud', 'generate_wordcloud_mask', 'generate_wordcloud']}
)