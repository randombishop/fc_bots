from langchain.agents import Tool


def compose_news(input):
  state = input.state
  data = state.get('data_yahoo_news')
  cast = {'text': data['tweet']}
  if 'url' in data and len(data['url']) > 10:
    link = data['url']
    cast['embeds'] = [link]
    cast['embeds_description'] = 'Link to the story'
  casts = [cast]
  return {
    'casts': casts
  }


ComposeNews = Tool(
  name="ComposeNews",
  description="Cast the news story",
  func=compose_news
)
