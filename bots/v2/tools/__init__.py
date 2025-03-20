from bots.v2.tools.action import ACTION_TOOLS
from bots.v2.tools.autoprompt import AUTO_PROMPT_TOOLS
from bots.v2.tools.fetch import FETCH_TOOLS
from bots.v2.tools.parse import PARSE_TOOLS
from bots.v2.tools.plan import PLAN_TOOLS
from bots.v2.tools.prepare import PREPARE_TOOLS
from bots.v2.tools.wakeup import WAKEUP_TOOLS


TOOL_MAP = {
  'action': ACTION_TOOLS,
  'autoprompt': AUTO_PROMPT_TOOLS,
  'fetch': FETCH_TOOLS,
  'parse': PARSE_TOOLS,
  'plan': PLAN_TOOLS,
  'prepare': PREPARE_TOOLS,
  'wakeup': WAKEUP_TOOLS
}


TOOL_LIST = []
for x in TOOL_MAP.values():
  TOOL_LIST.extend(x)


TOOL_DEPENDENCIES = {
  x.name: x.metadata['depends_on'] for x in TOOL_LIST if x.metadata is not None and'depends_on' in x.metadata
}