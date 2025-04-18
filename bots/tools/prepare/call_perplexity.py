from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.perplexity_api import call_perplexity


select_link_instructions = """
You are provided with a list of URLs.
Your task is to select the URL from the most well known domain.
Do not select URLs if the domain name is not well known.
Prefer URLs from famous origins such as wikipedia, reddit, youtube, medium articles, yahoo news, mainstream media institutions, reuters, and similar.
Avoid URLs from domains where you don't have enough information.
Avoid URLs that might be a commercial or a link to a specific product.
If none of the URLs meets our criteria, return {"url": null}
Return your response as a JSON object.

OUTPUT FORMAT:
{
  "url": "..."
}
"""


select_link_schema = {
  "type":"OBJECT",
  "properties":{
    "url":{"type":"STRING"}
  }
}


def prepare(input):
  state = input.state
  question = state.get('question')
  if len(question) < 5:
    raise Exception("This tool requires a question to forward to Perplexity.")
  data = call_perplexity(question)
  answer = None
  try:
    answer = data['choices'][0]['message']['content']
  except Exception:
    raise Exception("Could not get an answer from Perplexity.")
  link = None
  if 'citations' in data and len(data['citations']) > 0:
    links = "\n".join(data['citations'])
    links_selection = call_llm('medium', links, select_link_instructions, select_link_schema)
    if 'url' in links_selection and links_selection['url'] is not None and len(links_selection['url']) > 10:
      link = links_selection['url']
  return {
    'perplexity_answer': answer,
    'perplexity_link': link
  }


CallPerplexity = Tool(
  name="CallPerplexity",
  description="Call perplexity API with a question",
  metadata={
    'inputs': ['question'],
    'outputs': ['perplexity_answer', 'perplexity_link']
  },
  func=prepare
)
