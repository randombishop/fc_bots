import uuid
import os
from bots.i_action_step import IActionStep
from bots.utils.llms import call_llm
from bots.utils.read_params import read_channel
from bots.data.users import get_top_daily_casters
from bots.utils.images import user_activity_chart
from bots.utils.gcs import upload_to_gcs
from bots.data.channels import get_channel_url, get_channel_by_url

parse_instructions_template = """
#INSTRUCTIONS:
You are @{{name}}, a bot programmed to list the most active users in a social media channel.
Based on the provided conversation, which channel should we look at? 
Your goal is not to continue the conversation, you must only extract the channel parameter.
Channels typically start with /, but not always.

#CURRENT CHANNEL: 
{{channel}}

#RESPONSE FORMAT:
{
  "channel": ...
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "channel":{"type":"STRING"}
  }
}


class MostActiveUsers(IActionStep):

  def get_cost(self):
    return 20
  
  def auto_prompt(self):
    channel_url = get_channel_url(self.state.selected_channel)
    if channel_url is None:
      raise Exception("Most Active Users autoprompt can't find channel_url")
    self.state.action_params = {'channel': channel_url}
    self.state.request = f'Most active users in channel /{self.state.selected_channel}'
    self.state.conversation = self.state.request
    
  def parse(self):
    parse_prompt = self.state.format_conversation()
    parse_instructions = self.state.format(parse_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_schema)
    parsed = {}
    parsed['channel'] = read_channel(params, current_channel=self.state.root_parent_url, default_to_current=True)
    self.state.action_params = parsed

  def execute(self):
    channel_url = self.state.action_params['channel']
    if channel_url is None:
      raise Exception("Missing channel")
    channel_id = get_channel_by_url(channel_url)
    if channel_id is None:
      raise Exception("Channel not registered")
    df = get_top_daily_casters(channel_url)
    if len(df) == 0:
      raise Exception("Query returned 0 rows")
    filename = str(uuid.uuid4())+'.png'
    user_activity_chart(df, filename)
    upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
    os.remove(filename)
    num_mentions = min(len(df), 3)
    mentions = [int(df.iloc[i]['fid']) for i in range(num_mentions)]
    mentions_ats = ['@'+df.iloc[i]['User'] for i in range(num_mentions)]
    mentions_positions = []
    users_label = "casters"
    if channel_id == 'mfers':
      users_label = "mfers"
    text = f"The most active {users_label}"
    if channel_id != 'mfers':
      text += f" in /{channel_id}"
    text += " are:\n"
    text += "🥇 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += f" : {df.iloc[0]['casts_total']} casts.\n"
    if num_mentions > 1:
      text += "🥈 "
      mentions_positions.append(len(text.encode('utf-8')))
      text += f" : {df.iloc[1]['casts_total']} casts.\n"
    if num_mentions > 2:
      text += "🥉 "
      mentions_positions.append(len(text.encode('utf-8')))
      text += f" : {df.iloc[2]['casts_total']} casts.\n"
    cast = {
      'text': text, 
      'mentions': mentions, 
      'mentions_pos': mentions_positions,
      'mentions_ats': mentions_ats,
      'embeds': [f"https://fc.datascience.art/bot/main_files/{filename}"],
      'embeds_description': "Chart of top active users in the channel"
    }
    casts =  [cast]
    self.state.casts = casts
   