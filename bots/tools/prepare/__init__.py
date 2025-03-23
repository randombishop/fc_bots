from bots.tools.prepare.call_perplexity import CallPerplexity
from bots.tools.prepare.get_avatar import GetAvatar
from bots.tools.prepare.get_pfp_description import GetPfpDescription
from bots.tools.prepare.get_user_profile import GetUserProfile
from bots.tools.prepare.get_user_replies_and_reactions import GetUserRepliesAndReactions
from bots.tools.prepare.prepare_summary import PrepareSummary
from bots.tools.prepare.prepare_word_cloud import PrepareWordCloud
from bots.tools.prepare.generate_wordcloud_mask import GenerateWordCloudMask
from bots.tools.prepare.generate_wordcloud import GenerateWordCloud


PREPARE_TOOLS = [
  CallPerplexity,
  GetAvatar,
  GetPfpDescription,
  GetUserProfile,
  GetUserRepliesAndReactions,
  PrepareSummary,
  PrepareWordCloud,
  GenerateWordCloudMask,
  GenerateWordCloud
]