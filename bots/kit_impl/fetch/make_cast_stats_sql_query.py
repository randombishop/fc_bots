from bots.kit_interface.dune_query import DuneQuery
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_string
from bots.utils.format_state import format_template


instructions_template = """
#TASK:
You are @{{bot_name}} bot and you have access to a Dune table containing farcaster casts (=posts) features.
Your goal is to prepare a SQL query to help you proceed with your instructions.
What SQL query should we run.
If you can't get the exact information you need, try to get the closest alternative.
You only have access to the table dune.dsart.casts_features.
Your SQL query must not return more than 10 columns and 100 rows. 
Make your SQL query return the minimum amount of information to advance towards your goal.
You must only come up with a valid SQL query.
Note that Dune uses Trino SQL dialect.
Generate your output in valid json format like this {"sql": "..."}

#TARGET TABLE:
dune.dsart.casts_features

#COLUMNS:
|Column|Type|Description|
|---|---|---|
|day|DATE|YYYY-MM-DD|
|timestamp|TIMESTAMP|Cast timestamp as recorded by the Farcaster hub.|
|hash|STRING|Cast hash.|
|fid|INTEGER|Author fid.|
|user_name|STRING|Author username at time of cast.|
|num_follower|INTEGER|Author's number of followers at time of cast.|
|num_follower_bin|INTEGER|num_follower bin from 0 to 9, based on the same hour distribution.|
|num_following|INTEGER|Author's number of followed accounts at time of cast.|
|num_following_bin|INTEGER|num_following bin from 0 to 9, based on the same hour distribution.|
|num_casts_same_hour|INTEGER|Number of times the user casted in the same hour.|
|text|STRING|Cast text.|
|text_len|INTEGER|Cast text length.|
|text_len_bin|INTEGER|text_len bin from 0 to 9, based on the same hour distribution.
|embeds|JSON|Array of embeddings as recorded by the Farcaster hub.
|mentions|JSON|Array of mentions. As recorded by the Farcaster hub.
|mentions_pos|JSON|Array of mentions positions. As recorded by the Farcaster hub.
|embeds_num|INTEGER|Number of embeddings.
|mentions_num|INTEGER|Number of mentions.
|parent_fid|INTEGER|Parent cast fid when it's a reply.
|parent_hash|STRING|Parent cast hash when it's a reply.
|parent_url|STRING|Parent url when it's casted in a channel.
|category|INTEGER|Category classification into one of 11 categories.
|category_label|STRING|Category label, one of c_arts, c_business, c_crypto, c_culture, c_misc, c_money, c_nature, c_politics, c_sports, c_tech_science.
|topic|INTEGER|Topic classification into one of 60 topics.
|topic_label|STRING|Topic label.
|q_clear|INTEGER|Is it clear? (from 0 to 100)
|q_audience|INTEGER|Does it have a clear target audience? (from 0 to 100)
|q_info|INTEGER|Is it informative? (from 0 to 100)
|q_easy|INTEGER|Is it easy to understand for the general layman public? (from 0 to 100)
|q_verifiable|INTEGER|Is it verifiable online? (from 0 to 100)
|q_personal|INTEGER|Is it personal? (from 0 to 100)
|q_funny|INTEGER|Is it funny? (from 0 to 100)
|q_meme_ref|INTEGER|Is it a reference to a well known meme? (from 0 to 100)
|q_emo_res|INTEGER|Does it elicit an emotional response? (from 0 to 100)
|q_happiness|INTEGER|Does it convey happiness? (from 0 to 100)
|q_curiosity|INTEGER|Does it trigger curiosity? (from 0 to 100)
|q_aggressivity|INTEGER|Is it aggressive? (from 0 to 100)
|q_surprise|INTEGER|Does it have an element of surprise? (from 0 to 100)
|q_interesting_ask|INTEGER|Does it ask an interesting question? (from 0 to 100)
|q_call_action|INTEGER|Does it come with an explicit call to action? (from 0 to 100)
|language|STRING|Autodetected language from the text. (en, ca, vi, zh-cn, pt, cy, so, nl, pl, af, ...)


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


def make_cast_stats_sql_query(context: str, bot_name: str) -> DuneQuery:
  prompt = context
  instructions = format_template(instructions_template, {'bot_name': bot_name})
  params = call_llm('medium', prompt, instructions, parse_schema)
  sql = read_string(params, key='sql', default=None, max_length=1024)
  if sql is not None and len(sql) > 10:
    return DuneQuery(sql)
  else:
    return None
  
