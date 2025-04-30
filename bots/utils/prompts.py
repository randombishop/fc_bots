import re


def format_template(template, variables):
  result = template
  placeholders = re.findall(r'\{\{(\w+)\}\}', template)
  for placeholder in placeholders:
    value = variables[placeholder]
    if value is None:
      raise Exception(f"Placeholder {placeholder} not found in state")
    result = result.replace('{{' + placeholder + '}}', str(value))
  return result
  

def format_conversation(channel, conversation, request):
  ans = ''
  if channel is not None:
    ans += f"#CURRENT CHANNEL\n/{channel}\n\n"
  if conversation is not None and len(conversation)>0:
    ans += f"#CONVERSATION\n{conversation}\n"
  if request is not None and len(request)>0:
    ans += f"#INSTRUCTIONS\n{request}\n"
  return ans
