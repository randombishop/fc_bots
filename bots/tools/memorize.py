from langchain.agents import Tool
from langsmith import traceable
from bots.kit_interface.user_id import UserId
from bots.kit_interface.user_info import UserInfo
from bots.kit_interface.image_description import ImageDescription
from bots.kit_interface.user_casts_description import UserCastsDescription
from bots.kit_interface.user_reactions_description import UserReactionsDescription
from bots.kit_interface.avatar import Avatar
from bots.data.users import save_user_profile, save_user_profile_embeds
from bots.models.bert import bert


def get_embed(text):
  if text is None or len(text) < 5:
    return None
  return bert([text])[0]


def format_embed(embed):
  if embed is not None:
    return '[' + ','.join([f'{x:.5f}' for x in embed]) + ']'
  else:
    return None


@traceable(run_type='llm')
def memorize_user_profile(bot_id:int, 
  user_id: UserId, 
  user_info: UserInfo, 
  pfp_description: ImageDescription, 
  casts_description: UserCastsDescription,
  reactions_description: UserReactionsDescription,
  avatar: Avatar):
  bio_text = ''
  if user_info.display_name is not None:
    bio_text += user_info.display_name + '\n'
  if user_info.bio is not None:
    bio_text += user_info.bio
  bio_text = bio_text.strip()
  bio_embed = get_embed(bio_text)
  pfp_embed = get_embed(pfp_description.description)
  casts_embed = get_embed(casts_description.text)
  engagement_text = ''
  if reactions_description.text is not None:
    engagement_text += reactions_description.text + '\n'
  if reactions_description.keywords is not None:
    engagement_text += reactions_description.keywords
  engagement_embed = get_embed(engagement_text)
  avatar_embed = get_embed(avatar.prompt)
  profile = {
      'bot_id': bot_id,
      'fid': user_id.fid,
      'user_name': user_id.username,
      'display_name': user_info.display_name,
      'bio': user_info.bio,
      'pfp_url': pfp_description.url,
      'pfp_desc': pfp_description.description,
      'casts_desc': casts_description.text,
      'engagement_desc': reactions_description.text,
      'engagement_keywords': reactions_description.keywords,
      'avatar_url': avatar.url,
      'avatar_desc': avatar.prompt,
      'num_followers': user_info.followers,
      'num_following': user_info.following       
  }
  save_user_profile(profile)
  embeds = {
    'bot_id': bot_id,
    'fid': user_id.fid,
    'bio_embed': format_embed(bio_embed),
    'pfp_embed': format_embed(pfp_embed),
    'casts_embed': format_embed(casts_embed),
    'engagement_embed': format_embed(engagement_embed),
    'avatar_embed': format_embed(avatar_embed)
  }
  save_user_profile_embeds(embeds)
  return 'Saved user profile in pg'


def get_variables(state, data_types):
  ans = []
  for t in data_types:
    var = state.get_last_variable_value_by_type(t)
    if var is not None:
      ans.append(var)
    else:
      return None
  return ans


def _memorize(state):
  state.memorized = True
  log = []
  user_profile_data = get_variables(state, ['UserId', 'UserInfo', 'ImageDescription', 'UserCastsDescription', 'UserReactionsDescription', 'Avatar'])
  if user_profile_data is not None:
    log1 = memorize_user_profile(state.bot_id, user_profile_data[0], user_profile_data[1], user_profile_data[2], user_profile_data[3], user_profile_data[4], user_profile_data[5])
    log.append(log1)
  return log


memorize = Tool(
  name="memorize",
  description="Memorizes elements of the current state",
  func=_memorize
)