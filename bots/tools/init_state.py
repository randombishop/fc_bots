from langchain.agents import Tool
from langsmith import traceable
from bots.kit_interface.variable import Variable
from bots.kit_interface.time import Time
from bots.kit_interface.bio import Bio
from bots.kit_interface.lore import Lore
from bots.kit_interface.style import Style
from bots.kit_interface.channel_id import ChannelId
from bots.kit_interface.conversation import Conversation
from bots.kit_interface.user_id import UserId
from bots.data.app import get_bot_character
from bots.data.users import get_username, get_fid
from bots.data.channels import get_channel_url
from bots.data.channels import get_channel_by_url
from bots.data.neynar import get_cast_info
from bots.data.users import get_username
from bots.kit_blueprints.blueprints import BLUEPRINTS
from bots.utils.llms2 import get_max_capactity
from bots.utils.should_continue import should_continue
from bots.utils.like import like


@traceable(run_type='parser')
def init_time(state):
  var = Variable('time', 'The current time', Time())
  state.set_variable(var)
  return var


@traceable(run_type='parser')
def init_bio(state):
  character = state.character
  if character is None or character['bio'] is None or len(character['bio']) == 0:
    return None
  else:
    var = Variable('bio', 'Your bio', Bio(character['bio']))
    state.set_variable(var)
    return var

@traceable(run_type='parser')
def init_lore(state):
  character = state.character
  if character is None or character['lore'] is None or len(character['lore']) == 0:
    return None
  else:
    var = Variable('lore', 'Your lore', Lore(character['lore']))
    state.set_variable(var)
    return var

@traceable(run_type='parser')
def init_style(state):
  character = state.character
  if character is None or character['style'] is None or len(character['style']) == 0:
    return None
  else:
    var = Variable('style', 'Your style', Style(character['style']))
    state.set_variable(var)
    return var

max_depth = 28
@traceable(run_type='parser')
def init_conversation(state):
  fid_origin = state.fid_origin
  request = state.request
  attachment_hash = state.attachment_hash
  parent_hash = state.parent_hash
  context = []
  username_origin = get_username(fid_origin) if fid_origin is not None else 'unknown_user'
  if request is not None or attachment_hash is not None:
    main_cast = {
      'text': request if request is not None else '', 
      'fid': fid_origin, 
      'username': username_origin, 
      'when': 'now'
    }
    if attachment_hash is not None:
      attachment_cast = get_cast_info(attachment_hash)
      if attachment_cast is not None:
        main_cast['quote'] = {'text': attachment_cast['text'], 'fid': attachment_cast['fid'], 'username': attachment_cast['username']}
    context.append(main_cast)
  current_depth = 0
  while parent_hash is not None and current_depth < max_depth:
    previous_cast = None
    try:
      previous_cast = get_cast_info(parent_hash)
    except:
      pass
    if previous_cast is not None:
      context.append(previous_cast)
      parent_hash = previous_cast['parent_hash']
      current_depth += 1
    else:
      parent_hash = None
  context.reverse()
  if len(context) > 0:
    text = ''
    for i in range(len(context)):
      item = context[i]
      text += f"#{i+1}. @{item['username']} said {item['when']}: \n"
      text += f"{item['text']} \n"  
      if 'quote' in item:
        if 'username' in item['quote']:
          text += f"  [quoting @{item['quote']['username']}: \n"
          text += f"  {item['quote']['text']} \n"
          text += "  ]\n"
        elif 'url' in item['quote']:
          text += f"  [{item['quote']['url']}]\n"
      text += '#'
    var = Variable('conversation', "The context's conversation", Conversation(text))
    state.set_variable(var)
    return var
  
  
@traceable(run_type='parser')
def init_should_continue(state):
  bot_id = state.bot_id
  bot_name = state.bot_name
  channel = state.get_variable('current_channel')
  if channel is not None:
    channel = channel.value.channel_id
  conversation = state.get_variable('conversation')
  if conversation is not None:
    conversation = conversation.value.conversation
  request = state.request
  state.should_continue = should_continue(bot_id, bot_name, channel, conversation, request)
  return state.should_continue


@traceable(run_type='parser')
def init_like(state):
  bot_id = state.bot_id
  bot_name = state.bot_name
  bio = state.get_variable('bio')
  if bio is not None:
    bio = bio.value
  lore = state.get_variable('lore')
  if lore is not None:
    lore = lore.value
  conversation = state.get_variable('conversation')
  if conversation is not None:
    conversation = conversation.value.conversation
  request = state.request
  state.like = like(bot_id, bot_name, bio, lore, conversation, request)
  return state.like


def initialize_state(input):    
  state = input['state']
  # bot_id
  bot_id = input['bot_id']
  state.bot_id = bot_id
  # character
  character = get_bot_character(bot_id)
  if character is None:
    raise Exception(f"Bot {id} not found")
  state.character = character
  # name
  state.bot_name = character['name']
  # mode
  mode = input['mode']
  if mode not in ['assistant', 'bot', 'blueprint']:
    raise Exception(f"Invalid mode `{mode}`. should be assistant, bot or blueprint")
  state.mode = mode
  # request
  if 'request' in input and input['request'] is not None:
    state.request = input['request']
  # fid_origin
  if 'fid_origin' in input and input['fid_origin'] is not None:
    state.fid_origin = int(input['fid_origin'])
    user_origin = get_username(state.fid_origin)
    if user_origin is not None:
      user_origin_var = Variable('user_origin', 'The user id who submitted the request', UserId(state.fid_origin, user_origin))
      state.set_variable(user_origin_var)
  # parent_hash
  if 'parent_hash' in input and input['parent_hash'] is not None:
    state.parent_hash = input['parent_hash']
  # attachment_hash
  if 'attachment_hash' in input and input['attachment_hash'] is not None:
    state.attachment_hash = input['attachment_hash']
  # root_parent_url
  if 'root_parent_url' in input and input['root_parent_url'] is not None:
    state.root_parent_url = input['root_parent_url']
    current_channel_id = get_channel_by_url(state.root_parent_url)
    if current_channel_id is not None:
      current_channel_var = Variable('current_channel', 'The current channel where the conversation is happening', ChannelId(current_channel_id, state.root_parent_url))
      state.set_variable(current_channel_var)
  # user
  if 'user' in input and input['user'] is not None:
    user_name = input['user']
    user_fid = get_fid(user_name)
    if user_fid is not None and user_name is not None:
      user_var = Variable('selected_user', 'The selected user for this request', UserId(user_fid, user_name))
      state.set_variable(user_var)
  # channel
  if 'channel' in input and input['channel'] is not None:
    channel = input['channel']
    channel_url = get_channel_url(channel)
    if channel_url is not None:
      channel_var = Variable('selected_channel', 'The selected channel for this request', ChannelId(channel, channel_url))
      state.set_variable(channel_var)
  # blueprint
  if 'blueprint' in input and input['blueprint'] is not None:
    blueprint = input['blueprint']
    if isinstance(blueprint, list):
      state.blueprint = input['blueprint']
    elif isinstance(blueprint, str):
      if blueprint in BLUEPRINTS:
        state.blueprint = BLUEPRINTS[blueprint]
      else:
        raise Exception(f"Invalid blueprint `{blueprint}`")
    else:
      raise Exception(f"Invalid blueprint. Should be a list or a string")
    state.todo = state.blueprint.copy()
  # should_continue
  state.should_continue = True
  # max_rows
  state.max_rows = get_max_capactity()
  # mode specific initialization
  init_time(state)
  init_bio(state)
  init_lore(state)
  init_style(state)
  init_conversation(state)
  if state.mode == 'bot':
    init_should_continue(state)
    init_like(state)
  return [str(v) for v in state.variables.values()]
  

init_state = Tool(
  name="init_state",
  func=initialize_state,
  description="Initialize the state of the bot."
)