from dotenv import load_dotenv
load_dotenv()
from bots.iaction import IAction
from bots.utils.llms import call_llm
from bots.utils.read_params import read_string
from bots.utils.skyvern_api import start_workflow, get_workflow_result
from bots.utils.check_casts import check_casts


parse_instructions = """
You are @dsart bot, a social media bot.
Your task is to forward a search query to yahoo news API and get an interesting story.
What search query should we submit?
INSTRUCTIONS:
- Extract or come up with an appropriate search query.
- Your goal is not to continue the conversation, you must only extract a search query to call the next API.


OUTPUT FORMAT:
{
  "search": "..."
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "search":{"type":"STRING"}
  }
}

skyvern_workflow = "wpid_351323221886267440"


class News(IAction):
  
  def set_input(self, input):
    params = call_llm(input, parse_instructions, parse_schema)
    self.input = input
    self.set_params(params)
  
  def set_params(self, params):
    self.search = read_string(params, key='search', default=None, max_length=256)
    
  def get_cost(self):
    self.cost = 100
    return self.cost

  def get_data(self):
    if self.search is None or len(self.search) < 5:
      raise Exception("This action requires a search query to forward to Yahoo News.")
    run_id = start_workflow(skyvern_workflow, {"search": self.search})
    result = get_workflow_result(skyvern_workflow, run_id)
    if result['status'] != 'completed':
      raise Exception("Workflow did not complete")
    self.data = result['outputs']['Generate_output']['extracted_information']
    return self.data
    
  def get_casts(self, intro=''):
    if self.data is None or 'tweet' not in self.data:
      raise Exception("Could not get a news story")
    cast = {'text': self.data['tweet']}
    if 'url' in self.data and len(self.data['url']) > 10:
      link = self.data['url']
      cast['embeds'] = [link]
    casts = [cast]
    check_casts(casts)
    self.casts = casts
    return self.casts
