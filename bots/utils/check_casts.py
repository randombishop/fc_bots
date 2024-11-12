MAX_CAST_LENGTH = 300

def check_casts(casts):
  for c in casts:
    if len(c['text']) > MAX_CAST_LENGTH:
      c['text'] = c['text'][:MAX_CAST_LENGTH]+'...'
