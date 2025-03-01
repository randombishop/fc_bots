import numpy
from bots.i_memory_step import IMemoryStep
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


class UserProfile(IMemoryStep):
    
  def recall(self):
     pass
  
  def record(self):
    bio_text = self.state.user_display_name + '\n' + self.state.user_bio \
               if self.state.user_bio is not None else None
    bio_embed = get_embed(bio_text)
    pfp_embed = get_embed(self.state.user_pfp_description)
    casts_embed = get_embed(self.state.user_casts_description)
    engagement_text = self.state.user_replies_and_reactions_description + '\n' + \
                      self.state.user_replies_and_reactions_keywords \
                      if self.state.user_replies_and_reactions_description is not None else None
    engagement_embed = get_embed(engagement_text)
    avatar_embed = get_embed(self.state.user_avatar_prompt)
    embeds = [bio_embed, pfp_embed, casts_embed, engagement_embed, avatar_embed]
    embeds = [e for e in embeds if e is not None]
    global_embed = None
    if len(embeds) > 0:
      global_embed = numpy.sum(embeds, axis=0) / len(embeds)
    profile = {
       'fid': self.state.user_fid,
       'user_name': self.state.user,
       'display_name': self.state.user_display_name,
       'bio': self.state.user_bio,
       'pfp_url': self.state.user_pfp_url,
       'pfp_desc': self.state.user_pfp_description,
       'casts_desc': self.state.user_casts_description,
       'engagement_desc': self.state.user_replies_and_reactions_description,
       'engagement_keywords': self.state.user_replies_and_reactions_keywords,
       'avatar_url': self.state.user_avatar,
       'avatar_desc': self.state.user_avatar_prompt,
       'num_followers': self.state.user_followers,
       'num_following': self.state.user_following,
       'bio_embed': format_embed(bio_embed),
       'pfp_embed': format_embed(pfp_embed),
       'casts_embed': format_embed(casts_embed),
       'engagement_embed': format_embed(engagement_embed),
       'avatar_embed': format_embed(avatar_embed),
       'global_embed': format_embed(global_embed)       
    }
    save_user_profile(profile)
    save_user_profile_embeds(profile)
    self.state.log += 'Saved user profile in pg\n'
