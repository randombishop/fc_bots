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


def perplexity(input):
  state = input['state']
  llm = input['llm']
  question = state.action_params['question']
  if question is None or len(question) < 5:
    raise Exception("This action requires a question to forward to Perplexity.")
  data = call_perplexity(question)
  answer = None
  try:
    answer = data['choices'][0]['message']['content']
  except Exception:
    raise Exception("Could not get an answer from Perplexity.")
  cast = {'text': answer}
  link = None
  if 'citations' in data and len(data['citations']) > 0:
    links = "\n".join(data['citations'])
    links_selection = call_llm(llm,links, select_link_instructions, select_link_schema)
    if 'url' in links_selection and links_selection['url'] is not None and len(links_selection['url']) > 10:
      link = links_selection['url']
    links_log = '<LinksSelection>\n'
    links_log += links + '\n'
    links_log += " >>> " + str(link) + '\n'
    links_log += '</LinksSelection>\n'
  if link is not None:
    cast['embeds'] = [link]
    cast['embeds_description'] = 'Link'
  casts = [cast]
  state.casts = casts
  return {
    'casts': state.casts,
    'log': links_log
  }


Perplexity = Tool(
  name="perplexity",
  description="Get a perplexity answer",
  func=perplexity,
  metadata={
    'depends_on': ['parse_perplexity_params']
  }
)
