from langchain.agents import Tool


def who_is(input):
  state = input['state']
  fid = state.action_params['fid']
  user_name = state.action_params['user_name']
  if fid is None or user_name is None:
    raise Exception(f"Missing fid/user_name.")
  text = state.user_casts_description
  if text is None or text == '':
    raise Exception(f"Profile Description is empty")
  embeds = [state.user_avatar] if state.user_avatar is not None else []
  embeds_description = 'Avatar Img' if state.user_avatar is not None else None
  cast = {
    'text': ' ' + text,
    'embeds': embeds,
    'embeds_description': embeds_description,
    'mentions': [fid],
    'mentions_pos': [0],
    'mentions_ats': [f"@{user_name}"]
  }
  state.casts = [cast]
  return {
    'casts': state.casts
  }


WhoIs = Tool(
  name="WhoIs",
  description="Who is action",
  func=who_is,
  metadata={
    'depends_on': ['parse_praise_params', 'get_user_profile', 'get_pfp_description', 'get_user_replies_and_reactions', 'get_avatar']
  }
)

