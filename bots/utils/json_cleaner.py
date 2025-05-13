import re


def clean_json(text):
  json_start = text.rfind('```json')
  if json_start != -1:
    json_end = text.find('```', json_start + 7)
    if json_end != -1:
      text = text[json_start + 7:json_end]
  if text.startswith('{{'):
    text = text[1:]
  if text.endswith('}}'):
    text = text[:-1]
  first_brace = text.find('{')
  if first_brace != -1:
    text = text[first_brace:]
  last_brace = text.rfind('}')
  if last_brace != -1:
    text = text[:last_brace+1]
  text = re.sub(r'^\s*otype\s*:\s*[A-Za-z0-9_]+\s*,?\s*$', '', text, flags=re.MULTILINE)
  return text
