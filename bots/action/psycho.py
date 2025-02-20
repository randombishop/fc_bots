from bots.i_action_step import IActionStep
from bots.data.casts import get_casts_for_fid
from bots.utils.llms import call_llm
from bots.utils.read_params import read_user


parse_user_instructions_template = """
#INSTRUCTIONS:
You are @{{name}}, a bot programmed to psycho analyze a user.
Based on the provided conversation, who should we psycho analyze?
Your goal is not to continue the conversation, you must only extract the user parameter from the conversation so that we can call an API.
Users typically start with @, but not always.
If the request is about self, this or that user, or uses a pronoun, study the conversation carefully to figure out the intended user.

#RESPONSE FORMAT:
{
  "user": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


instructions_template = """
#TASK
You are @{{name}}, an eccentric, witty psychoanalyst with a flair for humor and satire.
Your task is to generate a parody psycho analysis of @{{user_name}}.

#INSTRUCTIONS:
The posts provided are from @{{user_name}}.
Based on the posts, provide a hilariously original psychoanalysis of @{{user_name}}'s personality in 3 sentences.
Do not use real pathology names, instead, create your own funny medical names with novel issues.
You can mix your psycho analysis with roasting.
Examine the recurring themes and word choices and explain their subconscious motivations in a playful, tongue-in-cheek manner. 
Imagine a blend of Freudian insights and stand-up comedy.
Remember to be creative, original, and thoroughly entertaining but always remain respectful.
Be respectful, and do not use sexual, religious or political references.
Output the result in json format.
Make sure you don't use " inside json strings. Avoid invalid json.
Output 3 sentences in json format.

#RESPONSE FORMAT:
{
  "sentence1": "...",
  "sentence2": "...",
  "sentence3": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "sentence1":{"type":"STRING"},
    "sentence2":{"type":"STRING"},
    "sentence3":{"type":"STRING"}
  }
}

class Psycho(IActionStep):
    
  def get_cost(self):
    return 20
    
  def parse(self):
    parse_prompt = self.state.format_conversation()
    parse_instructions = self.state.format(parse_user_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_user_schema)
    parsed = {}
    fid, user_name = read_user(params, self.state.fid_origin, default_to_origin=True)
    parsed['fid'] = fid
    parsed['user_name'] = user_name
    self.state.action_params = parsed
    self.state.user = user_name

  def execute(self):
    fid = self.state.action_params['fid']
    if fid is None:
      raise Exception(f"No fid provided.")
    df = get_casts_for_fid(fid)
    if df is None or len(df) == 0:
      raise Exception(f"Not enough activity to buid a psychodegen analysis.")
    data = list(df['text'])
    text = "\n".join([str(x) for x in data])
    instructions = self.state.format(instructions_template.replace('{{user_name}}', self.state.action_params['user_name']))
    result = call_llm(text, instructions, schema)
    casts = []
    if 'sentence1' in result:
      casts.append({'text': result['sentence1']})
    if 'sentence2' in result:
      casts.append({'text': result['sentence2']})
    if 'sentence3' in result:
      casts.append({'text': result['sentence3']})
    self.state.casts = casts
