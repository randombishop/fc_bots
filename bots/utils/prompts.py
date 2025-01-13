

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
