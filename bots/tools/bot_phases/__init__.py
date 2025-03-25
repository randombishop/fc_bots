from bots.tools.bot_phases.bot_wakeup import BotWakeup
from bots.tools.bot_phases.bot_plan import BotPlan
from bots.tools.bot_phases.bot_parse import BotParse
from bots.tools.bot_phases.bot_fetch import BotFetch
from bots.tools.bot_phases.bot_prepare import BotPrepare
from bots.tools.bot_phases.bot_compose import BotCompose
from bots.tools.bot_phases.bot_check import BotCheck
from bots.tools.bot_phases.bot_memorize import BotMemorize


BOT_PHASES = [
  BotWakeup,
  BotPlan,
  BotParse,
  BotFetch,
  BotPrepare,
  BotCompose,
  BotCheck,
  BotMemorize
]
