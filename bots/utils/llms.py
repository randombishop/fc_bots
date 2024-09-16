import ollama
import json

debug = False

def call_llm(prompt):
  return mistral(prompt)

def mistral(prompt):
  if debug:
    print('mistral prompt', prompt)
  result = ollama.generate(model='mistral', prompt=prompt, context=[])
  response = result['response']
  if debug:
    print('mistral response', response)
  result = json.loads(response)
  if 'error' in result and len(result['error']) > 0:
    raise Exception(result['error'])
  return result
