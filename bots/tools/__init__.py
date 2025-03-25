from bots.tools.wakeup import WAKEUP_TOOLS
from bots.tools.plan import PLAN_TOOLS
from bots.tools.parse import PARSE_TOOLS
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.prepare import PREPARE_TOOLS
from bots.tools.compose import COMPOSE_TOOLS
from bots.tools.check import CHECK_TOOLS
from bots.tools.memorize import MEMORIZE_TOOLS
from bots.tools.bot_phases import BOT_PHASES
from bots.tools.assistant_phases import ASSISTANT_PHASES


TOOL_MAP = {
  'wakeup': WAKEUP_TOOLS,
  'plan': PLAN_TOOLS,
  'parse': PARSE_TOOLS,
  'fetch': FETCH_TOOLS,
  'prepare': PREPARE_TOOLS,
  'compose': COMPOSE_TOOLS,
  'check': CHECK_TOOLS,
  'memorize': MEMORIZE_TOOLS,
  'bot_phases': BOT_PHASES,
  'assistant_phases': ASSISTANT_PHASES
}


TOOL_LIST = []
for x in TOOL_MAP.values():
  TOOL_LIST.extend(x)
  


