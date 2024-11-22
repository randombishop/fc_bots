def clean_json(text):
  if text.startswith('```json'):
    text = text[7:]
  if text.endswith('```'):
    text = text[:-3]
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
  return text
