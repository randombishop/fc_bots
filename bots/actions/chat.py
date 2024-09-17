from dotenv import load_dotenv
load_dotenv()
import sys
import uuid
import os
from bots.iaction import IAction
from bots.data.casts import get_cast
from bots.data.users import get_usernames
from bots.utils.prompts import instructions_and_request
from bots.utils.llms import call_llm
from bots.utils.check_casts import check_casts

instructions = """
INSTRUCTIONS:
You are @dsart bot.
Continue the conversation above by generating one short sentence.
You are encouraged to be creative, funny and use random emojis.
If you are not sure what to say, you can recommend to contact @randombishop. 

RESPONSE FORMAT:
{
  "sentence1": "short sentence, about 20 words max"
}
"""


class Chat(IAction):
  
  def parse(self, input, fid_origin=None, parent_hash=None):
    self.params = {'input': input, 'fid': fid_origin, 'parent_hash': parent_hash}

  def get_cost(self):
    self.cost = 0
    return self.cost

  def execute(self):
    context = []
    context.append({'text': '@dsart ' + self.params['input'], 'fid': self.params['fid']})
    parent_hash = self.params['parent_hash']
    while parent_hash is not None:
      cast = get_cast(parent_hash)
      context.append({'text': cast['text'], 'fid': cast['fid']})
      parent_hash = cast['parent_hash']
    context.reverse()
    fids = list(set(item['fid'] for item in context))
    print(fids)
    usernames = get_usernames(fids)
    print(usernames)
    for item in context:
      item['username'] = '@' +usernames[item['fid']] if item['fid'] in usernames else '#' + str(item['fid'])
    self.data = context
    return self.data
    
  def get_casts(self, intro=''):
    text = "CONVERSATION:\n\n"
    for item in self.data:
      text += f"--- {item['username']} ---\n {item['text']}\n\n"
    print(text)
    prompt = text + '\n\n' + instructions ;
    result = call_llm(prompt)
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
  action.parse(input, fid_origin=fid_origin, parent_hash=parent_hash)
  action.get_cost()
  action.execute()
  action.get_casts()
  print(f"Casts: {action.casts}")
