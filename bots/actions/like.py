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
You are @dsart bot, a social media bot.
Your task is to decide if the last post in the provided conversation is worth liking.

INSTRUCTIONS:
- If it's a greeting or a thank you message, set "like" to true. 
- If it's a positive message, nice or interesting feedback about the conversation, set "like" to true.  
- Otherwise, set "like" to false.

OUTPUT FORMAT:
{
  "like": true/false
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "like":{"type":"BOOLEAN"}
  }
}




class Like(IAction):
  
  def set_input(self, input):
    self.input = input

  def get_cost(self):
    self.cost = 1
    return self.cost

  def get_data(self):
    self.data = self.input
    return self.data
    
  def get_casts(self, intro=''):
    result = call_llm(instructions, self.data, schema)
    like = 'like' in result and str(result['like']).lower()=='true'
    if like:
      self.casts = [{'like': like}]
    else:
      self.casts =  []
    return self.casts
