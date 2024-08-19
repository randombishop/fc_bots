import ollama


def call_model(prompt):
  result = ollama.generate(model='mistral', prompt=prompt)
  return result['response']
