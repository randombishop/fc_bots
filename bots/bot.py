from bots.bot_state import BotState
from bots.wakeup.wakeup_steps import WAKEUP_STEPS


DEFAULT_WAKEUP_STEPS = [
  'bio',
  'lore',
  'style',
  'time',
  'channel',
  'conversation'
]

class Bot:
  
  def __init__(self, character, wakeup_steps=DEFAULT_WAKEUP_STEPS):
    self.character = character
    self.wakeup_steps = wakeup_steps
    self.state = BotState()

  def initialize(self, request, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None):
    self.state.request = request
    self.state.fid_origin = fid_origin
    self.state.parent_hash = parent_hash
    self.state.attachment_hash = attachment_hash
    self.state.root_parent_url = root_parent_url

  def wakeup(self):
    for key in self.wakeup_steps:
      wakeup_step = WAKEUP_STEPS[key]()
      wakeup_value = wakeup_step.get(self.character, self.state)
      self.state.set(key, wakeup_value)

  def respond(self, request, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None):
    # 1. Initialize the state
    self.initialize(request, fid_origin, parent_hash, attachment_hash, root_parent_url)
    
    # 2. Wake up steps
    self.wakeup()
    
    # 3. Plan actions (for v1 we can just pick one)
    #self.plan_actions()
    
    # 4. Execute actions
    #self.execute_actions()

    # 5. Prepare a response
    #self.prepare_response()
    
    # 6. Decide if we should reply, like or ignore
    #self.think()
    
    # 7. Execute decision
    #self.execute_decision()
