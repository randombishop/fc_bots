

def instructions_and_request(instructions, request):
  prompt = instructions
  prompt += '\n\n'
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