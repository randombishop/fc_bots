
extract_user_prompt = """
INSTRUCTIONS:
Extract the user name or id from the query.
Your goal is not to answer the query, you only need to extract the user parameter from the query.
The query doesn't have to follow a specific format, you just need to extract what you think is most likely the user name or id.
If you're not sure, pick the first token that starts with a @.

QUERY EXAMPLES:
* In query "Who are @alice.eth's favorite users?" -> the user is "alice.eth".
* In query "randombishop's wordcloud" -> the user is "randombishop".
* In query "Roast me!" -> the user is CURRENT USER ID indicated below.
* In query "Psycho analyze 328193" -> the user is 328193.

RESPONSE FORMAT:
{{
  "user": ...
}}
(if you can not extract a user name or id, return a json with an error message)
"""


def instructions_and_request(instructions, request, fid_origin=None):
  prompt = instructions
  prompt += '\n\n'
  if fid_origin is not None:
    prompt += '\n\n'
    prompt += f"CURRENT USER ID: {fid_origin}"
  prompt += 'REQUEST:\n'
  prompt += request
  return prompt


def casts_and_instructions(posts, instructions):
  prompt = 'POSTS:\n'
  for post in posts:
    prompt += "\n"
    prompt += "<"+post['hash']+">\n"
    prompt += post['text']
    prompt += "\n</"+post['hash']+">\n"
  prompt += "\n"
  prompt += '\n\n'
  prompt += instructions
  return prompt