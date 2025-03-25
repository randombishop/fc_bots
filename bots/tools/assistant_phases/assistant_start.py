from langchain.agents import Tool
from bots.tools.wakeup.get_bio import GetBio
from bots.tools.wakeup.get_lore import GetLore
from bots.tools.wakeup.get_style import GetStyle
from bots.tools.wakeup.get_time import GetTime
from bots.tools.fetch.get_trending import GetTrending
from bots.tools.fetch.get_casts_in_channel import GetCastsInChannel
from bots.tools.fetch.get_bot_casts_in_channel import GetBotCastsInChannel
from bots.tools.parse.parse_instructions_params import ParseInstructionsParams
from bots.tools.fetch.get_casts_for_context import GetCastsForContext
from bots.tools.plan.select_action_from_instructions import SelectActionFromInstructions


def assistant_start(input):
  GetBio.invoke({'input': input})
  GetLore.invoke({'input': input})
  GetStyle.invoke({'input': input})
  GetTime.invoke({'input': input})
  GetTrending.invoke({'input': input})
  GetCastsInChannel.invoke({'input': input})
  GetBotCastsInChannel.invoke({'input': input})
  ParseInstructionsParams.invoke({'input': input})
  GetCastsForContext.invoke({'input': input})
  SelectActionFromInstructions.invoke({'input': input})
  return {'log': 'ok'}


AssistantStart = Tool(
  name="AssistantStart",
  description="Assistant start phase",
  func=assistant_start
)