from dotenv import load_dotenv
load_dotenv()
import json
import sys
from bots.iaction import IAction
from bots.utils.read_params import read_channel, read_keyword, read_category
from bots.data.casts import get_top_casts
from bots.utils.prompts import concat_casts
from bots.utils.llms import call_llm, get_max_capactity
from bots.utils.check_links import check_link_data
from bots.utils.check_casts import check_casts

parse_instructions = """
INSTRUCTIONS:
Find one or more of the following parameters in the user input: category, channel, keywords. 
Your goal is not to answer the user query, you only need to extract the parameters.
The query doesn't need to match a specific format, your job is to guess the parameters that the user is asking for.

PARAMETERS:
* category, optional, one of pre-defined categories, defaults to null. Allowed categories are: 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* channel, optional, defaults to null. (channels always start with '/', for example '/data', if there is no '/' then it's not a channel)
* keyword, optional, any unique search keyword, if something can't be mapped to a category and doesn't look like a channel, then it's a keyword, defaults to null.

RESPONSE FORMAT:
{
  "category": ...,
  "channel": ...,
  "keyword": ...
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "category":{"type":"STRING"},
    "channel":{"type":"STRING"},
    "keyword":{"type":"STRING"}
  }
}



main_instructions = """
GENERAL INSTRUCTIONS:
YOUR TASK IS TO PROCESS THE SOCIAL MEDIA POSTS RECEIVED FROM A RANDOM SAMPLE OF USERS.
GENERATE A GLOBAL SUMMARY AND SELECT 3 INTERESTING ONES.

DETAILED INSTRUCTIONS:
- Write a catch phrase title.
- Generate 3 sentences to describe what the users are talking about, try to cover as much content as possible in these 3 sentences.
- Include 3 links to reference relevant post ids and comment them with a keyword and emoji.
- Output the result in json format.
- Make sure you don't use " inside json strings. Avoid invalid json.
- Ignore posts that look like ads, promotions, have links to minting NFTs or any other type of commercial activity.
- Focus on posts that are genuine, interesting, funny, or informative.
- Don't reference websites and don't include any urls in your summary.

ADDITIONAL_NOTES?

RESPONSE FORMAT:
{
  "title": "...catch phrase...",
  "sentence1": "...",
  "sentence2": "...",
  "sentence3": "...",
  "link1": {"id": "......", "comment": "keyword [emoji]"},
  "link2": {"id": "......", "comment": "keyword [emoji]"},
  "link3": {"id": "......", "comment": "keyword [emoji]"}
}
"""

main_schema = {
  "type":"OBJECT",
  "properties":{
    "title":{"type":"STRING"},
    "sentence1":{"type":"STRING"},
    "sentence2":{"type":"STRING"},
    "sentence3":{"type":"STRING"},
    "link1":{
       "type":"OBJECT", 
       "properties":{
         "id":{"type":"STRING"},
         "comment":{"type":"STRING"}
       }
    },
    "link2":{
       "type":"OBJECT", 
       "properties":{
         "id":{"type":"STRING"},
         "comment":{"type":"STRING"}
       }
    },
    "link3":{
       "type":"OBJECT", 
       "properties":{
         "id":{"type":"STRING"},
         "comment":{"type":"STRING"}
       }
    }  
  }
}


class DigestCasts(IAction):
    
  def set_input(self, input):
    params = call_llm(input, parse_instructions, parse_schema)
    self.input = input
    self.set_params(params)

  def set_params(self, params):
    self.channel = read_channel(params)
    self.keyword = read_keyword(params)
    self.category = read_category(params)
    self.max_rows = get_max_capactity()
      
  def get_cost(self):
    self.cost = 20
    return self.cost

  def get_data(self):
    # Get data
    posts = get_top_casts(channel=self.channel,
                          keyword=self.keyword,
                          category=self.category,
                          max_rows=self.max_rows)
    posts = posts.to_dict('records')
    posts.sort(key=lambda x: x['timestamp'])
    if len(posts) < 5:
      raise Exception(f"""Not enough posts to generate a digest: channel={self.channel}, 
                      keyword={self.keyword}, category={self.category}, max_rows={self.max_rows}, posts={len(posts)}""")
    # Run LLM
    if self.keyword is not None or self.category is not None:
      add_notes = "ADDITIONAL NOTES:\n"
      if self.keyword is not None:
        add_notes += ("- Focus on the following subject: " + self.keyword + "\n")
      if self.category is not None:
        add_notes += ("- Focus on the following category: " + self.category[2:] + "\n")
      instructions = main_instructions.replace("ADDITIONAL_NOTES?", add_notes)
    else:
      instructions = main_instructions.replace("ADDITIONAL_NOTES?", "")
    prompt = concat_casts(posts)
    result = call_llm(prompt,instructions,main_schema)
    # Make summary
    summary = []
    if 'sentence1' in result and len(result['sentence1']) > 0:
      summary.append(result['sentence1'])
    if 'sentence2' in result and len(result['sentence2']) > 0   :
      summary.append(result['sentence2'])
    if 'sentence3' in result and len(result['sentence3']) > 0:
      summary.append(result['sentence3'])
    try:
      del result['sentence1']
      del result['sentence2']
      del result['sentence3']
    except:
      pass
    result['summary'] = summary
    # Make links
    posts_map = {x['id']: x for x in posts}
    links = []
    for link_key in ['link1', 'link2', 'link3']:
      if link_key in result:
        link = check_link_data(result[link_key], posts_map)
        if link is not None:
          links.append(link)
        del result[link_key]
    result['links'] = links
    # Done
    self.data = result
    return self.data
  
  def get_casts(self, intro=''):
    casts = []
    cast1 = (intro + '\n\n' + self.data['title'] + '\n\n' + self.data['summary'][0]).strip()
    casts.append({'text': cast1})
    for t in self.data['summary'][1:]:
      casts.append({'text': t})
    for link in self.data['links']:
      casts.append({'text': link['comment'], 'embeds': [{'fid': link['fid'], 'user_name': link['user_name'], 'hash': link['hash']}]})
    check_casts(casts)
    self.casts = casts
    return self.casts


if __name__ == "__main__":
  input = sys.argv[1] 
  action = DigestCasts()
  action.set_input(input)
  action.run()
  action.print()
