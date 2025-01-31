from bots.i_action_step import IActionStep
from bots.prompts.contexts import conversation_and_request_template
from bots.data.casts import get_more_like_this
from bots.utils.llms import call_llm


parse_instructions_template = """
You are @{{name}}, a social media bot.
Your task is to forward a text to an API that will perform a more-like-this search.
What text should we submit?
Extract or come up with an appropriate text to be submitted to the more-like-this API.
Your goal is not to continue the conversation, you must only extract a text to call the next API.
You can use the conversation for more context if needed, but focus on the request to find out the intent of the last user.

OUTPUT FORMAT:
{
  "text": "..."
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "text":{"type":"STRING"}
  }
}

class MoreLikeThis(IActionStep):

  def get_cost(self):
    return 20

  def parse(self):
    parse_prompt = self.state.format(conversation_and_request_template)
    parse_instructions = self.state.format(parse_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_schema)
    text = params['text']
    if text is None or len(text) < 5:
      raise Exception("This action requires some text to find similar posts.")
    self.state.action_params = {'text': text}

  def execute(self):
    similar = get_more_like_this(self.state.action_params['text'], limit=3)
    if len(similar) == 0:
      raise Exception("No similar posts found.")
    data = similar.to_dict(orient='records')
    casts = []
    for similar in data:
      casts.append({
        'text': '', 
        'embeds': [{'fid': similar['fid'], 'user_name': similar['user_name'], 'hash': similar['hash']}],
        'q_distance': similar['q_distance'],
        'dim_distance': similar['dim_distance']
      })
    self.state.casts = casts
