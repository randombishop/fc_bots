from bots.bot_state import BotState
from bots.wakeup.bio_provider import WakeUpBio
from bots.wakeup.lore_provider import WakeUpLore
from bots.wakeup.time_provider import WakeUpTime
from bots.wakeup.channel_provider import WakeUpChannel
from bots.wakeup.conversation_provider import WakeUpConversation


class Bot:
  
  def __init__(self, character):
    self.character = character
    self.state = BotState()
    self.wakeup_steps = {
      'bio': WakeUpBio(),
      'lore': WakeUpLore(),
      'time': WakeUpTime(),
      'channel': WakeUpChannel(),
      'conversation': WakeUpConversation()
    }

  def initialize(self, request, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None):
    self.state.request = request
    self.state.fid_origin = fid_origin
    self.state.parent_hash = parent_hash
    self.state.attachment_hash = attachment_hash
    self.state.root_parent_url = root_parent_url

  def wakeup(self):
    for key, step in self.wakeup_steps.items():
      self.state[key] = step.get(self.character, self.state)

  def respond(self):
    # 1. Initialize the state
    self.initialize(self.state.request, 
                    self.state.fid_origin, 
                    self.state.parent_hash, 
                    self.state.attachment_hash, 
                    self.state.root_parent_url)
    
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
