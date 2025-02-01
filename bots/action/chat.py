from bots.i_action_step import IActionStep
from bots.prompts.contexts import conversation_and_request_template
from bots.utils.read_params import read_boolean, read_keyword, read_category, read_string
from bots.data.casts import get_casts_for_fid
from bots.utils.llms import call_llm
from bots.utils.check_casts import check_casts

preprocessing_instructions_template =  """
You are @{{name}}, a social media bot.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#CURRENT CHANNEL
{{channel}}

#TASK
Before responding to the user, you must evaluate if you should continue this conversation or not. 
If the user asks an interesting question or if their tone elicits a response from you, you should continue the conversation.
If the conversation is going in a contructive direction and produces interesting information from both sides, you should continue the conversation.
If it's just a greeting, a thank you note, or a closing comment, you should not continue the conversation.
If the conversation is not constructive, enters some kind of loop, or is not going anywhere, you should not continue the conversation.
If the conversation has been going back and forth for more than 10 messages without any progress, you should not continue the conversation.
You must only evaluate if you should continue the conversation or ignore the last request.
You must respond with a json like this {"continue": true/false}.
Return your evaluation in valid json format.

#RESPONSE FORMAT
{
  "continue": true/false
}
"""




parse_context_instructions_template = """
You are @{{name}}, a social media bot.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#CURRENT CHANNEL
{{channel}}

#TASK
Before responding to the user, you can access data from the social media platform to come up with a better response and link to relevant posts.
You have access to an API that can generate the summary based on these parameters: category, channel, keyword, search.
* category: Can be one of pre-defined categories 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* keyword: Can be any single keyword.
* search: Can be any search phrase to search for posts.
Your goal is not to continue the conversation, you must only come up with interesting parameters to call the API.
Your goal is to propose parameters to gain access to more data before responding.

#RESPONSE FORMAT
{
  "category": "...",
  "keyword": "...",
  "search": "..."
}
"""

parse_context_schema = {
  "type":"OBJECT",
  "properties":{
    "category":{"type":"STRING"},
    "keyword":{"type":"STRING"},
    "search":{"type":"STRING"}
  }
}


class Chat(IActionStep):
    
  def get_cost(self):
    return 20
    
  def parse(self):
    parse_prompt = self.state.format(conversation_and_request_template)
    parse_instructions = self.state.format(preprocessing_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_context_schema)
    parsed = {
      'continue': read_boolean(params, key='continue')
    }
    self.state.action_params = parsed

  def execute(self):
    casts = []
    check_casts(casts)
    self.state.casts = casts

  def get_casts(self):
    parse_prompt = self.state.format(conversation_and_request_template)
    parse_instructions = self.state.format(parse_context_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_context_schema)
    parsed = {}
    parsed['keyword'] = read_keyword(params)
    parsed['category'] = read_category(params)
    parsed['search'] = read_string(params, key='search', default=None, max_length=500)
    fid = self.state.fid_origin
    if fid is not None:
      print('We should get casts for user here...')