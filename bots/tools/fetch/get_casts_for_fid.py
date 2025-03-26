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
    'df_casts_for_fid': state.df_casts_for_fid
  }

GetCastsForFid = Tool(
  name="GetCastsForFid",
  description="Get posts by a user.",
  metadata={
    'inputs': 'Will fail if fid and user_name are not set',
    'outputs': 'Makes dataframe df_casts_for_fid'
  },
  func=get_casts_for_fid
)
