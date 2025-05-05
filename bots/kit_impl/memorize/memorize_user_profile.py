from bots.kit_interface.user_id import UserId
from bots.kit_interface.user_profile import UserProfile
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


def memorize_user_profile(user_id: UserId, 
             user_profile: UserProfile, 
             pfp_description: ImageDescription, 
             casts_description: UserCastsDescription,
             reactions_description: UserReactionsDescription,
             avatar: Avatar):
  bio_text = ''
  if user_profile.display_name is not None:
    bio_text += user_profile.display_name + '\n'
  if user_profile.bio is not None:
    bio_text += user_profile.bio
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
      'fid': user_id.fid,
      'user_name': user_id.username,
      'display_name': user_profile.display_name,
      'bio': user_profile.bio,
      'pfp_url': pfp_description.url,
      'pfp_desc': pfp_description.description,
      'casts_desc': casts_description.text,
      'engagement_desc': reactions_description.text,
      'engagement_keywords': reactions_description.keywords,
      'avatar_url': avatar.url,
      'avatar_desc': avatar.prompt,
      'num_followers': user_profile.followers,
      'num_following': user_profile.following       
  }
  save_user_profile(profile)
  embeds = {
    'fid': user_id.fid,
    'bio_embed': format_embed(bio_embed),
    'pfp_embed': format_embed(pfp_embed),
    'casts_embed': format_embed(casts_embed),
    'engagement_embed': format_embed(engagement_embed),
    'avatar_embed': format_embed(avatar_embed)
  }
  save_user_profile_embeds(embeds)
  return 'Saved user profile in pg'

