MAX_CAST_LENGTH = 300

def check_casts(casts):
  for c in casts:
    if len(c['text']) > MAX_CAST_LENGTH:
      print('truncated cast', len(c['text']))
      c['text'] = c['text'][:MAX_CAST_LENGTH]+'...'
