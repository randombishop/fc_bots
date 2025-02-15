from bots.prepare.get_bot_casts_in_channel import GetBotCastsInChannel
from bots.prepare.get_bot_casts import GetBotCasts
from bots.prepare.get_casts import GetCasts
from bots.prepare.get_casts_in_channel import GetCastsInChannel
from bots.prepare.get_trending import GetTrending
from bots.prepare.should_continue import ShouldContinue


PREPARE_STEPS = {
  'GetBotCastsInChannel': GetBotCastsInChannel,
  'GetBotCasts': GetBotCasts,
  'GetCasts': GetCasts,
  'GetCastsInChannel': GetCastsInChannel,
  'GetTrending': GetTrending,
  'ShouldContinue': ShouldContinue
}

