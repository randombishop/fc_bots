from langchain.agents import Tool
from bots.utils.check_links import check_link_data


def compose_praise(input):
  state = input.state
  fid = state.user_fid
  user_name = state.user
  result1 = state.user_praise
  if fid is None or user_name is None or result1 is None:
    raise Exception(f"Missing data.")
  embeds = [state.user_avatar] if state.user_avatar is not None else []
  embeds_description = 'Avatar Img' if state.user_avatar is not None else None
  casts = []
  cast1 = {
    'text': ' '+result1['tweet1']['text'],
    'embeds': embeds,
    'embeds_description': embeds_description,
    'mentions': [fid],
    'mentions_pos': [0],
    'mentions_ats': [f"@{user_name}"]
  }
  casts.append(cast1)
  used_links = []
  def add_cast(key):
    if key in result1 and 'text' in result1[key]:
      c = {'text': result1[key]['text']}
      if 'link' in result1[key]:
        link_id = result1[key]['link']
        if link_id not in used_links:
          used_links.append(link_id)
          l = check_link_data({'id':link_id}, state.posts_map)
          if l is not None:
            c['embeds'] = [{'fid': l['fid'], 'user_name': l['user_name'], 'hash': l['hash']}]
            c['embeds_description'] = l['text']
            c['embeds_warpcast'] = f"https://warpcast.com/{l['user_name']}/{l['hash'][:10]}"
      casts.append(c)
  add_cast('tweet2')
  add_cast('tweet3')
  state.casts = casts
  return {
    'casts': state.casts
  }


ComposePraise = Tool(
  name="ComposePraise",
  description="Cast a user praise",
  func=compose_praise
)