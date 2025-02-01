from bots.bot_state import BotState
from bots.wakeup.wakeup_steps import WAKEUP_STEPS
from bots.prepare.prepare_steps import PREPARE_STEPS
from bots.action.action_steps import ACTION_STEPS
from bots.prompts.action_plan import select_action_task, select_action_format, select_action_schema, select_action_prompt
from bots.utils.llms import call_llm

class Bot:
  
  def __init__(self, character):
    self.character = character
    self.state = BotState()
    
  def initialize(self, request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None):
    self.state = BotState(
      name=self.character['name'], 
      request=request, 
      fid_origin=fid_origin, 
      parent_hash=parent_hash, 
      attachment_hash=attachment_hash, 
      root_parent_url=root_parent_url
    )

  def wakeup(self):
    wakeup_steps = self.character['wakeup_steps']
    for key in wakeup_steps:
      wakeup_step = WAKEUP_STEPS[key]()
      wakeup_value = wakeup_step.get(self.character, self.state)
      self.state.set(key, wakeup_value)

  def plan(self):
    instructions = self.state.format(select_action_task)
    instructions += '\n'
    instructions += "#OUTPUT FORMAT\n"
    instructions += select_action_format
    prompt = self.state.format(select_action_prompt)
    result = call_llm(prompt, instructions, select_action_schema)
    if ('action' not in result or result['action'] is None or str(result['action']) not in self.character['action_steps']):
      self.state.selected_action = None
    else:
      self.state.selected_action = result['action']
  
  def prepare(self):
    if self.state.selected_action is None:
      return
    Action = ACTION_STEPS[self.state.selected_action]
    action = Action(self.state)
    prepare_steps = action.get_prepare_steps()
    for step in prepare_steps:
      Prepare = PREPARE_STEPS[step]
      prepare = Prepare(self.state)
      prepare.execute()
  
  def execute(self):
    if self.state.selected_action is None:
      return
    Action = ACTION_STEPS[self.state.selected_action]
    action = Action(self.state)
    action.parse()
    action.execute()
    
  def respond(self, request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None):
    self.initialize(request, fid_origin, parent_hash, attachment_hash, root_parent_url)
    self.wakeup()
    self.plan()
    self.prepare()
    self.execute()

    
    # Decide if we should reply or like (or ignore if both are false
    #self.think()
    
    # Respond
    #self.execute_decision()
