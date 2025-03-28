from langchain.agents import Tool
from bots.utils.llms2 import call_llm


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

def prepare_psycho(input):
  state = input.state
  llm = input.llm
  df = state.df_casts_for_fid
  if df is None or len(df) == 0:
    raise Exception(f"Not enough activity to buid a psychodegen analysis.")
  data = list(df['text'])
  text = "\n".join([str(x) for x in data])
  instructions = state.format(instructions_template.replace('{{user_name}}', state.user))
  result = call_llm(llm, text, instructions, schema)
  state.user_psycho = result
  return {
    'user_psycho': state.user_psycho
  }


PreparePsycho = Tool(
  name="PreparePsycho",
  description="Generate a funny psycho analysis for a user",
  func=prepare_psycho
)
