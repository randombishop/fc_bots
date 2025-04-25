from langchain.agents import Tool
from bots.data.dune import run_sql


def fetch(input):
  state = input.state
  sql = state.get('cast_stats_sql')
  df = run_sql(sql)    
  result = ''
  if df is not None and len(df)>0:
    result = df.to_string(index=False)
  return {
    'cast_stats_result': result
  }


GetCastStats = Tool(
  name="GetCastStats",
  description="Get stats from the casts table.",
  metadata={
    'inputs': ['cast_stats_sql'],
    'outputs': ['cast_stats_result']
  },
  func=fetch
)
