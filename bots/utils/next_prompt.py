import pandas
import numpy
import random
from bots.data.app import get_bot_prompts, get_bot_channels, get_bot_character
from bots.data.bot_history import get_bot_casts, get_bot_prompts_stats
from bots.data.casts import get_trending_casts
from bots.utils.format_character import format_bio, format_lore
from bots.utils.format_cast import format_bot_casts, format_trending
from bots.utils.llms2 import get_llm, call_llm


task = """
#TASK
You are provided with the current trending posts on the Farcaster platform.
First, read the TRENDING POSTS carefully and summarize them in one short paragraph.
Then, based on the current trends, rank the list of channels by order of preference for your next post. 
Place the channels more relevant to the trends at the top of the list.
Place the channels less relevant to the trends at the bottom of the list.
If you don't have enough information about a channel, put it at the bottom of the list.
Explain your reasoning for the top 5 channels in one paragraph.
Output your decision in JSON format and the channel list as a comma separated string.
Make sure you don't use " inside json strings. Avoid invalid json.

#RESPONSE FORMAT:
{
  "current_trends_summary": "one short paragraph summarizing the current trends",
  "channel_ranking": "most_relevant_channel,channel_2,channel3,...,...,...,least_relevant_channel",
  "reasoning": "explain why you ranked the first 5 channels on top of the list. Use one brief compact sentence per channel."
}
"""

schema = """
  "type":"OBJECT",
  "properties":{
    "current_trends_summary":{"type":"STRING"},
    "channel_ranking":{"type":"STRING"},
    "reasoning":{"type":"STRING"}
"""

def convert(df, field, ascending):
  q = min(len(df), 5)
  mult = 1 if ascending else -1
  noise = numpy.random.uniform(0, 0.0001, size=len(df))
  values = df[field].values * mult + noise
  return pandas.qcut(values, q=q, labels=False, retbins=False)  

def get_channel_ranking(bot_id, df_channels):
  character = get_bot_character(bot_id)
  name = character['name']
  channels = df_channels['channel'].to_list()
  bio = format_bio(character)
  lore = format_lore(character)
  trending = get_trending_casts(50)
  trending = format_trending(trending)
  bot_casts = get_bot_casts(bot_id)
  bot_casts = format_bot_casts(bot_casts, name)
  prompt = f"#TRENDING POSTS\n{trending}\n\n#YOUR RECENT POSTS\n{bot_casts}"
  instructions = f"You are @{name}, a social media bot running on the Farcaster platform.\n\n"
  instructions += f"#YOUR BIO\n{bio}\n\n"
  instructions += f"#YOUR LORE\n{lore}\n\n"
  instructions += f"#YOUR CHANNELS\n{','.join(channels)}\n\n"
  instructions += task
  llm = get_llm()
  result = call_llm(llm, prompt, instructions, schema)
  current_trends_summary = result['current_trends_summary']
  reasoning = result['reasoning']
  channel_ranking = result['channel_ranking']
  if isinstance(channel_ranking, str):
    channel_ranking = channel_ranking.split(',')
  channel_ranking = [c.strip() for c in channel_ranking]
  channel_ranking = [c for c in channel_ranking if c in channels]
  df_channel_ranking = pandas.DataFrame([{'channel':channel_ranking[i], 'relevance_ranking':i+1} for i in range(len(channel_ranking))])
  df_channel_ranking = df_channel_ranking.drop_duplicates(subset=['channel'], keep='first')
  return current_trends_summary, reasoning, df_channel_ranking
  
  
def get_next_prompt(bot_id):
  df_prompts = pandas.DataFrame(get_bot_prompts(bot_id))
  df_channels = pandas.DataFrame(get_bot_channels(bot_id))
  df_stats = pandas.DataFrame(get_bot_prompts_stats(bot_id))
  df = df_prompts[df_prompts['channel'] != '#Autopilot#']
  df_auto = df_prompts[df_prompts['channel'] == '#Autopilot#']
  if len(df_auto) > 0:
    df_auto = df_auto.merge(df_channels[['channel']], how='cross')
    df_auto.drop(columns=['channel_x'], inplace=True)
    df_auto.rename(columns={'channel_y': 'channel'}, inplace=True)
    df = pandas.concat([df, df_auto], ignore_index=True)
  df = df.merge(df_stats, on=['id', 'channel'], how='left')
  current_trends_summary, reasoning, df_ranking = get_channel_ranking(bot_id, df_channels)
  df = df.merge(df_ranking, on='channel', how='left')
  df['relevance_ranking'] = df['relevance_ranking'].astype(float).fillna(len(df))
  df['bot_activity'] = df['bot_activity'].astype(float).fillna(0)
  df['hours_ago'] = df['hours_ago'].astype(float).fillna(9999)
  df['channel_activity'] = df['channel_activity'].astype(float).fillna(9999)
  df['avg_replies'] = df['avg_replies'].astype(float).fillna(0)
  df['avg_likes'] = df['avg_likes'].astype(float).fillna(0)
  df['avg_recasts'] = df['avg_recasts'].astype(float).fillna(0)
  df['avg_engagement'] = df['avg_replies'] + df['avg_likes']*2 + df['avg_recasts']*3
  df['is_candidate'] = (df['channel_activity'] > df['min_activity']) & (df['hours_ago'] > df['min_hours'])
  print('Data frame rows:', len(df))
  df = df[df['is_candidate']]
  print('Candidate rows:', len(df))
  df['boost1'] = convert(df, 'hours_ago', True)
  df['boost2'] = convert(df, 'bot_activity', False)
  df['boost3'] = convert(df, 'channel_activity', True)
  df['boost4'] = convert(df, 'avg_engagement', True)
  df['boost5'] = convert(df, 'relevance_ranking', False)
  df['boost'] = df['boost1'] + df['boost2'] + df['boost3'] + df['boost4'] + df['boost5']
  df.sort_values(by='boost', ascending=False, inplace=True)
  df.reset_index(drop=True, inplace=True)
  del df['last_cast']
  del df['avg_replies']
  del df['avg_likes']
  del df['avg_recasts']
  candidates = df[['id', 'channel']].to_dict(orient='records')
  weights = df['boost'].tolist()
  selected = random.choices(candidates, weights=weights, k=1)[0]
  return {
    'prompt_id': selected['id'],
    'prompt': selected['prompt'],
    'channel': selected['channel'],
    'current_trends_summary': current_trends_summary,
    'reasoning': reasoning,
    'dataframe': df
  }
  
  