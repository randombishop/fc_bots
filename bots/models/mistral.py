import ollama
import json


class MistralLLM():
    
  def query(self, prompt, instructions=None, schema=None):
    model_prompt = prompt+'\n\n'+instructions
    result = ollama.generate(model='mistral', 
                            prompt=model_prompt, 
                            context=[])
    return result['response']


mistral = MistralLLM()