import re
from bots.utils.format_cast import insert_mentions, shorten_text


class State:
  
  def __init__(self):
    self.character = None
    self.tools_log = []
    self.next_tool = None
    self.tools_done =  False
    self.composed = False
    self.checked = False
    self.memorized = False
    self.posts_map = {}
  
  def get(self, key):
    for step in reversed(self.tools_log):
      tool_result = step[1]
      if key in tool_result:
        return tool_result[key]
    return None
  
  def add_posts(self, posts):
    for x in posts:
      self.posts_map[x['id']] = x
          
  def format_casts(self):
    casts = self.casts
    if casts is None or len(casts)==0:
      return ''
    ans = ''
    for c in casts:
      text = c['text']
      if 'mentions_ats' in c and 'mentions_pos' in c:
        text = insert_mentions(text, c['mentions_ats'], c['mentions_pos'])
      ans += f"> {text}"
      if 'embeds' in c and c['embeds'] is not None and len(c['embeds'])>0:
        embed = c['embeds'][0]
        description = c['embeds_description'] if 'embeds_description' in c else None
        description = shorten_text(description)
        if 'user_name' in embed and 'hash' in embed:
          ans += f" [{description}](https://warpcast.com/{embed['user_name']}/{embed['hash'][:10]})"
        else:
          ans += f" [{description}]({embed})"
      ans += '\n'
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
    conversation = self.get('conversation')
    request = self.get('request')
    ans = ''
    if conversation is not None and len(conversation)>0:
      ans += f"#CONVERSATION\n{conversation}\n"
    if request is not None and len(request)>0:
      ans += f"#INSTRUCTIONS\n{request}\n"
    return ans

  def format_all(self):
    ans = '#TOOL OUTPUTS\n\n'
    for x in self.tools_log:
      step = x[0]
      observation = x[1]
      ans += f"##{step.tool}\n"
      for k,v in observation.items():
        if v is not None and isinstance(v, str):
          ans += f"###{k}\n"
          ans += f"{v}\n\n"
    ans += '\n\n'
    ans += '#INSTRUCTIONS\n\n'
    ans += self.get('request')
    return ans
    
  def format_tools_log(self):
    ans = '#TOOL EXECUTION LOG\n\n'
    for x in self.tools_log:
      step = x[0]
      observation = x[1]
      ans += f"##{step.tool}\n"
      for k,v in observation.items():
        if v is not None and isinstance(v, str):
          if len(v) > 512:
            v = v[:512] + '...'
          ans += f"{k}: {v}\n"
    ans += '\n\n'
    ans += '#INSTRUCTIONS\n\n'
    ans += self.get('request')
    return ans
  
  def debug(self):
    try:
      pass
    except Exception as e:
      print('Exception in state.debug():', e)
