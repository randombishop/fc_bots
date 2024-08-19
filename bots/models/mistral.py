import ollama


def mistral(prompt):
  result = ollama.generate(model='mistral', prompt=prompt)
  return result['response']
