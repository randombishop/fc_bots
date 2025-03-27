import re
from bots.utils.format_cast import insert_mentions, shorten_text


class State:
  
  def __init__(self):
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
      
  def format_placeholder(self, key):
    if not hasattr(self, key):
      raise ValueError(f"Invalid key: {key}")
    if key == 'casts':
      return self.format_casts()
    else:
      value = getattr(self, key)
      if value is None:
        value = ''
      return value
    
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
      value = self.format_placeholder(placeholder)
      result = result.replace('{{' + placeholder + '}}', value)
    return result
  
  def format_all(self):
    return ''
  
  def format_prompt(self):
    if self.is_responding():
      return self.format_conversation()
    else:
      return self.format_instructions()
  
  def format_conversation(self):
    ans = ''
    if self.conversation is not None and len(self.conversation)>0:
      ans += f"#CONVERSATION\n{self.conversation}\n"
    if self.request is not None and len(self.request)>0:
      ans += f"#INSTRUCTIONS\n{self.request}\n"
    return ans

  def format_instructions(self):
    ans = ''
    if self.trending is not None and len(self.trending)>0:
      ans += f"#WHAT IS TRENDING IN GENERAL (NOT SPECIFIC TO THE CHANNEL)\n{self.trending}\n"
    if self.casts_in_channel is not None and len(self.casts_in_channel)>0:
      ans += f"#RECENT POSTS IN THE CHANNEL\n{self.casts_in_channel}\n"
    if self.bot_casts_in_channel is not None and len(self.bot_casts_in_channel)>0:
      ans += f"#WHAT YOU RECENTLY POSTED IN THE CHANNEL\n{self.bot_casts_in_channel}\n"
    if self.instructions is not None and len(self.instructions)>0:
      ans += f"#INSTRUCTIONS\n{self.instructions}\n"
    return ans

  def format_all_available_data(self):
    tmp = """
    You are @{{name}}, a social media bot.

    #YOUR BIO
    {{bio}}

    #YOUR LORE
    {{lore}}

    #YOUR STYLE
    {{style}}

    #CURRENT CHANNEL
    {{root_parent_url}}

    #CURRENT TIME
    {{time}}
    """
    ans = ''
    if self.trending is not None and len(self.trending)>0:
      ans += f"#WHAT IS TRENDING IN GENERAL (NOT SPECIFIC TO THE CHANNEL)\n{self.trending}\n"
    if self.casts_in_channel is not None and len(self.casts_in_channel)>0:
      ans += f"#RECENT POSTS IN THE CHANNEL\n{self.casts_in_channel}\n"
    if self.bot_casts_in_channel is not None and len(self.bot_casts_in_channel)>0:
      ans += f"#WHAT YOU RECENTLY POSTED IN THE CHANNEL\n{self.bot_casts_in_channel}\n"
    if self.casts is not None and len(self.casts)>0:
      ans += f"#CANDIDATE POSTS GENERATED SO FAR USING ACTION {self.action}\n{self.format_casts()}\n"
    if self.instructions is not None and len(self.instructions)>0:
      ans += f"#INSTRUCTIONS\n{self.instructions}\n"
    return ans
  
  def format_tools_log(self):
    ans = '#TOOL EXECUTION LOG\n\n'
    for x in self.tools_log:
      step = x[0]
      observation = x[1]
      ans += f"##{step.tool}\n"
      ans += f"{observation}\n\n"
    ans += '\n\n'
    ans += '#CURRENT PARAMETERS\n'
    ans += f"user: {self.user}\n"
    ans += f"user_fid: {self.user_fid}\n"
    ans += f"channel: {self.channel}\n"
    ans += f"channel_url: {self.channel_url}\n"
    ans += f"keyword: {self.keyword}\n"
    ans += f"category: {self.category}\n"
    ans += f"search: {self.search}\n"
    ans += f"text: {self.text}\n"
    ans += f"question: {self.question}\n"
    ans += f"criteria: {self.criteria}\n"
    ans += '\n\n'
    ans += '#INSTRUCTIONS\n\n'
    ans += self.instructions
    return ans
  
  def format_observations(self):
    ans = ''
    for x in self.tools_log:
      step = x[0]
      observation = x[1]
      if step.tool != 'SelectTool':  
        ans += f"#Outputs using tool {step.tool}:\n"
        for k,v in observation.items():
          ans += f"##{k}:\n"
          ans += f"{v}\n\n"
        ans += '\n\n'
    return ans
  
  def debug(self):
    try:
      s = ('-'*128) + '\n'
      # Conversation
      if self.conversation is not None and len(self.conversation)>0:
        s += self.conversation + '\n'
      # Instructions
      if self.instructions is not None and len(self.instructions)>0:
        s += self.instructions + '\n'
      # Selected action
      if self.action is not None:
        s += f"## {self.action} ##\n"
      # Casts
      if self.casts is not None and len(self.casts)>0: 
        s += ">> casts >>\n"
        s += self.format_casts()
      # End
      s += ('-'*128) + '\n'
      print(s)
    except Exception as e:
      print('Exception in state.debug():', e)
