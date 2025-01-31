
DEFAULT_STATE_TEMPLATE = """
#REQUEST
{{request}}
#PARAMS
fid_origin={{fid_origin}}, parent_hash={{parent_hash}}, attachment_hash={{attachment_hash}}, root_parent_url={{root_parent_url}}
#BIO
{{bio}}
#CHANNEL
{{channel}}
#CONVERSATION
{{conversation}}
#LORE
{{lore}}
#TIME
{{time}}
#STYLE
{{style}}
"""

def concat_casts(posts):
  ans = 'POSTS:\n'
  for post in posts:
    post['id'] = post['hash'][2:8]
    ans += "\n"
    ans += "<"+post['id']+">\n"
    ans += post['user_name'] + " said: " + post['text']
    ans += "\n</"+post['id']+">\n"
  ans += "\n"
  return ans
