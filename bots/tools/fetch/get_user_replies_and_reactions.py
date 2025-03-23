from langchain.agents import Tool
from bots.data.casts import get_user_replies_and_reactions as get_user_replies_and_reactions_data
from bots.utils.format_cast import format_when, shorten_text


def get_user_replies_and_reactions(input):
  state = input.state
  if state.user_replies_and_reactions is not None:
    return {'log': 'User replies and reactions already set.'}
  fid = state.user_fid
  user_name = state.user
  if fid is None or user_name is None:
    raise Exception(f"Missing fid or user_name in context.")
  df = get_user_replies_and_reactions_data(fid=fid, max_rows=50)
  rows = df.to_dict('records') if len(df) > 0 else []
  formatted = ''
  for r in rows:
    if r['reaction'] == 'REPLY':
      text = f"# Replied to @{r['to_user_name']} {format_when(r['timestamp'])}:\n"
      text += f"@{r['to_user_name']} said: {shorten_text(r['to_text'])}\n"
      text += f"@{user_name} replied: {r['text']}\n"
      text += '#\n'
      formatted += text
    elif r['reaction'] in ['REPOST', 'LIKE']:
      text = '# '
      text += "Liked" if r['reaction'] == 'LIKE' else "Reposted"
      text += f" @{r['to_user_name']}'s cast {format_when(r['timestamp'])}:\n"
      text += f"@{shorten_text(r['to_text'])}\n"
      text += '#\n'
      formatted += text
  state.user_replies_and_reactions = formatted
  return {
    'user_replies_and_reactions': state.user_replies_and_reactions,
  }


GetUserRepliesAndReactions = Tool(
  name="GetUserRepliesAndReactions",
  description="Get the replies and reactions of a user",
  func=get_user_replies_and_reactions
)
