from langchain_core.messages import HumanMessage, SystemMessage
from bots.utils.json_cleaner import clean_json
import json5


def call_llm(llm, prompt, instructions, schema):
  messages = [
    SystemMessage(instructions),
    HumanMessage(prompt)
  ]
  result = llm.invoke(messages)
  text = result.content
  text = clean_json(text)
  # TODO: check that result is compatible with schema 
  # Maybe run a LLM to fix it if not?
  try:
    result = json5.loads(text)
  except:
    raise Exception(f"Error parsing LLM response")
  if 'error' in result and len(result['error']) > 0:
    raise Exception(result['error'])
  return result
