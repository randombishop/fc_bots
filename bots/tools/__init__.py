from bots.tools.a_wakeup import WAKEUP_TOOLS
from bots.tools.b_plan import PLAN_TOOLS
from bots.tools.c_parse import PARSE_TOOLS
from bots.tools.d_fetch import FETCH_TOOLS
from bots.tools.e_prepare import PREPARE_TOOLS
from bots.tools.f_combine import COMBINE_TOOLS
from bots.tools.g_check import CHECK_TOOLS
from bots.tools.h_memorize import MEMORIZE_TOOLS


TOOL_MAP = {
  'wakeup': WAKEUP_TOOLS,
  'plan': PLAN_TOOLS,
  'parse': PARSE_TOOLS,
  'fetch': FETCH_TOOLS,
  'prepare': PREPARE_TOOLS,
  'combine': COMBINE_TOOLS,
  'check': CHECK_TOOLS,
  'memorize': MEMORIZE_TOOLS
}


TOOL_LIST = []
for x in TOOL_MAP.values():
  TOOL_LIST.extend(x)

