import re

MAX_CAST_LENGTH = 300

def clean_text(text):
  if text is None:
    return None
  text = re.sub(r"\$degen", "#Degen", text, flags=re.IGNORECASE)
  return text

def check_casts(casts):
  for c in casts:
    if len(c['text']) > MAX_CAST_LENGTH:
      c['text'] = c['text'][:MAX_CAST_LENGTH]+'...'
    c['text'] = clean_text(c['text'])
