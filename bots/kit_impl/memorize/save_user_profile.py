from langchain.agents import Tool
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


def memorize(input):
  state = input.state
  bio_text = ''
  if state.get('user_display_name') is not None:
    bio_text += state.get('user_display_name') + '\n'
  if state.get('user_bio') is not None:
    bio_text += state.get('user_bio')
  bio_text = bio_text.strip()
  bio_embed = get_embed(bio_text)
  pfp_embed = get_embed(state.get('user_pfp_description'))
  casts_embed = get_embed(state.get('user_casts_description'))
  engagement_text = ''
  if state.get('user_replies_and_reactions_description') is not None:
    engagement_text += state.get('user_replies_and_reactions_description') + '\n'
  if state.get('user_replies_and_reactions_keywords') is not None:
    engagement_text += state.get('user_replies_and_reactions_keywords')
  engagement_embed = get_embed(engagement_text)
  avatar_embed = get_embed(state.get('user_avatar_prompt'))
  profile = {
      'fid': state.get('user_fid'),
      'user_name': state.get('user'),
      'display_name': state.get('user_display_name'),
      'bio': state.get('user_bio'),
      'pfp_url': state.get('user_pfp_url'),
      'pfp_desc': state.get('user_pfp_description'),
      'casts_desc': state.get('user_casts_description'),
      'engagement_desc': state.get('user_replies_and_reactions_description'),
      'engagement_keywords': state.get('user_replies_and_reactions_keywords'),
      'avatar_url': state.get('user_avatar'),
      'avatar_desc': state.get('user_avatar_prompt'),
      'num_followers': state.get('user_followers'),
      'num_following': state.get('user_following')       
  }
  save_user_profile(profile)
  embeds = {
    'fid': state.get('user_fid'),
    'bio_embed': format_embed(bio_embed),
    'pfp_embed': format_embed(pfp_embed),
    'casts_embed': format_embed(casts_embed),
    'engagement_embed': format_embed(engagement_embed),
    'avatar_embed': format_embed(avatar_embed)
  }
  save_user_profile_embeds(embeds)
  return {'log': 'Saved user profile in pg'}


SaveUserProfile = Tool(
  name="SaveUserProfile",
  description="Save the user profile in long term memory",
  metadata={
    'inputs': ['user', 'user_fid', 'user_display_name', 'user_bio', 'user_avatar'],
  },
  func=memorize
)