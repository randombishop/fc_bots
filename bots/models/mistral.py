import ollama


def mistral(prompt):
  result = ollama.generate(model='mistral', prompt=prompt, context=[])
  return result['response']
