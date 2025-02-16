import pandas
import random
import numpy
from bots.i_plan_step import IPlanStep
from bots.utils.llms import call_llm


prompt_template = """
#TRENDING POSTS
{{trending}}
"""

instructions_template = """
You are @{{name}} social media bot running on the Farcaster platform.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#LIST OF CHANNELS
{{channel_list}}

#YOUR RECENT POSTS IN THE CHANNELS
{{recent_casts}}

#INSTRUCTIONS
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


class SelectChannel(IPlanStep):
    
  def plan(self):
    print('SelectChannel.plan()')
    df_channels = self.state.channel_list
    channels_list = df_channels['channel'].tolist()
    random.shuffle(channels_list)
    channels_string = ",".join(channels_list)
    instructions1 = self.state.format(instructions_template.replace('{{channel_list}}',channels_string))
    prompt1 = self.state.format(prompt_template)
    result = call_llm(prompt1, instructions1, schema)
    current_trends_summary = result['current_trends_summary']
    channel_ranking = result['channel_ranking'].split(',')
    reasoning = result['reasoning']
    df_channel_ranking = pandas.DataFrame([{'channel':channel_ranking[i], 'relevance_ranking':i+1} for i in range(len(channel_ranking))])
    df_channel_ranking = df_channel_ranking.drop_duplicates(subset=['channel'], keep='first')
    df_channels = df_channels.merge(df_channel_ranking, on='channel', how='left')
    df_channels['relevance_ranking'] = df_channels['relevance_ranking'].fillna(len(df_channels)).astype(int)
    def convert(field, ascending):
      q = min(len(df_channels), 5)
      mult = 1 if ascending else -1
      noise = numpy.random.uniform(0, 0.0001, size=len(df_channels))
      values = df_channels[field].values * mult + noise
      return pandas.qcut(values, q=q, labels=False, retbins=False) 
    df_channels['boost1'] = convert('hours', True)
    df_channels['boost2'] = convert('bot_activity', False)
    df_channels['boost3'] = convert('channel_activity', True)
    df_channels['boost4'] = convert('avg_engagement', True)
    df_channels['boost5'] = convert('relevance_ranking', False)
    df_channels['boost'] = df_channels['boost1'] + df_channels['boost2'] \
      + df_channels['boost3'] + df_channels['boost4'] \
      + df_channels['boost5']
    df_channels = df_channels[df_channels['boost'] > 0].copy()
    df_channels.sort_values(by='boost', ascending=False, inplace=True)
    df_channels.reset_index(drop=True, inplace=True)
    del df_channels['last_post']
    del df_channels['avg_replies']
    del df_channels['avg_likes']
    del df_channels['avg_recasts']
    channel_list = df_channels['channel'].tolist()
    channel_weights = df_channels['boost'].tolist()
    selected_channel = random.choices(channel_list, weights=channel_weights, k=1)[0]
    log = df_channels[df_channels['channel'] == selected_channel].to_dict(orient='records')[0]
    self.state.selected_channel = selected_channel
    self.state.selected_channel_df = df_channels
    self.state.selected_channel_reasoning = 'Trending:' + current_trends_summary + '\n' + 'Reasoning:' + reasoning
    self.state.selected_channel_log = log
