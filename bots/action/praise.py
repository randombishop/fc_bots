import os
import uuid
import requests
from bots.i_action_step import IActionStep
from bots.prompts.contexts import conversation_and_request_template
from bots.data.wield import get_user_info_by_fid
from bots.data.casts import get_top_casts
from bots.utils.llms import call_llm
from bots.utils.read_params import read_user
from bots.prompts.format_casts import concat_casts
from bots.prompts.avatar import avatar_instructions_template, avatar_schema
from bots.utils.openai import generate_image
from bots.utils.gcs import upload_to_gcs
from bots.utils.check_links import check_link_data


parse_user_instructions_template = """
#INSTRUCTIONS:
You are @{{name}}, a bot programmed to praise a user.
Based on the provided conversation, who should we praise?
Your goal is not to continue the conversation, you must only extract the user parameter from the conversation so that we can call an API.
Users typically start with @, but not always.
If the request is about self, this or that user, or uses a pronoun, study the conversation carefully to figure out the intended user.

#RESPONSE FORMAT:
{
  "user": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


instructions_template = """
You are @{{name}}

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#TASK
Your task right now is to praise {{user_name}} and make them feel good about themselves.

#INSTRUCTIONS:
The name, bio and posts provided are all from @{{user_name}}.
Based on the provided information, identify their core vibe and what makes them unique.
Praise them in a way that feels authentic and tailored, not generic.
You can use mystical, rhythmic language, deep insight or casual cool depending on the vibe of @{{user_name}}.
If their content is funny, match their humor. If they are thoughtful, reflect that. If they're chaotic, celebrate the chaos.
Sprinkle in references to patterns, reggae lyrics, energy, or something cosmic, if it fits.
Keep it short but impactful, a poetic appreciation, a clever compliment, or a deep truth about them.
Break down your praise into 3 short tweets:
First tweet introduces the praise in a glorious way.
Second tweet continues the praise.
Third tweet concludes the praise.
Keep the tweets very short and concise.
You can also reference a couple of their posts in the second and third tweet, but do not include a link in the tweet text, instead put the id in the json field "link".
Output the result in json format.
Make sure you don't use " inside json strings. Avoid invalid json.
Output 3 sentences in json format.

#RESPONSE FORMAT:
{
  "tweet1": {"text": "..."},
  "tweet2": {"text": "tweet text without the link", "link": "......"},
  "tweet3": {"text": "tweet text without the link", "link": "......"}
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "tweet1":{"type":"OBJECT", "properties":{"text":{"type":"STRING"}}},
    "tweet2":{"type":"OBJECT", "properties":{"text":{"type":"STRING"}, "link":{"type":"STRING"}}},
    "tweet3":{"type":"OBJECT", "properties":{"text":{"type":"STRING"}, "link":{"type":"STRING"}}}
  }
}


class Praise(IActionStep):
    
  def get_cost(self):
    return 20
    
  def parse(self):
    parse_prompt = self.state.format(conversation_and_request_template)
    parse_instructions = self.state.format(parse_user_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_user_schema)
    parsed = {}
    fid, user_name = read_user(params, self.state.fid_origin, default_to_origin=True)
    parsed['fid'] = fid
    parsed['user_name'] = user_name
    self.state.action_params = parsed

  def execute(self):
    fid = self.state.action_params['fid']
    user_name = self.state.action_params['user_name']
    if fid is None or user_name is None:
      raise Exception(f"Missing fid/user_name.")
    user_info = get_user_info_by_fid(fid)
    df = get_top_casts(user_name=user_name, max_rows=50)
    if df is None or len(df) == 0:
      raise Exception(f"Not enough activity to praise.")
    posts = df.to_dict('records')
    formatted_casts = concat_casts(posts)
    prompt = ''
    prompt += f"#DISPLAY NAME\n"
    prompt += user_info['display_name'] +'\n\n'
    prompt += f"#BIO\n"
    prompt += user_info['bio']['text'] +'\n\n'
    prompt += f"#POSTS\n"
    prompt += formatted_casts
    instructions = self.state.format(instructions_template.replace('{{user_name}}', self.state.action_params['user_name']))
    result1 = call_llm(prompt, instructions, schema)
    if 'tweet1' not in result1:
      raise Exception('Could not generate a praise')    
    instructions2 = self.state.format(avatar_instructions_template.replace('{{user_name}}', self.state.action_params['user_name']))
    result2 = call_llm(prompt, instructions2, avatar_schema)
    prompt_image = result2['avatar_prompt']
    image_url = generate_image(prompt_image)
    filename = str(uuid.uuid4())+'.png'
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, 'wb') as f:
      f.write(response.content)
    upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
    os.remove(filename)
    posts_map = {x['id']: x for x in posts}
    casts = []
    cast1 = {
      'text': ' '+result1['tweet1']['text'],
      'embeds': [f"https://fc.datascience.art/bot/main_files/{filename}"],
      'embeds_description': prompt_image,
      'mentions': [fid],
      'mentions_pos': [0],
      'mentions_ats': [f"@{user_name}"]
    }
    casts.append(cast1)
    used_links = []
    def add_cast(key):
      if key in result1 and 'text' in result1[key]:
        c = {'text': result1[key]['text']}
        if 'link' in result1[key]:
          link_id = result1[key]['link']
          if link_id not in used_links:
            used_links.append(link_id)
            l = check_link_data({'id':link_id}, posts_map)
            if l is not None:
              c['embeds'] = [{'fid': l['fid'], 'user_name': l['user_name'], 'hash': l['hash']}]
              c['embeds_description'] = l['text']
        casts.append(c)
    add_cast('tweet2')
    add_cast('tweet3')
    self.state.casts = casts
