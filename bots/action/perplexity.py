from bots.i_action_step import IActionStep
from bots.autoprompt.perplexity_question_in_channel import perplexity_question_in_channel
from bots.autoprompt.perplexity_question_no_channel import perplexity_question_no_channel
from bots.utils.llms import call_llm
from bots.utils.read_params import read_string
from bots.utils.perplexity_api import call_perplexity

parse_instructions_template = """
You are @{{name}} bot, a social media bot.
Your task is to forward a question to another AI that can search the web and generate an answer.
What question should we submit?
Extract or come up with an appropriate question.
Your goal is not to continue the conversation, you must only extract a question to call the next API.
You can use the conversation as a context, but focus on the last request to come up with a good question.

OUTPUT FORMAT:
{
  "question": ""
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "question":{"type":"STRING"}
  }
}

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


class Perplexity(IActionStep):
  
  def get_cost(self):
    return 100
  
  def auto_prompt(self):
    channel = self.state.selected_channel
    question, log = None, None
    if channel is None or channel in ['', 'None']:
      question, log = perplexity_question_no_channel(self.state)
    else:
      question, log = perplexity_question_in_channel(self.state)
    self.state.action_params = {'question': question}
    self.state.request = f'Ask Perplexity {question}'
    self.state.conversation = self.state.request
    self.state.log += log + '\n'
    
  def parse(self):
    parse_prompt = self.state.format_conversation()
    parse_instructions = self.state.format(parse_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_schema)
    parsed = {}
    parsed['question'] = read_string(params, key='question', default=None, max_length=256)
    self.state.action_params = parsed
    
  def execute(self):
    question = self.state.action_params['question']
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
      links_selection = call_llm(links, select_link_instructions, select_link_schema)
      if 'url' in links_selection and links_selection['url'] is not None and len(links_selection['url']) > 10:
        link = links_selection['url']
      links_log = '<LinksSelection>\n'
      links_log += links + '\n'
      links_log += " >>> " + str(link) + '\n'
      links_log += '</LinksSelection>\n'
      self.state.log += links_log
    if link is not None:
      cast['embeds'] = [link]
      cast['embeds_description'] = 'Link'
    casts = [cast]
    self.state.casts = casts
