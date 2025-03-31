from bots.tools.init.get_bio import GetBio
from bots.tools.init.get_conversation import GetConversation
from bots.tools.init.get_lore import GetLore
from bots.tools.init.get_style import GetStyle
from bots.tools.init.get_time import GetTime
from bots.tools.init.init_state import InitState
from bots.tools.init.should_continue import ShouldContinue


INIT_TOOLS = [
  GetBio,
  GetConversation,
  GetLore,
  GetStyle,
  GetTime,
  InitState,
  ShouldContinue
]
