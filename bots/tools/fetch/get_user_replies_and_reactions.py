from langchain.agents import Tool
from bots.data.casts import get_user_replies_and_reactions as get_user_replies_and_reactions_data
from bots.utils.format_cast import format_when, shorten_text


def fetch(input):
  state = input.state
  fid = state.get('user_fid')
  user_name = state.get('user')
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
  return {
    'user_replies_and_reactions': formatted
  }


GetUserRepliesAndReactions = Tool(
  name="GetUserRepliesAndReactions",
  description="Get the replies and reactions of a user",
  metadata={
    'inputs': ['user_fid', 'user'],
    'outputs': ['user_replies_and_reactions']
  },
  func=fetch
)
