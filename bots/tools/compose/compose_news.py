from langchain.agents import Tool


def compose_news(input):
  state = input.state
  data = state.yahoo_news
  if data is None or 'tweet' not in data:
    raise Exception("Could not get a news story")
  cast = {'text': data['tweet']}
  if 'url' in data and len(data['url']) > 10:
    link = data['url']
    cast['embeds'] = [link]
    cast['embeds_description'] = 'Link to the story'
  casts = [cast]
  state.casts = casts
  return {
    'casts': state.casts
  }


ComposeNews = Tool(
  name="ComposeNews",
  description="Cast the news story",
  func=compose_news
)
