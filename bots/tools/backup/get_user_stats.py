from langchain.agents import Tool
from bots.data.dune import run_sql


def fetch(input):
  state = input.state
  sql = state.get('user_stats_sql')
  df = run_sql(sql)    
  result = ''
  if df is not None and len(df)>0:
    result = df.to_string(index=False)
  return {
    'user_stats_result': result
  }


GetUserStats = Tool(
  name="GetUserStats",
  description="Get stats from the user table.",
  metadata={
    'inputs': ['user_stats_sql'],
    'outputs': ['user_stats_result']
  },
  func=fetch
)
