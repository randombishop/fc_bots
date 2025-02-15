from bots.bot_state import BotState
from bots.wakeup.wakeup_steps import WAKEUP_STEPS
from bots.prepare.prepare_steps import PREPARE_STEPS
from bots.action.action_steps import ACTION_STEPS
from bots.plan.select_channel import SelectChannel
from bots.plan.select_action import SelectAction
from bots.think.like import Like
from bots.think.reply import Reply
from bots.think.shorten import Shorten
from bots.data.app import get_bot_character

class Bot:
  
  def __init__(self, id, character):
    self.id = id
    self.character = character
    self.character['wakeup_steps'] += ['actions_templates','channel_list']
    self.state = BotState()
    
  def initialize(self, request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None, selected_action=None):
    self.state = BotState(
      id=self.id,
      name=self.character['name'], 
      request=request, 
      fid_origin=fid_origin, 
      parent_hash=parent_hash, 
      attachment_hash=attachment_hash, 
      root_parent_url=root_parent_url,
      selected_action=selected_action
    )

  def wakeup(self):
    wakeup_steps = self.character['wakeup_steps']
    for key in wakeup_steps:
      wakeup_step = WAKEUP_STEPS[key]()
      wakeup_value = wakeup_step.get(self.character, self.state)
      self.state.set(key, wakeup_value)

  def plan(self):
    if self.state.request is None and len(self.state.channel)==0:
      select_channel_step = SelectChannel(self.state)
      select_channel_step.plan()
    if self.state.selected_action is None:
      select_action_step = SelectAction(self.state)
      select_action_step.plan()
  
  def prepare(self):
    if self.state.selected_action is None:
      return
    Action = ACTION_STEPS[self.state.selected_action]
    action = Action(self.state)
    prepare_steps = action.get_prepare_steps()
    for step in prepare_steps:
      Prepare = PREPARE_STEPS[step]
      prepare_step = Prepare(self.state)
      prepare_step.prepare()
  
  def execute(self):
    if self.state.selected_action is None:
      return
    Action = ACTION_STEPS[self.state.selected_action]
    action = Action(self.state)
    action.parse()
    action.execute()
    self.state.cost += action.get_cost()
    
  def think(self):
    # Decide if we should like the post
    if self.state.request is not None:  
      like_step = Like(self.state)
      like_step.think()
    # Shorten the casts if needed
    if self.state.casts is not None and len(self.state.casts) > 0:
      shorten_step = Shorten(self.state)
      shorten_step.think()
    # Decide if we should reply
    if self.state.request is not None:
      reply_step = Reply(self.state)
      reply_step.think()
  
  def respond(self, request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None, selected_action=None):
    self.initialize(request, fid_origin, parent_hash, attachment_hash, root_parent_url, selected_action)
    self.wakeup()
    self.plan()
    self.prepare()
    self.execute()
    self.think()
    response = {
      'like': self.state.like,
      'reply': self.state.reply,
      'casts': self.state.casts,
      'cost': self.state.cost,
      'selected_action': self.state.selected_action,
      'selected_user': self.state.user
    }
    return response
  

def generate_bot_response(bot_id, request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None, selected_action=None):
  character = get_bot_character(bot_id)
  if character is None:
    raise Exception(f"Bot {bot_id} not found")
  bot = Bot(bot_id, character)
  response = bot.respond(request=request, 
                         fid_origin=fid_origin, 
                         parent_hash=parent_hash, 
                         attachment_hash=attachment_hash, 
                         root_parent_url=root_parent_url,
                         selected_action=selected_action)
  return response