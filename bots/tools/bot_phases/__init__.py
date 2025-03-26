from bots.tools.bot_phases.bot_wakeup import BotWakeup
from bots.tools.bot_phases.bot_plan import BotPlan
from bots.tools.bot_phases.bot_action import BotAction
from bots.tools.bot_phases.bot_check import BotCheck
from bots.tools.bot_phases.bot_memorize import BotMemorize


BOT_PHASES = [
  BotWakeup,
  BotPlan,
  BotAction,
  BotCheck,
  BotMemorize
]
