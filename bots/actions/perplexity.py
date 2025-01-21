from dotenv import load_dotenv
load_dotenv()
from bots.iaction import IAction
from bots.utils.llms import call_llm
from bots.utils.read_params import read_string
from bots.utils.perplexity_api import call_perplexity
from bots.utils.check_casts import check_casts


parse_instructions = """
You are @dsart bot, a social media bot.
Your task is to forward a question to another AI that can search the web and generate an answer.
What question should we submit?
INSTRUCTIONS:
- Extract or come up with an appropriate question.
- Your goal is not to continue the conversation, you must only extract a question to call the next API.


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




class Perplexity(IAction):
  
  def set_input(self, input):
    params = call_llm(input, parse_instructions, parse_schema)
    self.input = input
    self.set_params(params)
  
  def set_params(self, params):
    self.question = read_string(params, key='question', default=None, max_length=256)
    
  def get_cost(self):
    self.cost = 100
    return self.cost

  def get_data(self):
    if self.question is None or len(self.question) < 5:
      raise Exception("This action requires a question to forward to Perplexity.")
    self.data = call_perplexity(self.question)
    return self.data
    
  def get_casts(self, intro=''):
    answer = None
    try:
      answer = self.data['choices'][0]['message']['content']
    except Exception:
      raise Exception("Could not get an answer from Perplexity.")
    link = None
    if 'citations' in self.data and len(self.data['citations']) > 0:
      link = self.data['citations'][0]
    cast = {'text': answer}
    if link is not None:
      cast['embeds'] = [link]
    casts = [cast]
    check_casts(casts)
    self.casts = casts
    return self.casts
