from bots.prepare.get_bot_casts_in_channel import GetBotCastsInChannel
from bots.prepare.get_bot_casts import GetBotCasts
from bots.prepare.get_casts import GetCasts
from bots.prepare.get_channel_casts import GetChannelCasts
from bots.prepare.get_trending import GetTrending
from bots.prepare.should_continue import ShouldContinue


PREPARE_STEPS = {
  'GetBotCastsInChannel': GetBotCastsInChannel,
  'GetBotCasts': GetBotCasts,
  'GetCasts': GetCasts,
  'GetChannelCasts': GetChannelCasts,
  'GetTrending': GetTrending,
  'ShouldContinue': ShouldContinue
}

