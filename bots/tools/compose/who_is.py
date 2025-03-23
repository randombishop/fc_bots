from langchain.agents import Tool


def compose_who_is(input):
  state = input.state
  fid = state.user_fid
  user_name = state.user
  if fid is None or user_name is None:
    raise Exception(f"Missing fid/user_name")
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


ComposeWhoIs = Tool(
  name="ComposeWhoIs",
  description="Cast about who a user is",
  func=compose_who_is
)

