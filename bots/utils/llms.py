import os
import json5
from bots.models.mistral import mistral
from bots.models.gemini import gemini
from bots.utils.json_cleaner import clean_json


LLM_MAP = {
  'gemini': gemini,
  'mistral': mistral
}
LLM_KEY = os.getenv('LLM_MODEL')
LLM = LLM_MAP[LLM_KEY] if LLM_KEY is not None else None
print(f"Using {LLM_KEY} as LLM")


DEBUG = False


def get_max_capactity():
  if LLM_KEY == 'mistral':
    return 15
  elif LLM_KEY == 'gemini':
    return 50
  else:
    raise Exception(f"Unknown LLM: {LLM_KEY}")


def call_llm(prompt, instructions, schema):
  if DEBUG:
    print("---Calling LLM---")
    print(f"<Instructions>\n{instructions}")
    #print(f"<Schema>\n{schema}")
    if len(prompt) > 100:
      print(f"<Prompt>\n{prompt[:100]}...")
    else:
      print(f"<Prompt>\n{prompt}")
  text = LLM.query(prompt, instructions, schema)
  if DEBUG:
    print(f"<LLM response>\n{text}")
  text = clean_json(text)
  # TODO: check that result is compatible with schema 
  # Maybe run a LLM to fix it if not?
  try:
    result = json5.loads(text)
  except:
    raise Exception(f"Error parsing LLM response: {text}") from None
  if 'error' in result and len(result['error']) > 0:
    raise Exception(result['error'])
  return result


def call_llm_with_attachment(prompt, data, mime_type, instructions, schema):
  text = LLM.query_with_attachment(prompt, data, mime_type, instructions, schema)
  text = clean_json(text)
  try:
    result = json5.loads(text)
  except:
    raise Exception(f"Error parsing LLM response: {text}") from None
  if 'error' in result and len(result['error']) > 0:
    raise Exception(result['error'])
  return result
