from bots.tools.init import INIT_TOOLS
from bots.tools.intent import INTENT_TOOLS
from bots.tools.plan import PLAN_TOOLS
from bots.tools.parse import PARSE_TOOLS
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.prepare import PREPARE_TOOLS
from bots.tools.check import CHECK_TOOLS
from bots.tools.memorize import MEMORIZE_TOOLS
from bots.tools.helpers import HELPERS_TOOLS


TOOL_MAP = {
  'init': INIT_TOOLS,
  'intent': INTENT_TOOLS,
  'plan': PLAN_TOOLS,
  'parse': PARSE_TOOLS,
  'fetch': FETCH_TOOLS,
  'prepare': PREPARE_TOOLS,
  'check': CHECK_TOOLS,
  'memorize': MEMORIZE_TOOLS,
  'helpers': HELPERS_TOOLS
}


TOOL_LIST = []
for x in TOOL_MAP.values():
  TOOL_LIST.extend(x)
  


  


