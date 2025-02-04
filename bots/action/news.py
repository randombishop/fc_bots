from bots.i_action_step import IActionStep
from bots.prompts.contexts import conversation_and_request_template
from bots.utils.llms import call_llm
from bots.utils.read_params import read_string
from bots.utils.skyvern_api import start_workflow, get_workflow_result


parse_instructions_template = """
You are @{{name}} bot, a social media bot.
Your task is to forward a search query to a news API and get an interesting story.
What search query should we submit?
Extract or come up with an appropriate search query.
Your goal is not to continue the conversation, you must only extract a search query to call the next API.
You can use the conversation as a context for the request, but focus on the last request to come up with a good search query.

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


class News(IActionStep):
  
  def get_cost(self):
    return 100

  def parse(self):
    parse_prompt = self.state.format(conversation_and_request_template)
    parse_instructions = self.state.format(parse_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_schema)
    parsed = {}
    parsed['search'] = read_string(params, key='search', default=None, max_length=256)
    self.state.action_params = parsed
  
  def execute(self):
    search = self.state.action_params['search']
    if search is None or len(search) < 5:
      raise Exception("This action requires a search query to forward to Yahoo News.")
    run_id = start_workflow(skyvern_workflow, {"search": search})
    result = get_workflow_result(skyvern_workflow, run_id)
    if result['status'] != 'completed':
      raise Exception("Workflow did not complete")
    data = result['outputs']['Generate_output']['extracted_information']
    if data is None or 'tweet' not in data:
      raise Exception("Could not get a news story")
    cast = {'text': data['tweet']}
    if 'url' in data and len(data['url']) > 10:
      link = data['url']
      cast['embeds'] = [link]
      cast['embeds_description'] = 'Link to the story'
    casts = [cast]
    self.state.casts = casts
