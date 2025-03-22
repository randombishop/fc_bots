from langchain.agents import Tool
from bots.data.casts import get_casts_for_fid as get_casts_for_fid_data


def get_casts_for_fid(input):
  state = input.state
  user_name = state.user
  fid = state.user_fid
  if user_name is None or fid is None:
    raise Exception(f"Missing fid/user_name")
  state.df_casts_for_fid = get_casts_for_fid_data(fid)
  return {
    'df_casts_for_fid': len(state.df_casts_for_fid) if state.df_casts_for_fid is not None else 0
  }

GetCastsForFid = Tool(
  name="GetCastsForFid",
  description="Fetch casts for a user",
  func=get_casts_for_fid
)
