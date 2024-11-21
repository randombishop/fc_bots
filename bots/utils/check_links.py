def check_link_data(link, posts_map):
  if not 'id' in link:
    return None
  h = str(link['id'])
  h = h.replace('<', '')
  h = h.replace('>', '')
  h = h.replace('/', '')
  if h in posts_map:
    link['id'] = h
    link['hash'] = posts_map[h]['hash']
    link['fid'] = posts_map[h]['fid']
    link['user_name'] = posts_map[h]['user_name']
    return link
  else:
    return None
