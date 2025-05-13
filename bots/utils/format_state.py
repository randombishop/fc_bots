import re
from bots.utils.format_cast import format_casts


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
    ans += f"#CONVERSATION\n{conversation}\n\n"
  if request is not None and len(request)>0:
    ans += f"#INSTRUCTIONS\n{request}\n\n"
  return ans


def format_state(state, intro=False, variables=False):
    ans = ''
    if intro:
      ans = f'You are @{state.bot_name} bot, a social media bot.\n'
    if variables:
      ans += 'Here are the variables in your internal state, followed by your instructions.\n\n'
      for variable in state.variables.values():
        variable_type = variable.value.__class__.__name__
        ans += f"#{variable.name} ({variable_type}) -> {variable.description}\n"
        ans += f"{variable.value}\n\n"
      ans += '\n\n'
    channel = state.get_variable('current_channel')
    if channel is not None:
      ans += f"#CURRENT CHANNEL\n/{channel.value}\n\n"
    conversation = state.get_variable('conversation')
    if conversation is not None and len(conversation.value.conversation)>0:
      ans += f"#CONVERSATION\n{conversation.value.conversation}\n"
    request = state.request
    if request is not None and len(request)>0:
      ans += f"#INSTRUCTIONS\n{request}\n"
    return ans


def format_todo(state):
  if state.todo is None:
    return ''
  todo = [f'{x["tool"]}.{x["method"]}' for x in state.todo]
  return '\n'.join(todo)
  
  
def debug_state(state):
  ans = "-"*64
  ans += "\n"
  ans += format_state(state, intro=False, variables=False)
  ans += "\n"
  variables = '\n'.join([str(v) for v in state.variables.values()])
  ans += f"#VARIABLES\n{variables}"
  if state.casts is not None and len(state.casts)>0:
    ans += "\n\n"
    ans += ">>> OUTPUT CASTS >>>\n"
    ans += format_casts(state.casts)
  ans += "\n"
  ans += "-"*64
  return ans
  
  