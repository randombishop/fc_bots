import sys
import json
from bots.utils.prompts import instructions_and_request
from models.mistral import mistral


instructions = """
INSTRUCTIONS:
Map the query to one of the following actions and output a json representation of the action.


FUNCTIONS:
*run_sql*
runs a {sql} query
sql, text, required. 
Only read-only queries.
If the sql doesn't look like a read-only query, return an error in the json object.


*pick_cast*
selects top post from {channel} over last {num_days} days by {criteria}
channel is an optional parameter and defaults to null
num_days is an optional parameter and defaults to 1  
criteria is free text and defaults to 'most interesting'

*digest_casts*
Summarizes the last {num_days} casts/posts containing {keywords} from {channel}
num_days, integer, optional, defaults to 1  
keywords, comma separated list of keywords, optional, defaults to null
channel, string, optional, defaults to null

*favorite_users*
Who are the favorite users of {user}
user, text or integer, required. If the user is referencing themselves, then user=0

*most_active_users*
Lists the most active users in channel {channel} over the last {num_days} days
channel, text, required.
num_days, integer, optional, defaults to 1



RESPONSE FORMAT:
{
  "function": "one of run_sql, pick_cast, digest_casts, favorite_users",
  "params": {...parameters inferred from user query...}
}
(if the user query does not match any of the functions, return a json with "error": "can't map query to function")

"""


def parse(request):
  prompt = instructions_and_request(instructions, request)
  result_string = mistral(prompt)
  result = json.loads(result_string)
  if 'function' in result and result['function'] == 'run_sql':
    # avoid mistral hallucinating the sql
    result['params']['sql'] = request
  return result



if __name__ == "__main__":
  request = sys.argv[1]
  result = parse(request)
  print(result)