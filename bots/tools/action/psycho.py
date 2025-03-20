from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.data.casts import get_casts_for_fid


instructions_template = """
#TASK
You are @{{name}}, an eccentric, witty psychoanalyst with a flair for humor and satire.
Your task is to generate a parody psycho analysis of @{{user_name}}.

#INSTRUCTIONS:
The posts provided are from @{{user_name}}.
Based on the posts, provide a hilariously original psychoanalysis of @{{user_name}}'s personality in 3 sentences.
Do not use real pathology names, instead, create your own funny medical names with novel issues.
You can mix your psycho analysis with roasting.
Examine the recurring themes and word choices and explain their subconscious motivations in a playful, tongue-in-cheek manner. 
Imagine a blend of Freudian insights and stand-up comedy.
Remember to be creative, original, and thoroughly entertaining but always remain respectful.
Be respectful, and do not use sexual, religious or political references.
Output the result in json format.
Make sure you don't use " inside json strings. Avoid invalid json.
Output 3 sentences in json format.

#RESPONSE FORMAT:
{
  "sentence1": "...",
  "sentence2": "...",
  "sentence3": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "sentence1":{"type":"STRING"},
    "sentence2":{"type":"STRING"},
    "sentence3":{"type":"STRING"}
  }
}

def psycho(input):
  state = input['state']
  llm = input['llm']
  fid = state.action_params['fid']
  if fid is None:
    raise Exception(f"No fid provided.")
  df = get_casts_for_fid(fid)
  if df is None or len(df) == 0:
    raise Exception(f"Not enough activity to buid a psychodegen analysis.")
  data = list(df['text'])
  text = "\n".join([str(x) for x in data])
  instructions = state.format(instructions_template.replace('{{user_name}}', state.action_params['user_name']))
  result = call_llm(llm, text, instructions, schema)
  casts = []
  if 'sentence1' in result:
    casts.append({'text': result['sentence1']})
  if 'sentence2' in result:
    casts.append({'text': result['sentence2']})
  if 'sentence3' in result:
    casts.append({'text': result['sentence3']})
  state.casts = casts
  return {
    'casts': state.casts
  }


Psycho = Tool(
  name="Psycho",
  description="Generate a funny psycho analysis of a user",
  func=psycho,
  metadata={
    'depends_on': ['parse_psycho_params']
  }
)
