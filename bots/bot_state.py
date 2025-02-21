import re
from bots.data.users import get_username
from bots.utils.format_cast import insert_mentions, shorten_text


DEFAULT_TEMPLATE = """
#NAME
{{name}}

#ACTIONS
{{actions}}

#ACTIONS TEMPLATES
{{actions_templates}}

#REQUEST
{{request}}

#PARAMS
fid_origin={{fid_origin}}, parent_hash={{parent_hash}}, attachment_hash={{attachment_hash}}, root_parent_url={{root_parent_url}}

#BIO
{{bio}}

#LORE
{{lore}}

#STYLE
{{style}}

#TRENDING POSTS
{{trending}}

#RECENT POSTS
{{bot_casts}}

#SELECTED CHANNEL
{{selected_channel}}

#CONVERSATION
{{conversation}}

#TIME
{{time}}

#SELECTED ACTION
{{selected_action}}
"""



CONVERSATION_AND_REQUEST_TEMPLATE = """
#CONVERSATION
{{conversation}}

#REQUEST
{{request}}
"""


class BotState:
  
  def __init__(self, id=None, name=None, 
               request=None, 
               fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None,
               selected_channel=None, selected_action=None):
    # 1. Initialization
    self.id = id
    self.name = name
    self.request = request
    self.fid_origin = int(fid_origin) if fid_origin is not None else None
    self.user_origin = get_username(self.fid_origin) if self.fid_origin is not None else None
    self.parent_hash = parent_hash
    self.attachment_hash = attachment_hash
    self.root_parent_url = root_parent_url
    self.log = ''
    # 2. Wake up
    self.actions = ''
    self.actions_templates = ''
    self.bio = ''
    self.cast_stats = ''
    self.channel = selected_channel
    self.channel_list = ''
    self.conversation = ''
    self.lore = ''
    self.style = ''
    self.time = ''
    # 3. Plan
    self.selected_channel = selected_channel
    self.selected_channel_df = None
    self.selected_channel_reasoning = None
    self.selected_channel_log = None
    self.selected_action = selected_action
    # 4. Prepare 
    self.should_continue = True
    self.trending = ''
    self.user = None
    self.user_casts = None
    self.about_user = None
    self.user_display_name = None
    self.user_bio = None
    self.user_pfp_url = None
    self.user_pfp_description = None
    self.user_avatar_prompt = None
    self.user_new_avatar = None
    self.keyword = None
    self.about_keyword = None
    self.topic = None
    self.about_topic = None
    self.context = None
    self.about_context = None
    self.posts_map = {}
    self.casts_in_channel = None
    self.bot_casts = None
    self.bot_casts_in_channel = None
    self.bot_casts_no_channel = None
    # 5. Execute actions
    self.cost = 0
    self.action_params = None
    self.casts = []
    # 6. Think
    self.like = False
    self.reply = False
    self.do_not_reply_reason = None
       
  def set(self, key, value):
    if hasattr(self, key):
      setattr(self, key, value)
    else:
      raise ValueError(f"Invalid field: {key}")
  
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
      if 'embeds_description' in c and c['embeds_description'] is not None:
        description = c['embeds_description']
        description = shorten_text(description)
        ans += f" (embedded link: {description})"
      ans += '\n'
    return ans
  
  def format_casts2(self):
    casts = self.casts
    if casts is None or len(casts)==0:
      return ''
    ans = ''
    for c in casts:
      text = c['text']
      if 'mentions_ats' in c and 'mentions_pos' in c:
        text = insert_mentions(text, c['mentions_ats'], c['mentions_pos'])
      ans += f"{text}"
      if 'embeds' in c and c['embeds'] is not None and len(c['embeds'])>0:
        description = c['embeds_description'] if 'embeds_description' in c else None
        description = shorten_text(description)
        embed = c['embeds'][0]
        if 'user_name' in embed and 'hash' in embed:
          ans += f" [{description}](https://warpcast.com/{embed['user_name']}/{embed['hash'][:10]})"
        else:
          ans += f" [{description}]({embed})"
      ans += '\n'
    return ans
  
  def format(self, template=DEFAULT_TEMPLATE):
    result = template
    placeholders = re.findall(r'\{\{(\w+)\}\}', template)
    for placeholder in placeholders:
      value = self.format_placeholder(placeholder)
      result = result.replace('{{' + placeholder + '}}', value)
    return result
  
  def format_conversation(self):
    return self.format(CONVERSATION_AND_REQUEST_TEMPLATE)
  
  def debug(self):
    try:
      s = ('-'*128) + '\n'
      # Request
      if self.conversation is not None and len(self.conversation)>0:
        s += self.conversation + '\n'
      # Selected action
      if self.selected_action is None:
        s += '## No action was selected ##\n'
      else:  
        s += f"## {self.selected_action} ##\n"
      # Action parameters
      if self.action_params is not None:
        attrs = ['fid', 'user_name', 'channel', 'keyword', 'category', 'search', 'criteria', 'text', 'question', 'continue']
        for attr in attrs:
          if attr in self.action_params and self.action_params[attr] is not None: 
            s += f"<< {attr} << {self.action_params[attr]}\n"
      else:
        s += '<< No parameters were parsed <<\n'
      # Casts
      if self.casts is not None and len(self.casts)>0: 
        s += ">> casts >>\n"
        s += self.format_casts2()
      # Logs
      if self.log is not None and len(self.log)>0:
        s += f"-- logs --\n"
        s += self.log + "\n"
      # End
      s += ('-'*128) + '\n'
      print(s)
    except Exception as e:
      print('Exception in state.debug():', e)
