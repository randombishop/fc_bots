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
INSTRUCTIONS:
You are @dsart bot.
Continue the conversation by generating one short sentence.
You are encouraged to be creative, funny and use random emojis.
If you are not sure what to say, just recommend a visit to app.datascience.art. 

OUTPUT FORMAT:
{
  "sentence1": "short sentence, about 20 words max"
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "sentence1":{"type":"STRING"}
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
    while parent_hash is not None:
      cast = get_cast(parent_hash)
      context.append({'text': cast['text'], 'fid': cast['fid']})
      parent_hash = cast['parent_hash']
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
    cast = {'text': result['sentence1']}
    casts = [cast]
    check_casts(casts)
    self.casts = casts
    return casts

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
