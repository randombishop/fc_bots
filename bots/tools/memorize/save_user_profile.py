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
  if state.selected_action not in ['WhoIs', 'Praise']:
    return {'log': 'No user profile to save'}
  bio_text = state.user_display_name + '\n' + state.user_bio \
              if state.user_bio is not None else None
  bio_embed = get_embed(bio_text)
  pfp_embed = get_embed(state.user_pfp_description)
  casts_embed = get_embed(state.user_casts_description)
  engagement_text = state.user_replies_and_reactions_description + '\n' + \
                    state.user_replies_and_reactions_keywords \
                    if state.user_replies_and_reactions_description is not None else None
  engagement_embed = get_embed(engagement_text)
  avatar_embed = get_embed(state.user_avatar_prompt)
  profile = {
      'fid': state.user_fid,
      'user_name': state.user,
      'display_name': state.user_display_name,
      'bio': state.user_bio,
      'pfp_url': state.user_pfp_url,
      'pfp_desc': state.user_pfp_description,
      'casts_desc': state.user_casts_description,
      'engagement_desc': state.user_replies_and_reactions_description,
      'engagement_keywords': state.user_replies_and_reactions_keywords,
      'avatar_url': state.user_avatar,
      'avatar_desc': state.user_avatar_prompt,
      'num_followers': state.user_followers,
      'num_following': state.user_following       
  }
  save_user_profile(profile)
  embeds = {
    'fid': state.user_fid,
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
  func=memorize,
  description="Save the user profile in long term memory"
)