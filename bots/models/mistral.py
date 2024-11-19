import ollama
import json


def mistral(prompt):
  result = ollama.generate(model='mistral', prompt=prompt, context=[])
  response = result['response']
  try:
    response = response.replace('\\', '\\\\')
    result = json.loads(response)
  except:
    raise Exception(f"Error parsing LLM response: {response}")
  if 'error' in result and len(result['error']) > 0:
    raise Exception(result['error'])
  return result
