from bots.i_action_step import IActionStep
from bots.data.casts import get_more_like_this
from bots.utils.llms import call_llm


parse_instructions = """
You are @dsart bot, a social media bot.
Your task is to forward a text to an API that will perform a more-like-this search.
What text should we submit?
INSTRUCTIONS:
- Extract or come up with an appropriate text to be submitted to the more-like-this API.
- Your goal is not to continue the conversation, you must only extract a text to call the next API.


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

  def set_input(self, input):
    params = call_llm(input, parse_instructions, parse_schema)
    self.input = input
    self.set_params(params)

  def set_params(self, params):
    self.text = params['text']
    if self.text is None or len(self.text) < 5:
      raise Exception("This action requires some text to find similar posts.")

  def get_cost(self):
    self.cost = 20
    return self.cost

  def get_data(self):
    similar = get_more_like_this(self.text, limit=3)
    if len(similar) == 0:
      raise Exception("No similar posts found.")
    data = similar.to_dict(orient='records')
    self.data = data
    return self.data

  def get_casts(self, intro=''):
    casts = []
    for similar in self.data:
      casts.append({'text': '', 'embeds': [{'fid': similar['fid'], 'user_name': similar['user_name'], 'hash': similar['hash']}]})
    self.casts = casts
    return self.casts
