import pandas
import random
from bots.data.bot_history import get_bot_casts
from bots.utils.read_params import read_category
from bots.utils.llms import get_max_capactity
from bots.utils.format_cast import shorten_text, format_when
from bots.prepare.get_trending import GetTrending
from bots.utils.llms import call_llm


MIN_HOURS_FOR_CATEGORIES = 120


prompt_template = """
#TRENDING POSTS
{{trending}}

#YOUR PREVIOUSLY POSTED SUMMARIES
{{bot_casts_in_channel}}
"""

instructions_template = """
You are @{{name}} social media bot running on the Farcaster platform.
Your task is to come up with the next search phrase to generate a new summary and post in channel /{{selected_channel}}

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#INSTRUCTIONS
You are provided with recent activity in the /{{selected_channel}} channel.
Generate a new search phrase that we will use to search for posts and summarize them.
Your search phrase should be simple and short.
Your search phrase should be designed to find posts that are relevant to the channel activity.
Do not generate multiple search phrases or complex ones.
Please generate only one single, simple and short search phrase that will be used to search for posts.
Your search phrase should be made of 5 to 7 words.
Do not copy existing posts.
Do not re-use your previous summary prompts.
Output your decision in JSON format.
Make sure you don't use " inside json strings. Avoid invalid json.

#RESPONSE FORMAT:
{
  "search": "search phrase to find interesting posts"
}
"""

schema = """
  "type":"OBJECT",
  "properties":{
    "search":{"type":"STRING"}
"""



def summary_prompt_no_channel(state):
  previous_summaries = get_bot_casts(state.id, no_channel=True, selected_action='Summary')
  df = pandas.DataFrame(previous_summaries)
  df['is_category_summary'] = df['action_prompt'].str.startswith('Summarize category')
  log = 'Previous summaries:\n' + str(df[['action_prompt', 'hours']])
  # First, try to re-run a category summary
  if df['is_category_summary'].sum() > 0:
    log += f'Found {int(df["is_category_summary"].sum())} category summaries...\n'
    categories = df[df['is_category_summary']].groupby('action_prompt'
                    ).agg({'hours': 'min'}).reset_index().to_dict(orient='records')
    for c in categories:
      c['category'] = read_category({'category': c['action_prompt'].replace('Summarize category', '').strip()})
      c['hours'] = float(c['hours'])
    categories = [x for x in categories if x['category'] is not None and x['hours'] > MIN_HOURS_FOR_CATEGORIES]
    if len(categories) > 0:
      category = random.choice(categories)
      log += 'Selected category summary: '+category['category']
      return category['action_prompt'], {'category': category['category'], 'max_rows': get_max_capactity()}, log
    else:
      log += f'No category summaries found within the last {MIN_HOURS_FOR_CATEGORIES} hours.\n'
  # If no category is applicable, figure out a search phrase
  text = ''
  for c in previous_summaries:
    row = '{\n'
    row += f"  prompt: {c['action_prompt']}\n"
    row += f"  post: {shorten_text(c['casted_text'])}\n"
    row += f"  when: {format_when(c['casted_at'])}\n"
    row += '}\n'
    text += row
  state.bot_casts_in_channel = text
  GetTrending(state).prepare()
  prompt = state.format(prompt_template)
  instructions = state.format(instructions_template)
  result = call_llm(prompt, instructions, schema)
  if result is None or 'search' not in result:
    raise Exception('Could not generate a new summary prompt.')
  search = result['search']
  prompt = f'Summarize posts about "{search}"'
  log += 'Selected search summary: '+search
  return prompt, {'search': search}, log
