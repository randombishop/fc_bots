from bots.utils.prompts import instructions_and_request
from models.mistral import mistral


instructions = """
INSTRUCTIONS:
Map the query to one of the following actions and output a json representation of the action.


FUNCTIONS:
*run_sql*
runs a {sql} query
sql, text, required.

*pick_cast*
selects top post from {channel} over last {num_days} days by {criteria}
channel is an optional parameter and defaults to null
num_days is an optional parameter and defaults to 1  
criteria is free text and defaults to 'most interesting'

*digest_casts*
digests the last {num_days} casts/posts containing {keywords} from {channel}
num_days, integer, optional, defaults to 1  
keywords, comma separated list of keywords, optional, defaults to null
channel, string, optional, defaults to null

*favorite_users*
Who are the favorite users of {username}
username, text or integer, required.


RESPONSE FORMAT:
{
  "function": "one of run_sql, pick_cast, digest_casts, favorite_users",
  "params": {...parameters inferred from user query...}
}
(if the user query does not match any of the functions, return a json with only the key "error" and the value "unknown function")

"""





if __name__ == "__main__":
  request = "Common followers between @jim, @joe and @dwr.eth"
  prompt = instructions_and_request(instructions, request)
  print(prompt)
  result = mistral(prompt)
  print(result)