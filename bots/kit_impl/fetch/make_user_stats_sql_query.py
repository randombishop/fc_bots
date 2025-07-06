from bots.kit_interface.dune_query import DuneQuery
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_string
from bots.utils.format_state import format_template


instructions_template = """
#TASK:
You are @{{bot_name}} bot and you have access to a Dune table containing user accounts statistics and features.
Your goal is to prepare a SQL query to help you proceed with your instructions.
What SQL query should we run.
If you can't get the exact information you need, try to get the closest alternative.
You only have access to the table dune.dsart.result_user_features.
Your SQL query must not return more than 10 columns and 100 rows. 
Make your SQL query return the minimum amount of information to advance towards your goal.
You must only come up with a valid SQL query.
Note that Dune uses Trino SQL dialect.
Generate your output in valid json format like this {"sql": "..."}

#TARGET TABLE
dune.dsart.result_user_features

#COLUMNS
|Column|Type|Description|
|---|---|---|
|fid|INTEGER|User id|
|user_name|STRING|Username|
|first_cast_ts|TIMESTAMP|Timestamp of first cast ever|
|last_cast_ts|TIMESTAMP|Timestamp of last recorded cast|
|casts_num|INTEGER|Number of casts (ever)|
|casts_del|INTEGER|Number of casts deleted (ever)|
|casts_30d|INTEGER|Number of casts in the last 30 days|
|days_active|INTEGER|Number of days with some activity in the last 30 days|
|casts_per_day|DOUBLE|Average number of casts per day|
|casts_del_ratio|DOUBLE|Ratio of deletions to casts|
|follower_num|INTEGER|Number of followers|
|follower_inactive|INTEGER|Number of followers who are not active|
|follower_low|INTEGER|Number of followers who with low network score|
|follower_medium|INTEGER|Number of followers who with medium network score|
|follower_high|INTEGER|Number of followers who with high network score|
|following_num|INTEGER|Number of following|
|score_dsart|DOUBLE|Network score calculated by dsart|
|score_openrank|DOUBLE|Network score calculated by openrank|
|score|DOUBLE|Overall network score|


#OUTPUT FORMAT:
{
  "sql": "..."
}
"""


parse_schema = {
  "type":"OBJECT",
  "properties":{
    "sql":{"type":"STRING"}
  }
}


def make_user_stats_sql_query(context: str, bot_name: str) -> DuneQuery:
  prompt = context
  instructions = format_template(instructions_template, {'bot_name': bot_name})
  params = call_llm('medium', prompt, instructions, parse_schema)
  sql = read_string(params, key='sql', default=None, max_length=1024)
  if sql is not None and len(sql) > 10:
    return DuneQuery(sql)
  else:
    return None
