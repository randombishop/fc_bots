import re
from bots.data.channels import get_channel_by_url


def include_in_log(v):
  return (isinstance(v, str) and len(v) > 0) or isinstance(v,int) or isinstance(v,float) or isinstance(v,bool)

class State:
  
  def __init__(self):
    self.character = None
    self.tools_log = []
    self.posts_map = {}
  
  def get(self, key):
    for step in reversed(self.tools_log):
      tool_result = step[1]
      if key in tool_result:
        return tool_result[key]
    return None
  
  def get_current_channel(self):
    channel = self.get('channel')
    if channel is None:
      channel = self.get('root_parent_url')
      if channel is not None:
        channel = get_channel_by_url(channel)
    return channel

  def add_posts(self, posts):
    for x in posts:
      self.posts_map[x['id']] = x
  
  def get_available_data(self):
    ans = {}
    for x in self.tools_log:
      observation = x[1]
      for k,v in observation.items():
        if v is not None:
          ans[k] = v
    return ans
  
  def format(self, template):
    result = template
    placeholders = re.findall(r'\{\{(\w+)\}\}', template)
    for placeholder in placeholders:
      value = self.get(placeholder)
      if value is None:
        raise Exception(f"Placeholder {placeholder} not found in state")
      result = result.replace('{{' + placeholder + '}}', value)
    return result
  
  def format_conversation(self):
    channel = self.get_current_channel()
    conversation = self.get('conversation')
    request = self.get('request')
    ans = ''
    if channel is not None:
      ans += f"#CURRENT CHANNEL\n/{channel}\n\n"
    if conversation is not None and len(conversation)>0:
      ans += f"#CONVERSATION\n{conversation}\n"
    if request is not None and len(request)>0:
      ans += f"#INSTRUCTIONS\n{request}\n"
    return ans

  def format_all(self, succint=False):
    skip_tools = [
      'InitState', 
      'GetBio', 
      'GetLore', 
      'GetStyle', 
      'GetTime', 
      'GetConversation', 
      'ShouldContinue',
      'Like',
      'Preload',
      'Parse',
      'Fetch',
      'Prepare',
      'Check'
      ]
    name = self.get('name')
    ans = f'You are @{name} bot, a social media bot.\n'
    ans += 'Here is your log of the internal tools you executed, followed by your instructions.\n\n'
    ans += '#TOOL OUTPUTS\n\n'
    for x in self.tools_log:
      step = x[0]
      if step.tool not in skip_tools:
        observation = x[1]
        ans += f"##{step.tool}\n\n"
        for k,v in observation.items():
          if v is not None and include_in_log(v):
            ans += f"###{k}\n"
            v = str(v)
            if succint and len(v) > 256:
              v = v[:256] + '...\n'
              v += f'(text length: {len(v)}. Data truncated to focus on current task.)'
            ans += f"{v}\n\n"
    ans += '\n\n'
    channel = self.get_current_channel()
    if channel is not None:
      ans += f"#CURRENT CHANNEL\n/{channel}\n\n"
    conversation = self.get('conversation')
    if conversation is not None and len(conversation)>0:
      ans += f"#CONVERSATION\n{conversation}\n"
    request = self.get('request')
    if request is not None and len(request)>0:
      ans += f"#INSTRUCTIONS\n{request}\n"
    return ans
      
  def get_tools_sequence(self):
    return [x[0].tool for x in self.tools_log]
    
  def debug(self):
    try:
      s = '-'*100+'\n'
      s += ' > '.join(self.get_tools_sequence())+' >>> \n'
      casts = self.get('casts')
      if casts is not None and len(casts)>0:
        s += casts
      s += '-'*100+'\n'
      print(s)
    except Exception as e:
      print('Exception in state.debug():', e)
