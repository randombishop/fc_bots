from dotenv import load_dotenv
load_dotenv()
import sys
import time
from bots.iaction import IAction
from bots.data.casts import get_cast
from bots.data.users import get_username
from bots.utils.llms import call_llm
from bots.utils.check_casts import check_casts

instructions = """
You are @dsart bot.
You are programmed to perform the following actions:
- Make a summary
- Pick a post
- Search with More-Like-This
- Find favorite accounts
- List most active users in a channel
- Make a word cloud
- Roast (or psycho-analyze) a user

INSTRUCTIONS:
Given the provided conversation, it seems like none of your programmed capabilities could be parsed.
You are entering Chat mode and need to decide what to do next.
- If it's a greeting or a thank you message, set "like" to true and "continue_conversation" to false. 
- If it makes sense to point the user to one of your capabilities, set "continue_conversation" to true and generate a short sentence to suggest using one of your programmed actions.
- Otherwise, set continue_conversation to false. 

OUTPUT FORMAT:
{
  "continue_conversation": true/false,
  "like": true/false,
  "sentence": "short sentence, about 20 words max"
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "continue_conversation":{"type":"BOOLEAN"},
    "like":{"type":"BOOLEAN"},
    "sentence":{"type":"STRING"}
  }
}




class Chat(IAction):
  
  def set_input(self, input):
    self.input = input

  def get_cost(self):
    self.cost = 1
    return self.cost

  def get_data(self):
    context = []
    context.append({'text': '@dsart ' + self.input, 'fid': self.fid_origin})
    parent_hash = self.parent_hash
    max_depth = 7
    current_depth = 0
    while parent_hash is not None and current_depth < max_depth:
      cast = get_cast(parent_hash)
      context.append({'text': cast['text'], 'fid': cast['fid']})
      parent_hash = cast['parent_hash']
      current_depth += 1
    context.reverse()
    fids = list(set(item['fid'] for item in context))
    fids = [x for x in fids if x is not None]
    if len(fids) > 0:
      usernames = {}
      for fid in fids:
        usernames[fid] = get_username(fid)
      for item in context:
        item['username'] = '@' +usernames[item['fid']] if usernames[item['fid']] is not None else '#' + str(item['fid'])
    for item in context:
      if 'username' not in item:
        item['username'] = 'anonymous'
    self.data = context
    return self.data
    
  def get_casts(self, intro=''):
    text = "CONVERSATION:\n\n"
    for item in self.data:
      text += f"--- {item['username']} ---\n {item['text']}\n\n"
    result = call_llm(instructions, text, schema)
    continue_conversation = 'continue_conversation' in result and str(result['continue_conversation']).lower()=='true'
    sentence = result['sentence'] if 'sentence' in result and len(result['sentence'])>0 else None
    like = 'like' in result and str(result['like']).lower()=='true'
    print(f"continue_conversation={continue_conversation}, like={like}, sentence={sentence}")
    if continue_conversation and sentence is not None:
      cast = {'text': sentence}
      casts = [cast]
      check_casts(casts)
      self.casts = casts
      return casts
    else:
      return []

if __name__ == "__main__":
  input = sys.argv[1]
  fid_origin = int(sys.argv[2])
  parent_hash = sys.argv[3]
  action = Chat()
  action.set_fid_origin(fid_origin)
  action.set_parent_hash(parent_hash)
  action.set_input(input)
  action.run()
  action.print()
