def clean_json(text):
  if text.startswith('```json'):
    text = text[7:]
  if text.endswith('```'):
    text = text[:-3]
  if text.startswith('{{'):
    text = text[1:]
  if text.endswith('}}'):
    text = text[:-1]
  return text
