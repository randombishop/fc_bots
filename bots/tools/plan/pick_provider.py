from bots.utils.llms2 import call_llm


schema = {
  "type":"OBJECT",
  "properties":{
    "tool":{"type":"STRING"}
  }
}

def format_instructions(tool, providers):
  provider_names = [x.name for x in providers]
  ans = '#TASK'
  ans += f'You are an AI assistant currently trying to call this tool:\n'
  ans += f'  #{tool.name}\n'
  ans += f'  Description: {tool.description}\n'
  ans += f'\n'
  ans += f'But before calling it, we need to satisfy its dependencies and need to call one of these tools first:\n'
  for provider in providers:
    ans += f'  #{provider.name}\n'
    ans += f'  {provider.description}\n'
  ans += f'\n'
  ans += f'Your task is only to select one of the dependencies, which one makes more sense in the current context?:\n'
  ans += f'If you are not sure, select the one that is most likely to be of general purpose.\n'
  ans += f'\n'
  ans += '#OUTPUT FORMAT\n'
  ans += '{\n'
  ans += f'  "tool": "select one from {",".join(provider_names)}"\n'
  ans += '}\n'
  return ans

def pick_provider(tool, providers, llm, state):
  prompt = state.format_conversation()
  instructions = format_instructions(tool, providers)
  result = call_llm(llm, prompt, instructions, schema)
  if 'tool' not in result:
    return None
  tool = result['tool']
  if tool not in providers:
    return None
  return tool