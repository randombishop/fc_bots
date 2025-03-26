from langchain.agents import Tool


def compose_roast(input):
  state = input.state
  result = state.user_roast
  if result is None:
    raise Exception(f"Missing roast data")
  cast = {'text': result['tweet']}
  casts = [cast]
  state.casts = casts
  return {
    'casts': state.casts
  }


ComposeRoast = Tool(
  name="ComposeRoast",
  description="Cast the roast of the user",
  func=compose_roast
)