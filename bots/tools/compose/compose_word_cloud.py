from langchain.agents import Tool


def compose_word_cloud(input):
  state = input.state
  if state.wordcloud_url is None:
    raise Exception("Missing wordcloud_url")
  cast = {
    'text': "", 
    'embeds': [state.wordcloud_url],
    'embeds_description': 'Wordcloud Image'
  }
  if (state.user_fid is not None) and (state.user is not None):
    cast['mentions'] = [state.user_fid]
    cast['mentions_pos'] = [0]
    cast['mentions_ats'] = [f"@{state.user}"]
  casts =  [cast]
  state.casts = casts
  return {
    'casts': state.casts
  }


ComposeWordCloud = Tool(
  name="ComposeWordCloud",
  description="Create a word cloud",
  func=compose_word_cloud,
  metadata={'depends_on': ['parse_word_cloud_params', 'prepare_word_cloud', 'generate_wordcloud_mask', 'generate_wordcloud']}
)