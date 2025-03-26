from langchain.agents import Tool


def compose_favorite_users(input):
  state = input.state
  user_name = state.user
  df = state.df_favorite_users
  table = state.favorite_users_table
  if user_name is None or df is None or table is None:
    raise Exception(f"Missing data")
  if len(df) < 3:
    raise Exception(f"Not enough data ({len(df)})")
  mentions = [int(df.iloc[i]['target_fid']) for i in range(3)]
  mentions_ats = ['@'+df.iloc[i]['User'] for i in range(3)]
  mentions_positions = []
  text = user_name+"'s favorite users are:\n"
  text += "🥇 "
  mentions_positions.append(len(text.encode('utf-8')))
  text += "\n"
  text += "🥈 "
  mentions_positions.append(len(text.encode('utf-8')))
  text += "\n"
  text += "🥉 "
  mentions_positions.append(len(text.encode('utf-8')))
  text += "\n"
  cast = {
    'text': text, 
    'mentions': mentions, 
    'mentions_pos': mentions_positions,
    'mentions_ats': mentions_ats,
    'embeds': [table],
    'embeds_description': 'Favorite users table'
  }
  casts =  [cast]
  state.casts = casts
  return {
    'casts': state.casts
  }


ComposeFavoriteUsers = Tool(
  name="ComposeFavoriteUsers",
  description="Cast the favorite accounts of a user",
  func=compose_favorite_users
)
