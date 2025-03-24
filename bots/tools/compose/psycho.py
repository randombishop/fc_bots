from langchain.agents import Tool


def compose_psycho(input):
  state = input.state
  result = state.user_psycho
  if result is None:
    raise Exception(f"Missing psycho analysis data")
  casts = []
  if 'sentence1' in result:
    casts.append({'text': result['sentence1']})
  if 'sentence2' in result:
    casts.append({'text': result['sentence2']})
  if 'sentence3' in result:
    casts.append({'text': result['sentence3']})
  state.casts = casts
  return {
    'casts': state.casts
  }


ComposePsycho = Tool(
  name="ComposePsycho",
  description="Cast the psycho analysis of a user",
  func=compose_psycho
)
