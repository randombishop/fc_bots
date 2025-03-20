from bots.v2.tools.prepare.generate_wordcloud_mask import GenerateWordCloudMask
from bots.v2.tools.prepare.generate_wordcloud import GenerateWordCloud
from bots.v2.tools.prepare.prepare_digest_casts import PrepareDigestCasts
from bots.v2.tools.prepare.prepare_word_cloud import PrepareWordCloud


PREPARE_TOOLS = [
  GenerateWordCloudMask,
  GenerateWordCloud,
  PrepareDigestCasts,
  PrepareWordCloud
]