from bots.i_prepare_step import IPrepareStep
from bots.data.casts import get_user_replies_and_reactions
from bots.utils.llms import call_llm
from bots.utils.format_cast import format_when, shorten_text

prompt_template = """
# USER ID
@{{user}}

# USER DISPLAY NAME
{{user_display_name}}

# USER BIO
{{user_bio}}

# USER POSTS
{{user_replies_and_reactions}}
"""

instructions_template = """
You are @{{name}} bot

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#INSTRUCTIONS:
You are analyzing replies, likes and recasts from @{{user}} on the social media platform Farcaster. 
Your goal is to describe the kind of content and topics they typically engage with.
Analyze their replies, likes and reposts carefully to understand their interests and preferences.
Extract the topics that they find interesting.
Your output will be published in their profile under the rubric "What they react to"
Your descrition should be positive and respectful.
Your goal is not to summarize the actual content they engage with, you must instead capture what they typically like in more general terms and keywords.
Avoid judgment or personal opinions and keep your description neutral.
Output your description in one sentence, plus a list of keywords.
Make sure you don't use " inside json strings. Avoid invalid json.
Output your description and keywords in the following json format. 

#RESPONSE FORMAT:
{
  "description": "..."
  "keywords": "comma separated list of keywords"
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "description":{"type":"STRING"},
    "keywords":{"type":"STRING"}
  }
}


class GetUserRepliesAndReactions(IPrepareStep):
    
  def prepare(self):
    if self.state.user_replies_and_reactions_description is not None:
      return
    fid = self.state.user_fid
    user_name = self.state.user
    if fid is None or user_name is None:
      raise Exception(f"Missing fid or user_name in context.")
    df = get_user_replies_and_reactions(fid=fid, max_rows=50)
    rows = df.to_dict('records') if len(df) > 0 else []
    formatted = ''
    for r in rows:
      if r['reaction'] == 'REPLY':
        text = f"# Replied to @{r['to_user_name']} {format_when(r['timestamp'])}:\n"
        text += f"@{r['to_user_name']} said: {shorten_text(r['to_text'])}\n"
        text += f"@{user_name} replied: {r['text']}\n"
        text += '#\n'
        formatted += text
      elif r['reaction'] in ['REPOST', 'LIKE']:
        text = '# '
        text += "Liked" if r['reaction'] == 'LIKE' else "Reposted"
        text += f" @{r['to_user_name']}'s cast {format_when(r['timestamp'])}:\n"
        text += f"@{shorten_text(r['to_text'])}\n"
        text += '#\n'
        formatted += text
    self.state.user_replies_and_reactions = formatted
    if len(rows)>0:
      prompt = self.state.format(prompt_template)
      instructions = self.state.format(instructions_template)
      result = call_llm(prompt, instructions, schema)
      description = result['description'] if 'description' in result else ''
      keywords = result['keywords'] if 'keywords' in result else ''
      self.state.user_replies_and_reactions_description = description
      self.state.user_replies_and_reactions_keywords = keywords
    log = '<GetUserRepliesAndReactions>\n'
    log += f"{len(rows)} rows\n"
    log += f"description: \n{self.state.user_replies_and_reactions_description}\n"
    log += f"keywords: \n{self.state.user_replies_and_reactions_keywords}\n"
    log += '</GetUserRepliesAndReactions>\n'
    self.state.log += log
  