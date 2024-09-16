
parse_user_examples = """
QUERY EXAMPLES:
* In query "Who are @alice.eth's favorite users?" -> the user is "alice.eth".
* In query "randombishop's wordcloud" -> the user is "randombishop".
* In query "Roast me!" -> the user is CURRENT USER ID indicated below.
* In query "Psychoanalysis of 328193" -> the user is 328193.
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