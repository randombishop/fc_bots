from bots.tools.e_prepare.generate_wordcloud_mask import GenerateWordCloudMask
from bots.tools.e_prepare.generate_wordcloud import GenerateWordCloud
from bots.tools.e_prepare.get_avatar import GetAvatar
from bots.tools.e_prepare.get_pfp_description import GetPfpDescription
from bots.tools.e_prepare.get_user_profile import GetUserProfile
from bots.tools.e_prepare.get_user_replies_and_reactions import GetUserRepliesAndReactions
from bots.tools.e_prepare.prepare_digest_casts import PrepareDigestCasts
from bots.tools.e_prepare.prepare_word_cloud import PrepareWordCloud


PREPARE_TOOLS = [
  GenerateWordCloudMask,
  GenerateWordCloud,
  GetAvatar,
  GetPfpDescription,
  GetUserProfile,
  GetUserRepliesAndReactions,
  PrepareDigestCasts,
  PrepareWordCloud
]