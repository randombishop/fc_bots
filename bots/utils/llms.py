import ollama
import json

def call_llm(prompt):
  return mistral(prompt)

def mistral(prompt):
  result = ollama.generate(model='mistral', prompt=prompt, context=[])
  response = result['response']
  print('mistral response', response)
  result = json.loads(response)
  if 'error' in result and len(result['error']) > 0:
    raise Exception(result['error'])
  return result
