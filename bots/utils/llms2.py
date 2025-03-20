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


def rewrite_prompt(llm, original_prompt):
  try:
    messages = [
      SystemMessage("Rewrite the provided prompt to adhere to OpenAI's content policies."),
      HumanMessage(original_prompt)
    ]
    response = llm.invoke(messages)
    return response.content if response else original_prompt
  except Exception as e:
    print('Failed to rewrite the prompt.')
    raise e


def _do_generate_image(llm_img, prompt):
  messages = [HumanMessage(content=prompt)]
  response = llm_img.invoke(messages, size="1024x1024", quality="standard", n=1)
  if hasattr(response, 'data') and response.data:
    return response.data[0].url
  else:
    raise Exception("Image LLM did not return an image URL")


def generate_image(llm_img, llm, prompt):
  try:
    return _do_generate_image(llm_img, prompt)
  except Exception as e:
    if 'content_policy_violation' in str(e).lower():
      print('Content policy violation detected.')
      new_prompt = rewrite_prompt(llm, prompt)
      return _do_generate_image(llm_img, new_prompt)
    else: 
      raise e