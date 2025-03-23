from langchain.agents import Tool


def compose_perplexity(input):
  state = input.state
  answer = state.perplexity_answer
  link = state.perplexity_link
  if answer is None or len(answer) < 5:
    raise Exception("Missing perplexity data")
  cast = {'text': answer}
  if link is not None:
    cast['embeds'] = [link]
    cast['embeds_description'] = 'Link'
  casts = [cast]
  state.casts = casts
  return {
    'casts': state.casts
  }


ComposePerplexity = Tool(
  name="ComposePerplexity",
  description="Get a perplexity answer",
  func=compose_perplexity
)
