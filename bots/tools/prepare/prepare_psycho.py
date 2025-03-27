from langchain.agents import Tool
from bots.utils.llms2 import call_llm


instructions_template = """
#TASK
You are @{{name}}, an eccentric, witty psychoanalyst with a flair for humor and satire.
Your task is to generate a parody psycho analysis of @{{user}}.

#INSTRUCTIONS:
The posts provided are from @{{user}}.
Based on the posts, provide a hilariously original psychoanalysis of @{{user}}'s personality in 3 sentences.
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

def prepare(input):
  state = input.state
  llm = input.llm
  prompt = state.get('casts_user')
  instructions = state.format(instructions_template)
  result = call_llm(llm, prompt, instructions, schema)
  return {
    'data_user_psycho': result
  }


PreparePsycho = Tool(
  name="PreparePsycho",
  description="Generate a funny psycho analysis for a user",
  metadata={
    'inputs': ['casts_user'],
    'outputs': ['data_user_psycho']
  },
  func=prepare
)
